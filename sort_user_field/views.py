import traceback

from django.http import JsonResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from.utils import sort_bitrix


@main_auth(on_cookies=True)
def user_list(request):
    but = request.bitrix_user_token

    user_fields = but.call_api_method("crm.company.userfield.list", {"order": {"SORT": "ASC"}})["result"]
    name_user_fields = [{'id': element["ID"], 'name': element["FIELD_NAME"]} for element in user_fields]

    return render(request, 'fields_for_sort.html', {'name_user_fields': name_user_fields})


@main_auth(on_cookies=True)
def show_user_field(request):
    if request.method == 'POST':
        try:
            but = request.bitrix_user_token
            user_id = request.POST.get('user_id')
            user_field_list = but.call_api_method("crm.company.userfield.list", {
                "order": {"SORT": "ASC"},
                "filter": {"ID": user_id}
            })["result"][0]["LIST"]

            user_field_list_value = [element["VALUE"] for element in user_field_list]

            return JsonResponse({'status': 'success', 'user_field_list_value': user_field_list_value})
        except Exception as e:
            traceback.print_exc()
    return JsonResponse({'status': 'failed'}, status=400)


@main_auth(on_cookies=True)
def sort_user_field(request):
    but = request.bitrix_user_token
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            sort_bitrix(but, user_id)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            traceback.print_exc()
    return JsonResponse({'status': 'failed'}, status=400)
