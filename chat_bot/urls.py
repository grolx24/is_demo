from django.urls import path

from chat_bot.views.text_req import chat_bot
from chat_bot.views.command_req import command

urlpatterns = [
    path('main', chat_bot, name="chat_bot"),
    path('command_intent/', command, name="command_intent"),
]