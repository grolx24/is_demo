import asyncio
import os.path
import time

import requests

from upload_call.models.call_info_model import CallInfo
from django.conf import settings

import pandas as pd


class ImporterCrmExcel:

    def __init__(self, but, filename):
        self.excel_file = pd.ExcelFile(filename)
        self.origin_id_prefix = time.time()
        self.but = but
        self.object_count = dict()
        self.methods = [self.import_companies,
                        self.import_contacts,
                        self.import_leads,
                        self.import_deals,
                        self.import_calls,
                        ]

    def import_all_crm(self):
        for method in self.methods:
            try:
                a = time.time()
                method()
                print(method.__str__(), time.time() - a)
            except Exception as e:
                print(f"Exception in {method} - {e}")

    def add_origin_prefix(self, companies_excel):
        """
        В файле ексель(гугл) док мы делаем связку между страницами по полю ORIGIN_ID, т.к при импорте в Б24 мы получим новые ID сущностей.
        Эта функция помогает делать уникальные ORIGIN_ID для единовременного импорта демоданных
        для всех записей добавляет префикс (Мы его возьмем как текущее время с микросекундами)
        у все записей "10" станет "1690205018.084936_10"
        """

        for company in companies_excel:
            # Добавляем префикс для ORIGIN_ID
            if company.get('ORIGIN_ID'):
                company['ORIGIN_ID'] = "{}_{}".format(self.origin_id_prefix, company.get('ORIGIN_ID'))
        return companies_excel

    def load_crm(self, crm_items, type_id):
        # загружаем элементы crm в битрикс пакетными запросами
        methods = []
        for item in crm_items:
            methods.append(('crm.item.batchImport',
                            {"entityTypeId": type_id, "data": [item]}))
        self.but.batch_api_call(methods)

    def make_links_from_origin(self, contacts_excel, excel_field, b24_field, companies_bitrix_origin_id):
        # заменяет excel_field=COMPANY_ORIGIN_ID на b24_field=COMPANY_ID учитывая предыдущую замену при импорте демоданных
        # для создания правильной адресации на только что созданные сущности
        for contact in contacts_excel:
            # Добавляем префикс для ORIGIN_ID
            if contact.get(excel_field):
                contact[b24_field] = \
                    companies_bitrix_origin_id["{}_{}".format(self.origin_id_prefix, contact.get(excel_field))]['ID']
        return contacts_excel

    async def api_crm_address_add(self, company):
        await asyncio.to_thread(self.but.call_api_method, "crm.address.add", {"fields": {
            "TYPE_ID": "1",  # Идентификатор типа адреса. Фактический адрес?
            "ENTITY_TYPE_ID": "4",  # 4 - для Компаний
            "ENTITY_ID": self.companies_bitrix_origin_id[company['ORIGIN_ID']]['ID'],
            "CITY": company["ADDRESS_CITY"],
            "ADDRESS_1": company["ADDRESS"],
        }})

    async def multi_api_crm_address_add(self, companies):
        tasks = [self.api_crm_address_add(company) for company in companies]
        return await asyncio.gather(*tasks)

    def import_companies(self):
        companies_csv = self.excel_file.parse('Компании').to_dict("records")
        companies_csv = self.add_origin_prefix(companies_csv)
        self.object_count["Компании"] = len(companies_csv)

        self.load_crm(companies_csv, "4")

        companies_bitrix = self.but.call_list_method('crm.company.list', {
            "SELECT": ["ORIGIN_ID", "ID"],
            "FILTER": {"%ORIGIN_ID": "{}_".format(self.origin_id_prefix)}
        })
        self.companies_bitrix_origin_id = {item['ORIGIN_ID']: item for item in companies_bitrix}

        asyncio.run(self.multi_api_crm_address_add(companies_csv))
        return self

    def import_contacts(self):
        contacts_excel = self.excel_file.parse('Контакты').to_dict("records")
        contacts_excel = self.make_links_from_origin(contacts_excel,
                                                     'COMPANY_ORIGIN_ID',
                                                     'COMPANY_ID',
                                                     self.companies_bitrix_origin_id)
        for contact in contacts_excel:
            contact["PHONE"] = [{"VALUE": str(contact["PHONE"]), "VALUE_TYPE": "WORK"}]

        self.load_crm(contacts_excel, "3")
        self.object_count["Контакты"] = len(contacts_excel)
        return self

    def import_leads(self):
        leads_data = self.excel_file.parse('Лиды').to_dict("records")
        self.object_count["Лиды"] = len(leads_data)
        self.load_crm(leads_data, "1")
        return self

    def import_deals(self):
        deals_data = self.excel_file.parse('Сделки').to_dict("records")
        self.object_count["Сделки"] = len(deals_data)
        self.load_crm(deals_data, "2")
        return self

    def import_calls(self):
        calls_data = self.excel_file.parse('Звонки').to_dict('records')
        self.object_count["Звонки"] = len(calls_data)

        for call in calls_data:
            call_info = CallInfo(
                user_phone=call["user_phone"],
                user_id=int(call["user_id"]),
                phone_number=call["phone_number"],
                show_call=0,
                create_crm=0,
                call_date=call["call_date"],
                type=int(call["type"]),
                add_to_chat=int(call["add_to_chat"])
            )
            call_info.save()

            drive_id = call["file"].split("/")[-2]
            url = "https://drive.google.com/uc?id=" + drive_id + "&export=download"
            result = requests.get(url, allow_redirects=True)

            file_path = os.path.join(call_info.inner_media_path, str(call_info.id) + '.mp3')
            with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb') as file:
                file.write(result.content)

            call_info.file.name = file_path
            call_info.save()

            call_info.telephony_externalcall_register(self.but)
            call_info.telephony_externalcall_finish(self.but)
            call_info.telephony_externalcall_attach_record(self.but)
        return self
