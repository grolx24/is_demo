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

    def success_extract(self, message):
        bot_send_message(self.but, message, self.chat_id)
        res = self.but.call_api_method("app.option.set", {"options": {self.option: "-"}})["result"]
        if not res:
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
                    self.tasks_bitrix.create_task(dict_params, self.user_id, self.input_message)
                    self.success_extract("создана")
                else:
                    self.error_extract(user_choice)

            case "изменить задачу":
                dict_params = self.intent_detector.extract_parameters_update(self.input_message)
                if dict_params:
                    self.tasks_bitrix.update_task(dict_params)
                    self.success_extract("изменена")
                else:
                    self.error_extract(user_choice)

            case "показать задачи":
                dict_params = self.intent_detector.extract_parameters_show(self.input_message)
                if dict_params:
                    tasks = self.tasks_bitrix.show_tasks(dict_params)
                    for i in tasks:
                        bot_send_message(self.but, str(i), self.chat_id)
                    if self.but.call_api_method("app.option.set", {"options": {self.option: "-"}})["result"] is None:
                        raise ValueError("app.option.set")
                else:
                    self.error_extract(user_choice)

            case "сгенерировать отчет":
                # dict_params = NER_gen_rep(input_message)
                self.tasks_bitrix.gen_report()
                bot_send_message("сгенерирован", self.chat_id)
                if self.but.call_api_method("app.option.set", {"options": {self.option: "-"}})["result"] is None:
                    raise ValueError("app.option.set")
            case _:
                self.success_extract("я не понял вас")
