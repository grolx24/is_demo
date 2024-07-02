from django.apps import AppConfig
import os

class AutocompleteCrmTasksConfig(AppConfig):
    name = 'autocomplete_crm_tasks'
    path = os.path.dirname(os.path.abspath(__file__))