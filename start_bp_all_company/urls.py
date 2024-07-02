from django.urls import path

from .views.runbizproc import run_bizproc
from crmfields.views.reload import reload_start

urlpatterns = [
    path('run_bizproc/', run_bizproc, name='run'),
]
