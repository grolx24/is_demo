from django.urls import path

from .models.robot_weather_model import WeatherRobot
from .views.install import install
from .views.robot_weather_view import robot_weather
from .views.uninstall import uninstall

app_name = 'bitrix_robot_currency'

urlpatterns = [
    path('home/', robot_weather, name='robot_currency_home'),
    path('install/', install, name='install_robot'),
    path('uninstall/', uninstall, name='uninstall_robot'),
    path('handler/', WeatherRobot.as_view(), name='handler_robot'),
]
