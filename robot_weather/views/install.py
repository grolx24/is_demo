from django.http import HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from robot_weather.models.robot_weather_model import WeatherRobot


@main_auth(on_cookies=True)
def install(request):
    try:
        WeatherRobot.install_or_update('bitrix_robot_currency:handler_robot', request.bitrix_user_token)
    except Exception as exc:
        return HttpResponse(str(exc))

    return HttpResponse('ok')
