from django.urls import path

from .views.employee_list import employee_list

urlpatterns = [
    path('show_list/', employee_list),
]
