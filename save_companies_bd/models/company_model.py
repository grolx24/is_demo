import json

from django.db import models


class Company(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    data = models.JSONField()

    @staticmethod
    def sync_companies(but):
        contacts = but.call_list_method("crm.contact.list",
                                        {"filter": {"!COMPANY_ID": None},
                                         "select": ["COMPANY_ID", "LAST_NAME", "NAME", "SECOND_NAME", "PHONE"]})
        contacts_by_company = {}
        for contact in contacts:
            contacts_by_company.setdefault(contact['COMPANY_ID'], []).append(contact)

        companies = but.call_list_method("crm.company.list")
        companies_by_id = {}
        for company in companies:
            company["CONTACT"] = contacts_by_company.get(company['ID'], None)
            companies_by_id[company['ID']] = company

        companies_obj = []
        for index, data in companies_by_id.items():
            data_json = json.dumps(data)
            companies_obj.append(Company(id=index, data=data_json))

        if len(companies_obj) != 0:
            Company.objects.bulk_create(
                companies_obj,
                update_conflicts=True,
                unique_fields=['id'],
                update_fields=['data'])

        return len(companies_obj)