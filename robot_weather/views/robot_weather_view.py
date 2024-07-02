from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def robot_weather(request):

    return render(request, 'robot_weather_temp.html', locals())
