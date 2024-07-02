from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models.bitrix_user import BitrixUser


@main_auth(on_cookies=True)
def lead_fields(request):
    but = request.bitrix_user_token
    table_fields = but.call_list_method("crm.lead.fields")

    list_dicts_fields = []
    for id_data, data in table_fields.items():
        data = {k: str(v) for k, v in data.items()}
        data["id"] = id_data
        list_dicts_fields.append(data)

    contex = {
        'table_fields': list_dicts_fields,
    }

    return render(request, 'lead_fields_grid.html', contex)