from django.urls import path

from .views.lead_fields import lead_fields


urlpatterns = [
    path('lead_fields/', lead_fields, name='lead_fields'),
]