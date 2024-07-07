class TasksBitrix:
    def __init__(self, but):
        self.but = but

    def create_task(self, dict_params, created_by, input_message):
        # {'TITLE': 'Закупка приборов для лаборатории', 'PRIORITY': 'Отсутствует', 'RESPONSIBLE_ID': 'Владимир Иванов', 'DEADLINE': '20.01.24'}
        if len(dict_params) <= 0:
            return None
        for param, value in dict_params.items():
            if param == "RESPONSIBLE_ID":
                dict_params[param] = self.user_name_to_id(value)

        dict_params["STATUS"] = "2"
        dict_params["CREATED_BY"] = created_by
        dict_params["DESCRIPTION"] = input_message
        if "RESPONSIBLE_ID" not in dict_params:
            dict_params["RESPONSIBLE_ID"] = created_by

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
        if len(dict_params) <= 0:
            return None
        params = {"Идентификатор задачи": "ID", "Завершенность": "STATUS", "Название": "TITLE", "Крайний срок": "DEADLINE"}
        dict_params = {params[k]: v for k, v in dict_params.items()}
        dict_params["STATUS"] = "5" if dict_params["STATUS"] == "завершенные" else "2"

        list_tasks = self.but.call_api_method('tasks.task.list', {"select": ['ID', 'TITLE', 'STATUS'], "filter": dict_params})["result"]
        return list_tasks["tasks"]

    def gen_report(self):
        print("gen_report")

    def user_name_to_id(self, name):
        res = self.but.call_api_method('user.get')["result"]

        users = {}
        for i in res:
            full_name = i["LAST_NAME"] + " " + i["NAME"]
            users[full_name] = i["ID"]

        return users[name]
