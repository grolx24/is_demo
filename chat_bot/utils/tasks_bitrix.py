from datetime import datetime, timedelta, timezone


class TasksBitrix:
    def __init__(self, but):
        self.but = but

    def create_task(self, dict_params):
        # {'TITLE': 'Закупка приборов для лаборатории', 'PRIORITY': 'Отсутствует', 'RESPONSIBLE_ID': 'Владимир Иванов', 'DEADLINE': '20.01.24'}
        if len(dict_params) <= 0:
            return None
        for param, value in dict_params.items():
            if param == "RESPONSIBLE_ID":
                dict_params[param] = self.user_name_to_id(value)

        dict_params["STATUS"] = "2"
        if "RESPONSIBLE_ID" not in dict_params:
            dict_params["RESPONSIBLE_ID"] = dict_params["CREATED_BY"]

        return self.but.call_api_method("tasks.task.add", {"fields": dict_params})["result"]

    def update_task(self, dict_params):
        # {'TITLE': 'Отсутствует', 'PRIORITY': 'Отсутствует', 'RESPONSIBLE_ID': 'Марина Александрова', 'DEADLINE': 'Отсутствует', 'taskId': 90}
        if len(dict_params) <= 0:
            return None
        taskId = dict_params["taskId"]
        del dict_params["taskId"]

        res = self.but.call_api_method("tasks.task.update", {"taskId": taskId, "fields": dict_params})["result"]
        if res is None:
            raise ValueError
        return res

    def show_tasks(self, dict_params):
        list_tasks = self.but.call_api_method('tasks.task.list', {
            "select": ['ID', 'TITLE', 'STATUS'], "filter": dict_params})["result"]["tasks"]

        attach = []
        for task in list_tasks:
            del task["group"]
            del task["subStatus"]

            attach.append({"MESSAGE": str(task)})
            attach.append({"DELIMITER": {"SIZE": "200", "COLOR": "#a6a6a6"}})

        return attach

    def report(self, _):
        list_tasks = self.but.call_api_method('tasks.task.list', {"select": ["ID", "TITLE", "CREATED_BY",
            "CREATED_DATE", "STATUS", "DEADLINE", "RESPONSIBLE_ID"]})["result"]["tasks"]

        attach = []
        weekly_report = self.generate_weekly_report(list_tasks)
        for user_report in weekly_report:
            attach.append({"MESSAGE": f"Сотрудник: {user_report['name']}"})
            attach.append({"MESSAGE": f"Выполненные задачи: {user_report['completed']}"})
            attach.append({"MESSAGE": f"Невыполненные задачи: {user_report['uncompleted']}"})
            attach.append({"MESSAGE": "Список задач:"})

            for task in user_report['tasks']:
                attach.append({"MESSAGE": f"- {task['title']} (Дата создания: {task['createdDate']}, Статус: {task['status']})"})
            attach.append({"DELIMITER": {"SIZE": "200", "COLOR": "#a6a6a6"}})

        return attach

    def user_name_to_id(self, name):
        res = self.but.call_api_method('user.get')["result"]

        users = {}
        for i in res:
            full_name = i["LAST_NAME"] + " " + i["NAME"]
            users[full_name] = i["ID"]

        return users[name]

    @staticmethod
    def generate_weekly_report(tasks):
        # Определяем текущую дату и время с временной зоной
        now = datetime.now(timezone.utc)
        start_date = now - timedelta(days=7)
        end_date = now

        user_tasks = {}
        for task in tasks:
            responsible_id = task['responsibleId']
            if responsible_id not in user_tasks:
                user_tasks[responsible_id] = {
                    'name': task['responsible']['name'],
                    'completed': 0,
                    'uncompleted': 0,
                    'tasks': []
                }

            # Преобразуем строку даты задачи в datetime с учетом временной зоны
            task_date = datetime.strptime(task['createdDate'], '%Y-%m-%dT%H:%M:%S%z')

            # Сравниваем offset-aware даты
            if start_date <= task_date <= end_date:
                if task['status'] == '5':
                    user_tasks[responsible_id]['completed'] += 1
                else:
                    user_tasks[responsible_id]['uncompleted'] += 1
                user_tasks[responsible_id]['tasks'].append({
                    'title': task['title'],
                    'createdDate': task['createdDate'],
                    'status': task['status']
                })

        report = []
        for user_id, user_data in user_tasks.items():
            report.append({
                'name': user_data['name'],
                'completed': user_data['completed'],
                'uncompleted': user_data['uncompleted'],
                'tasks': user_data['tasks']
            })

        return report
