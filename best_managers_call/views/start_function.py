from django.shortcuts import render

from best_managers_call.utils.datetime_utils import get_now_date
from best_managers_call.utils.utils import setting_tasks, update_app_possible_calls, update_tasks_id
from best_managers_call.utils.api_methods import *
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def start_find_all_call(request):
    """Позволяет получить все звонки, найти среди них подходящие по условию,
    и поставить пользователям задачу на выбор лучшего звонка за каждый день
    когда они были совершены, также пользователям в комментарии к задаче
    отправляется таблица с удобочитаемыми данными, чтобы пользователь смог
    проанализировать информацию и сделать выбор"""

    info = None
    if request.method == "POST":
        but = request.bitrix_user_token
        now_date = get_now_date()
        try:
            app_date = get_app_date(but)

            if app_date == now_date:
                return render(request, "best_managers_call_temp.html", {"info": "Сегодня уже создавались задачи"})
            else:
                calls = get_new_calls(but, app_date, now_date)
        except (TypeError, KeyError):
            calls = get_all_calls(but, now_date)

        task_id_list, possible_calls = setting_tasks(but, calls)

        app_possible_calls = update_app_possible_calls(but, possible_calls)
        app_tasks_id = update_tasks_id(but, task_id_list)

        set_app_tasks_id(but, app_tasks_id)
        set_app_possible_calls(but, app_possible_calls)
        set_app_date(but, now_date)
        info = "Задачи созданы"

    return render(request, "best_managers_call_temp.html", {"info": info})
