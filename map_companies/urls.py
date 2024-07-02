from django.urls import path

from map_companies.views.company_on_map_view import map_companies_view
from map_companies.views.companies import companies

urlpatterns = [
    path('', map_companies_view, name="company_on_map"),
    path('companies/', companies, name="companies"),
]
