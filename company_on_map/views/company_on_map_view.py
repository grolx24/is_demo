from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def company_on_map(request):
    return render(request, 'company_on_map_temp.html')
