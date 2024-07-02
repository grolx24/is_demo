from django.urls import path

from .views.crm_from_googledocs import crm_from_googledocs

urlpatterns = [
    path('crm_gdocs/', crm_from_googledocs, name='crm_gdocs'),
]
