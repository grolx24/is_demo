from django.urls import path

from chat_bot.views import chat_bot, register_bot_view, command_intent

urlpatterns = [
    path('main', chat_bot, name="chat_bot"),
    path('register_bot_view/', register_bot_view, name="register"),
    path('command_intent/', command_intent, name="command_intent"),
]