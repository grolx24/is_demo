import json
import dateutil.parser as pr
import datetime as dt

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUser
from django.shortcuts import redirect


@main_auth(on_start=True, set_cookie=True)
def move(request):
    return render(request, 'template.html', {"info": None})


@csrf_exempt
@xframe_options_exempt
def move_by_admin(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Bad Request: This endpoint only accepts POST requests.')

    but = BitrixUser.objects.filter(is_admin=True, user_is_active=True).first().bitrix_user_token
    task_id = request.POST.get("task_id", None)

    date_info = but.call_api_method("tasks.task.get", {
        "taskId": task_id, "select": ["DEADLINE"]})['result']['task']['deadline']
    if date_info is None:
        datetime_date = dt.datetime.now()
    else:
        datetime_date = pr.parse(date_info)
    moved_date = datetime_date + dt.timedelta(days=1)
    str_moved_date = moved_date.strftime('%d.%m.%Y %H:%M:%S')

    but.call_api_method("tasks.task.update", {"taskId": task_id, "fields": {"DEADLINE": str_moved_date}})
    return HttpResponse("updated")


@main_auth(on_cookies=True)
def move_for_auth(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Bad Request: This endpoint only accepts POST requests.')

    but = BitrixUser.objects.filter(is_admin=True, user_is_active=True).first().bitrix_user_token
    task_id = request.POST.get("task_id", None)

    date_info = but.call_api_method("tasks.task.get", {
        "taskId": task_id, "select": ["DEADLINE"]})['result']['task']['deadline']
    if date_info is None:
        datetime_date = dt.datetime.now()
    else:
        datetime_date = pr.parse(date_info)
    moved_date = datetime_date + dt.timedelta(days=1)
    str_moved_date = moved_date.strftime('%d.%m.%Y %H:%M:%S')

    but.call_api_method("tasks.task.update", {"taskId": task_id, "fields": {"DEADLINE": str_moved_date}})
    return HttpResponse("updated")


@main_auth(on_cookies=True)
def move_my(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Bad Request: This endpoint only accepts POST requests.')

    but = BitrixUser.objects.filter(is_admin=True, user_is_active=True).first().bitrix_user_token
    task_id = request.POST.get("task_id", None)

    task_info = but.call_api_method("tasks.task.get", {
        "taskId": task_id, "select": ["DEADLINE", "CREATED_BY"]})['result']['task']
    date_info = task_info["deadline"]
    task_creator = task_info["creator"]["id"]

    if task_creator != str(request.bitrix_user.bitrix_id):
        return HttpResponse("not creator")

    if date_info is None:
        datetime_date = dt.datetime.now()
    else:
        datetime_date = pr.parse(date_info)
    moved_date = datetime_date + dt.timedelta(days=1)
    str_moved_date = moved_date.strftime('%d.%m.%Y %H:%M:%S')

    but.call_api_method("tasks.task.update", {"taskId": task_id, "fields": {"DEADLINE": str_moved_date}})
    return HttpResponse("updated")
