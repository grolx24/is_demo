from best_managers_call.utils.table_creation import add_row, add_row_to_df
from best_managers_call.utils.api_methods import *
from best_managers_call.utils.datetime_utils import parse_date_in_dmy

from search_supervisors.utils.search_manager import search_manager

import pandas as pd
from prettytable import PrettyTable


def make_manager_dict(but):
    user_dict, _ = search_manager(but)
    manager_dict = dict()

    for manager_id, user in user_dict.items():
        if len(user["SUPERVISORS"]) < 1:
            manager_dict[manager_id] = manager_id
        else:
            sup_ords = user["SUPERVISORS_ORDER"]
            min_sup = min(sup_ords, key=sup_ords.get)
            manager_dict[manager_id] = user["SUPERVISORS"].get(min_sup)
    return manager_dict


def setting_tasks(but, calls):
    """Позволяет поставить задачи по выбору лучшего звонка пользователям."""

    manager_dict = make_manager_dict(but)

    call_info_df = pd.DataFrame(
        columns=["CALL_ID", "MANAGER_ID", "PHONE_NUMBER",
                 "START_DATE", "START_DATETIME", "DURATION", "CALL_TYPE"])

    for call in calls:
        add_row_to_df(call_info_df, call)

    call_info_df.sort_values(by="START_DATETIME", inplace=True)
    call_info_df = call_info_df.groupby(["MANAGER_ID", "START_DATE"])

    table = PrettyTable()
    table.field_names = ["№", "ID звонка", "Номер телефона",
                         "Дата и время звонка",
                         "Длительность звонка",
                         "Тип звонка"]

    task_id_list = list()
    possible_calls = {}

    for group, call_df in call_info_df:
        call_df.reset_index(drop=True, inplace=True)
        table.clear_rows()

        calls_for_task = []

        for index, row in call_df.iterrows():
            add_row(table, index + 1, row)

            calls_for_task.append(row["CALL_ID"])

        task_id = add_task(but, group[0], manager_dict[group[0]], table,
                           parse_date_in_dmy(group[1]))
        task_id_list.append(task_id)

        possible_calls[task_id] = calls_for_task

    return task_id_list, possible_calls


def update_app_possible_calls(but, possible_calls):
    app_possible_calls = but.call_api_method("app.option.get", {"option": "possible_calls"})["result"]
    if app_possible_calls and type(app_possible_calls) is dict:
        app_possible_calls.update(possible_calls)
    else:
        app_possible_calls = possible_calls
    return app_possible_calls


def update_tasks_id(but, task_id_list):
    app_tasks_id = get_app_tasks_id(but)
    if app_tasks_id and app_tasks_id[0] != '':
        app_tasks_id.extend(task_id_list)
    else:
        app_tasks_id = task_id_list
    return app_tasks_id


def check_complete_tasks(progress_tasks_id, app_tasks):
    completed_tasks = dict()
    for task in app_tasks:
        if task["status"] == '5':  # STATE_COMPLETED = 5
            progress_tasks_id.remove(task["id"])
            completed_tasks[task["id"]] = task
    return completed_tasks


def get_app_possible_calls(but):
    possible_calls = but.call_api_method("app.option.get", {"option": "possible_calls"})["result"]
    if type(possible_calls) is not dict:
        raise ValueError(f"possible_calls не установлена на портале")
    return possible_calls


def process_completed_tasks(but, completed_tasks, possible_calls, uncompleted_tasks_id):
    calls = dict()
    for task_id, task in completed_tasks.items():
        try:
            task_res = get_task_res(but, task_id)
        except IndexError:
            uncompleted_tasks_id.append(task_id)

            but.call_api_method("tasks.task.renew", {"taskId": task_id})
            but.call_api_method("task.commentitem.add", {
                "TASKID": task_id,
                "FIELDS": {
                    "AUTHOR_ID": task["createdBy"],
                    "POST_MESSAGE": "Оставьте комментарий помеченный как результат"
                }
            })

            continue

        if possible_calls.get(task_id):
            if not (task_res["text"] in possible_calls[task_id]):
                uncompleted_tasks_id.append(task_id)

                but.call_api_method("tasks.task.renew", {"taskId": task_id})
                but.call_api_method("task.commentitem.add", {
                    "TASKID": task_id,
                    "FIELDS": {
                        "AUTHOR_ID": task["createdBy"],
                        "POST_MESSAGE": "Укажите корректный id звонка"
                    }
                })

                continue
            else:
                del possible_calls[task_id]

        calls[task_res["text"]] = task["responsible"]["name"]

    return calls
