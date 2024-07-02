from collections import Counter

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

API_methods = {
    "lead": ("crm.lead.list", "TITLE"),
    "deal": ("crm.deal.list", "TITLE"),
    "product": ("crm.product.list", "NAME"),
    "contact": ("crm.contact.list", "NAME"),
    "company": ("crm.company.list", "TITLE"),
}


@main_auth(on_cookies=True)
def find_dupl(request):
    but = request.bitrix_user_token
    duplicates = {}
    entity = ''
    if request.method == 'POST':
        entity = request.POST.get('entity')
        if entity and entity in API_methods:
            lst_ent = but.call_list_method(API_methods[entity][0], {"select": [API_methods[entity][1]]})
            titles = [entry[API_methods[entity][1]] for entry in lst_ent]
            duplicates = {name: count for name, count in Counter(titles).items() if count > 1}
    return render(request, 'dupl.html', {"duplicates": duplicates, "entity": entity})
#
