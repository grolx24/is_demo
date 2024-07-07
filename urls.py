"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import settings
from django.contrib import admin
from django.urls import path, include
from post_currency.views import *
from django.conf.urls.static import static

from start.views.start import start

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', start),
    path('tasks/', include('tasks.urls')),
    path('ones/', include('ones_fresh_unf_with_b24.urls')),
    path('crmfields/', include('crmfields.urls')),
    path('callsuploader/', include('callsuploader.urls')),
    path('duplicatefinder/', include('duplicatefinder.urls')),
    path('urlmanager/', include('usermanager.urls')),
    path('selectuser/', include('selectuser.urls')),
    path('company_on_map/', include('company_on_map.urls')),
    path('employeegrid/', include('employeegrid.urls')),
    path('product_list_in_excel/', include('product_list_excel.urls')),
    path('allcompbizproc/', include('allcompbizproc.urls')),
    path('import_company_google/', include('import_company_google.urls')),
    path('demo_data_in_bitrix/', include('demo_data_in_bitrix.urls')),
    path('sample_tg_bot/', include('sample_tg_bot.urls')),
    path('audio_recognition/', include('audio_recognition.urls')),
    path('best_call_manager/', include('best_call_manager.urls')),
    path('move_deadline_task/', include('calls_to_telegram.urls')),
    path('tg_open_ai/', include('tg_openai_bot.urls')),
    path('deal_for_powerbi/', include('deal_for_powerbi.urls')),
    path('autocomplete_crm_tasks/', include('autocomplete_crm_tasks.urls')),
    path('move_tasks_deadline_js/', include('move_tasks_deadline_js.urls', 'move_tasks_deadline_js')),

    path('myapp/', include('myapp.urls')),
    path('upload_call/', include('upload_call.urls')),
    path('duplicate_entity/', include('duplicate_entity.urls')),
    path('search_supervisors/', include('search_supervisors.urls')),
    path('start_bp_all_company/', include('start_bp_all_company.urls')),
    path('import_crm_from_googledocs/', include('import_crm_googledocs.urls')),
    path('sort_user_field/', include('sort_user_field.urls')),
    path('tg_bot/', include('tg_bot.urls')),
    path('calls_to_tgchat/', include('calls_to_tgchat.urls')),
    path('best_managers_call/', include('best_managers_call.urls')),
    path('robot/', include('robot_weather.urls', 'bitrix_robot_currency')),
    path('save_companies/', include('save_companies_bd.urls')),
    path('move_deadline_task/', include('move_deadline_task.urls')),
    path('map_companies/', include('map_companies.urls')),
    path('chat_bot/', include('chat_bot.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
