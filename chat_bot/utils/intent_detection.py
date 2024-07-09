import json
import requests
from chat_bot.models.intent_detection_history import IntentDetectionHistory
from settings import CHAD_API_KEY


class IntentDetection:
    BASE_URL = 'https://ask.chadgpt.ru/api/public/gpt-3.5'

    def __init__(self, api_key=CHAD_API_KEY):
        self.api_key = api_key

    def _send_request(self, prompt, input_message, goal):
        try:
            history_record = IntentDetectionHistory.objects.get(input_message=input_message, goal=goal)
            print("use bd")
            return history_record.intent_response
        except IntentDetectionHistory.DoesNotExist:
            print("DoesNotExist")

        request_json = {
            "message": f"{prompt}\nСообщение пользователя: {input_message}",
            "temperature": 0.1,
            "api_key": self.api_key
        }
        response = requests.post(url=self.BASE_URL, json=request_json)
        resp_json = response.json()

        if not resp_json.get("is_success"):
            raise ValueError("Failed to get a successful response from the API")

        intent_response = resp_json["response"]

        IntentDetectionHistory.objects.create(input_message=input_message, intent_response=intent_response, goal=goal)

        return intent_response

    def detect_intent(self, input_message):
        prompt = (
            "Ты — умный ассистент, который помогает пользователям управлять задачами в Bitrix24. "
            "Ты должен определить только тип функции, которую пользователь хочет запросить: "
            "создать задачу, изменить задачу, показать задачи, сгенерировать отчет или ошибка. "
            "Игнорируй любые переданные параметры. В ответе должен быть только один из этих вариантов и ничего лишнего. "
            "Пример запроса и ответа: "
            "Запрос: Добавь новую задачу 'Запуск рекламной кампании' на следующую пятницу для Иванова Ивана. "
            "Ответ: создать задачу. "
            "Пример запроса и ответа: "
            "Запрос: привет, как дела? "
            "Ответ: ошибка"
        )
        return self._send_request(prompt, input_message, "intent")

    def extract_parameters_create(self, input_message):
        params = {"Название": "TITLE", "Приоритет": "PRIORITY", "Исполнитель": "RESPONSIBLE_ID", "Крайний срок": "DEADLINE"}
        prompt = (
            "Ты — умный ассистент, который помогает пользователям управлять задачами в Bitrix24. "
            "Твоя задача — разобрать ответ пользователя и выбрать из него параметры для создания задачи. "
            "Возможные параметры: Название, Приоритет, Исполнитель, Крайний срок. "
            "В ответе ты должен вернуть только json с параметрами и ничего кроме этого. "
            "Порядок параметров всегда один. При отсутствии значения не выводишь параметр. \n"
            "Пример запроса: Добавь новую задачу 'Запуск рекламной кампании' с дедлайном 06.07.24 для Иванова Ивана. "
            "Пример ответа: { Название: Запуск рекламной кампании, Исполнитель: Иванов Иван, Крайний срок: 06.07.24 }"
        )
        dict_res = json.loads(self._send_request(prompt, input_message, "create"))
        dict_params = {params[key]: val for key, val in dict_res.items()}
        dict_params["DESCRIPTION"] = input_message

        return dict_params

    def extract_parameters_update(self, input_message):
        params = {"Название": "TITLE", "Приоритет": "PRIORITY", "Исполнитель": "RESPONSIBLE_ID", "Крайний срок": "DEADLINE", "Идентификатор задачи": "taskId", "Статус": "STATUS"}
        prompt = (
            "Ты — умный ассистент, который помогает пользователям управлять задачами в Bitrix24. "
            "Твоя задача — разобрать ответ пользователя и выбрать из него параметры для изменения задачи. "
            "Возможные параметры: Название, Приоритет, Исполнитель, Крайний срок, Идентификатор задачи, статус. Статус может иметь одно из двух значений: завершенный или незавершенный. "
            "В ответе ты должен вернуть только json с параметрами и ничего кроме этого. "
            "Порядок параметров всегда один. При отсутствии значения не выводишь параметр. \n"
            "Пример запроса: У задачи 19 передвинь дедлайн на 16.07.24. "
            "Пример ответа: { Крайний срок: 16.07.24, Идентификатор задачи: 19 }"
            "Пример запроса: Сделай задачу 132 завершенной. "
            "Пример ответа: { Статус: завершенный, Идентификатор задачи: 132 }"
        )
        dict_res = json.loads(self._send_request(prompt, input_message, "update"))
        res = {params[key]: val for key, val in dict_res.items()}
        if "STATUS" in res:
            res["STATUS"] = "5" if res["STATUS"] == "завершенный" else "2"
        return res

    def extract_parameters_show(self, input_message):
        params = {"Идентификатор задачи": "ID", "Завершенность": "STATUS", "Название": "TITLE", "Крайний срок": "DEADLINE"}
        prompt = (
            "Ты — умный ассистент, который помогает пользователям управлять задачами в Bitrix24. "
            "Твоя задача — разобрать ответ пользователя и выбрать из него параметры для фильтрации списка задач. "
            "Возможные параметры: Идентификатор задачи, Завершенность, Название, Крайний срок. "
            "В ответе ты должен вернуть только json с параметрами и ничего кроме этого. "
            "Порядок параметров всегда один. При отсутствии значения не выводишь параметр. \n"
            "Параметр Завершенность может иметь только одно из двух значений: незавершенные или завершенные. "
            "Пример запроса: покажи незавершенные задачи. "
            "Пример ответа: { \"Завершенность\": незавершенные } "
            "Пример запроса: покажи задачу с id 118. "
            "Пример ответа: { \"Идентификатор задачи\": 118 }"
        )

        dict_params = json.loads(self._send_request(prompt, input_message, "show"))
        dict_params = {params[k]: v for k, v in dict_params.items()}
        if "STATUS" in dict_params:
            dict_params["STATUS"] = "5" if dict_params["STATUS"] == "завершенные" else "2"
        return dict_params


if __name__ == "__main__":
    intent_detector2 = IntentDetection()

    res = intent_detector2.extract_parameters_update("для задачи 128 поменяй статус на завершенный")
    print(res)
