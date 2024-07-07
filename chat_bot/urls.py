from django.urls import path

from chat_bot.views import chat_bot, register_bot_view, echo_command

urlpatterns = [
    path('main', chat_bot, name="chat_bot"),
    path('register_bot_view/', register_bot_view, name="register"),
    path('echo_command/', echo_command, name="echo_command"),
]