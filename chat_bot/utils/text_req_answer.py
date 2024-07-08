from chat_bot.utils.api_methods import *
from chat_bot.utils.intent_detection import IntentDetection
from chat_bot.utils.tasks_bitrix import TasksBitrix



class TextReqAnswer:
    def __init__(self, but, input_message, user_id, chat_id):
        self.but = but
        self.input_message = input_message
        self.user_id = user_id
        self.chat_id = chat_id

        self.option = f"wait_next_{self.user_id}_{self.chat_id}"

        self.intent_detector = IntentDetection()
        self.tasks_bitrix = TasksBitrix(but)

    def success_extract(self, choice, dict_params):
        bitrix_methods = {
            Choices.CREATE: self.tasks_bitrix.create_task,
            Choices.UPDATE: self.tasks_bitrix.update_task,
            Choices.SHOW: self.tasks_bitrix.show_tasks,
            Choices.REPORT: self.tasks_bitrix.report,
        }
        messages = {
            Choices.CREATE: "создана",
            Choices.UPDATE: "обновлена",
            Choices.SHOW: "показана",
            Choices.REPORT: "отчет",
        }

        result = bitrix_methods[choice](dict_params)

        if choice == Choices.SHOW or choice == Choices.REPORT:
            bot_send_attach(self.but, messages[choice], result, self.chat_id)
        else:
            bot_send_message(self.but, messages[choice], self.chat_id)

        if not self.but.call_api_method("app.option.set", {"options": {self.option: "-"}})["result"]:
            raise ValueError("app.option.set")

    def error_extract(self, user_choice):
        message = "Для того, чтобы " + user_choice + ", введите параметры"
        bot_send_message(self.but, message, self.chat_id)
        res = self.but.call_api_method("app.option.set", {"options": {self.option: user_choice}})["result"]
        if not res:
            raise ValueError("app.option.set")

    def process_user_request(self):

        user_choice = self.but.call_api_method("app.option.get", {"option": self.option})["result"]
        if user_choice == "-" or user_choice == '':
            user_choice = self.intent_detector.detect_intent(self.input_message)

        match user_choice:
            case "ошибка":
                self.success_extract("ошибка, введите другой запрос")
            case "создать задачу":
                dict_params = self.intent_detector.extract_parameters_create(self.input_message)
                if dict_params:
                    dict_params["CREATED_BY"] = self.user_id
                    self.success_extract(Choices.CREATE, dict_params)
                else:
                    self.error_extract(user_choice)
            case "изменить задачу":
                dict_params = self.intent_detector.extract_parameters_update(self.input_message)
                if dict_params:
                    self.success_extract(Choices.UPDATE, dict_params)
                else:
                    self.error_extract(user_choice)
            case "показать задачи":
                dict_params = self.intent_detector.extract_parameters_show(self.input_message)
                if dict_params:
                    self.success_extract(Choices.SHOW, dict_params)
                else:
                    self.error_extract(user_choice)
            case "сгенерировать отчет":
                self.success_extract(Choices.REPORT, {})
            case _:
                self.success_extract("я не понял вас")
