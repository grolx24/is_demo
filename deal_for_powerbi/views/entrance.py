from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from local_settings import POWER_BI_SECRET, APP_SETTINGS


@main_auth(on_cookies=True)
def entrance(request):
    """
    Выводит инструкцию
    """

    return render(request, 'export_deals_temp.html', {"secret": POWER_BI_SECRET, "domain": APP_SETTINGS.app_domain})
