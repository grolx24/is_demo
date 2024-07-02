from django.urls import path

from sort_user_field.views import user_list, show_user_field, sort_user_field

urlpatterns = [
    path('', user_list, name='user_list'),
    path('show_user_field', show_user_field, name='show_user_field'),
    path('sort_user_field', sort_user_field, name='sort_user_field'),
]
