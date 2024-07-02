import requests
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..forms.link_import_form import LinkImportForm
from ..utils.import_crm_csv import ImporterCrmExcel


@main_auth(on_cookies=True)
def crm_from_googledocs(request):
    but = request.bitrix_user_token
    object_count = None
    if request.method == 'POST':
        form = LinkImportForm(request.POST)
        if form.is_valid():
            model = form.save()
            try:
                filename = model.download_xlsx()
                importer = ImporterCrmExcel(but, filename)
                importer.import_all_crm()
                object_count = importer.object_count

            except (requests.exceptions.RequestException, OSError) as e:
                print("error  loading the file:", e)
            except Exception as e:
                print("error importing crm data in bitrix24:", e)

    form = LinkImportForm()
    return render(request, 'link_for_import.html', {"form": form, "object_count": object_count})
