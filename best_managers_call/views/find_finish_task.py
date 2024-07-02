import html
from django.shortcuts import render
from best_managers_call.utils.table_creation import get_html_row, get_html_table
from best_managers_call.utils.api_methods import *
from best_managers_call.utils.utils import check_complete_tasks, get_app_possible_calls, process_completed_tasks
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def find_finish_task(request):
    """Позволяет собрать все результаты завершенных задач. Создает группу
    если она не существует, а если существует берет ее id. По результату
    задач находит нужный звонок и делает пост с таблицей лучших звонков
    каждого менеджера."""

    if request.method == "POST":
        but = request.bitrix_user_token

        app_tasks_id = get_app_tasks_id(but)
        if not app_tasks_id or app_tasks_id[0] == '':
            return render(request, 'best_managers_call_temp.html', {"info": "Нет установленных задач"})

        app_tasks = get_app_tasks(but, app_tasks_id)

        uncompleted_tasks_id = app_tasks_id
        completed_tasks = check_complete_tasks(uncompleted_tasks_id, app_tasks)
        if not completed_tasks:
            return render(request, 'best_managers_call_temp.html', {"info": "Нет выполненных задач"})

        possible_calls = get_app_possible_calls(but)

        calls = process_completed_tasks(but, completed_tasks, possible_calls, uncompleted_tasks_id)

        set_app_tasks_id(but, uncompleted_tasks_id)
        but.call_api_method("app.option.set", {"options": {"possible_calls": possible_calls}})

        app_calls = get_app_calls(but, list(calls.keys()))

        rows = ""
        for counter, app_call in enumerate(app_calls, 1):
            row = get_html_row(app_call, calls, counter)
            rows += row

        html_table = get_html_table(rows)

        group_id = get_app_group(but)
        add_post(but, f"{html.unescape(html_table)}", [f"SG{group_id}"])

    return render(request, "best_managers_call_temp.html", {"info": "Лучшие звонки загружены в группу"})
