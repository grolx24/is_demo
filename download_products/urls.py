from django.urls import path

from .views.download_xlsx import download_xlsx

urlpatterns = [
    path('download_xlsx/', download_xlsx, name='xlsx'),
]
