import asyncio

from django.db import models

from integration_utils.bitrix24.exceptions import BitrixApiError


class CompanyBPModel(models.Model):
    process_id = models.IntegerField(unique=True)
    process_name = models.CharField(max_length=200)

    @staticmethod
    def find_all_bizprocs(but):
        res_bizprocs = but.call_list_method('bizproc.workflow.template.list',
                                            {'select': ["ID", "NAME"],
                                             'filter': {"DOCUMENT_TYPE": [
                                                 "crm",
                                                 "CCrmDocumentCompany",
                                                 "COMPANY"
                                             ]}})
        for item in res_bizprocs:
            CompanyBPModel.objects.update_or_create(process_id=item['ID'], defaults={"process_name": item['NAME']})

    async def run_BP(self, but, company_id):
        try:
            res = await asyncio.to_thread(but.call_api_method, 'bizproc.workflow.start', {
                'TEMPLATE_ID': self.process_id,
                'DOCUMENT_ID': ['crm', 'CCrmDocumentCompany', str(company_id)]
            })
        except BitrixApiError:
            res = None
        return res

    async def run_multiple_bp(self, but, companies):
        tasks = [self.run_BP(but, company["ID"]) for company in companies]
        return await asyncio.gather(*tasks)

    def __str__(self):
        return f"Бизнес процесс {self.process_id} - {self.process_name}"