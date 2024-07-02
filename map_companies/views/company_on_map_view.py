from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from settings import YMAPS_API_KEY


@main_auth(on_cookies=True)
def map_companies_view(request):
    return render(request, 'map_companies.html', {"YMAPS_API_KEY": YMAPS_API_KEY})
