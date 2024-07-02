from django.urls import path

from .views import send_tg_message

urlpatterns = [
    path('', send_tg_message, name='tg_message'),
]
