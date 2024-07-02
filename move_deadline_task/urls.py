from django.urls import path

from .views.move_deadline import move, move_by_admin, move_for_auth, move_my

urlpatterns = [
    path('', move, name='move'),
    path('byAdmin/', move_by_admin, name='byAdmin'),
    path('move_for_auth/', move_for_auth, name='forAuth'),
    path('move_mine/', move_my, name='onlyOwn'),
]
