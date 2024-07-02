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
        return JsonResponse([])

    all_addresses = but.call_list_method("crm.address.list", {
        "order": {"TYPE_ID": "ASC"},
        "select": ["ADDRESS_1", "CITY", "PROVINCE", "COUNTRY", "ANCHOR_ID"],
        "filter": {"ANCHOR_TYPE_ID": "4"}  # 4 - компании
    })

    comps_w_addr = []
    for address in all_addresses:
        comp_id = address["ANCHOR_ID"]
        if not all_companies.get(comp_id):
            continue

        country = address['COUNTRY'] if address['COUNTRY'] is not None else ''
        city = address['CITY'] if address['CITY'] is not None else ''
        exact_address = address['ADDRESS_1'] if address['ADDRESS_1'] is not None else ''

        comps_w_addr.append({"name": all_companies[comp_id]["TITLE"], "address": f"{country} {city} {exact_address}"})
    return JsonResponse(comps_w_addr, safe=False)
