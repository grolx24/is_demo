from django.urls import path

from .views.save_companies_view import save_companies

urlpatterns = [
    path('', save_companies, name='save_companies'),
]
