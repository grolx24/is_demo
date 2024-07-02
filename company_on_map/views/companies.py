from django.http import JsonResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def companies(request):
    """Возвращает JSON со списком компаний с известными адресами"""
    but = request.bitrix_user_token
    all_companies = but.call_list_method("crm.company.list", {
        "select": ["ID", "TITLE"]
    })
    all_companies = {c["ID"]: c for c in all_companies}

    if not all_companies:
        return JsonResponse({})

    all_addresses = but.call_list_method("crm.address.list", {
        "order": {"TYPE_ID": "ASC"},
        "select": ["ADDRESS_1", "CITY", "PROVINCE", "COUNTRY", "ANCHOR_ID"],
        "filter": {"ANCHOR_TYPE_ID": "4"}  # компании
    })

    if not all_addresses:
        return JsonResponse({})

    comps_w_addr = {}
    for address in all_addresses:
        comp_id = address["ANCHOR_ID"]
        if not all_companies.get(comp_id):
            continue

        comp = comps_w_addr.setdefault(comp_id, {})
        comp.setdefault("addr", []).append(address)
        comp["title"] = all_companies[comp_id]["TITLE"]

    return JsonResponse(comps_w_addr)
