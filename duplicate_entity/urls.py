from django.urls import path

from duplicate_entity.views.find_duplicate import  find_dupl

urlpatterns = [
    path('duplicate/', find_dupl, name='find_dupl'),
]
