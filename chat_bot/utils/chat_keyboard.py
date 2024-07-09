import json
from datetime import datetime, timedelta
from enum import Enum


class Choices(Enum):
    CREATE = 1
    UPDATE = 2
    SHOW = 3
    REPORT = 4
    ERROR = 5


class ChatKeyboard:
    COMMAND = "tasksBot"
    BOT_ID = "26"  # Идентификатор чат-бота

    def __init__(self, but):
        self.but = but

    @staticmethod
    def end_of_week() -> str:
        current_date = datetime.now()
        days_until_end_of_week = 6 - current_date.weekday() if current_date.weekday() < 6 else 0
        end_of_week_date = current_date + timedelta(days=days_until_end_of_week)
        return end_of_week_date.strftime('%d.%m.%Y')

    @staticmethod
    def tomorrow() -> str:
        return (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')

    def last_five_tasks(self) -> str:
        tasks = self.but.call_api_method('tasks.task.list', {
            "select": ['ID'],
            "order": {'ID': 'desc'}
        })["result"]["tasks"]
        ids = [task["id"] for task in tasks][:5]
        return json.dumps(ids)

    def bot_send_attach(self, message: str, attach: str = '', dialog_id: str = "1") -> int:
        if not attach:
            attach = ''
            message = "не найдено"
        data = {
            "DIALOG_ID": dialog_id,
            "MESSAGE": message,
            "COLOR": "#29619b",
            "ATTACH": attach
        }
        message_id = self.but.call_api_method('imbot.message.add', data)
        return message_id

    def bot_send_message(self, message: str, dialog_id: str = "1") -> int:
        message_data = {
            'BOT_ID': self.BOT_ID,
            'DIALOG_ID': dialog_id,
            'MESSAGE': message,
            'ATTACH': '',
            'KEYBOARD': '',
            'MENU': '',
            'SYSTEM': 'N',
            'URL_PREVIEW': 'Y'
        }
        message_id = self.but.call_api_method('imbot.message.add', message_data)
        return message_id

    def bot_send_keyboard(self, message: str = "Нажмите на соответствующую кнопку", dialog_id: str = "1") -> int:
        data = {
            "DIALOG_ID": dialog_id,
            "MESSAGE": message,
            "COLOR": "#29619b",
            "KEYBOARD": [
                {"TEXT": "create", "COMMAND": self.COMMAND, "COMMAND_PARAMS": "create", "DISPLAY": "LINE",
                 "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
                {"TEXT": "update", "COMMAND": self.COMMAND, "COMMAND_PARAMS": "update", "DISPLAY": "LINE",
                 "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
                {"TEXT": "show", "COMMAND": self.COMMAND, "COMMAND_PARAMS": "show", "DISPLAY": "LINE",
                 "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
                {"TEXT": "report", "COMMAND": self.COMMAND, "COMMAND_PARAMS": "report", "DISPLAY": "LINE",
                 "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            ]
        }
        message_id = self.but.call_api_method('imbot.message.add', data)
        return message_id

    def keyboard_create(self, message_text: str, message_id: str) -> dict:
        param_prefix = "choicecreate_"
        params = [
            r'{"TITLE": "Закупить канц товары", "DESCRIPTION": "Закупить канцелярские товары"}',
            r'{"TITLE": "Подготовить годовой отчет", "DEADLINE": "' + self.end_of_week() + r'", "DESCRIPTION": "подготовить годовой отчет до конца недели"}',
            r'{"DEADLINE": "' + self.tomorrow() + '", "TITLE": "встретиться с заказчиком", "DESCRIPTION": "завтра встретиться с заказчиком"}'
        ]
        answer_data = {
            'COMMAND_ID': "72",
            'COMMAND': self.COMMAND,
            'MESSAGE_ID': message_id,
            'MESSAGE': message_text,
            'ATTACH': '',
            'MENU': '',
            'SYSTEM': 'N',
            'URL_PREVIEW': 'Y',
            'CLIENT_ID': '',
            "KEYBOARD": [
                {"TEXT": "закупить канц товары", "COMMAND": self.COMMAND,
                 "COMMAND_PARAMS": param_prefix + params[0], "DISPLAY": "LINE", "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
                {"TEXT": "подготовить годовой отчет до конца недели", "COMMAND": self.COMMAND,
                 "COMMAND_PARAMS": param_prefix + params[1], "DISPLAY": "LINE",
                 "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
                {"TEXT": "Завтра встретиться с заказчиком", "COMMAND": self.COMMAND,
                 "COMMAND_PARAMS": param_prefix + params[2], "DISPLAY": "LINE", "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            ]
        }
        result = self.but.call_api_method('imbot.command.answer', answer_data)
        return result

    def keyboard_update(self, message_text: str, message_id: str) -> dict:
        param_prefix = "choiceupdate_"
        params = [
            r'{"TITLE": "Закупить канц товары", "DESCRIPTION": "Закупить канцелярские товары"}',
            r'{"TITLE": "Подготовить годовой отчет", "DEADLINE": "' + self.end_of_week() + r'", "DESCRIPTION": "подготовить годовой отчет до конца недели"}',
        ]
        answer_data = {
            'COMMAND_ID': "72",
            'COMMAND': self.COMMAND,
            'MESSAGE_ID': message_id,
            'MESSAGE': message_text,
            'ATTACH': '',
            'MENU': '',
            'SYSTEM': 'N',
            'URL_PREVIEW': 'Y',
            'CLIENT_ID': '',
            "KEYBOARD": [
                {"TEXT": "у последней задачи передвинуть дедлайн на завтра", "COMMAND": self.COMMAND,
                 "COMMAND_PARAMS": "update_move dealine 1 day", "DISPLAY": "LINE",
                 "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
                {"TEXT": "завершить последнюю задачу", "COMMAND": self.COMMAND,
                 "COMMAND_PARAMS": "update_complete last task", "DISPLAY": "LINE",
                 "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            ]
        }
        result = self.but.call_api_method('imbot.command.answer', answer_data)
        return result

    def keyboard_show(self, message_text: str, message_id: str) -> dict:
        param_prefix = "choiceshow_"
        params = [
            r'{"ID": ' + self.last_five_tasks() + '}',
            r'{"STATUS": "2"}',
        ]
        answer_data = {
            'COMMAND_ID': "72",
            'COMMAND': self.COMMAND,
            'MESSAGE_ID': message_id,
            'MESSAGE': message_text,
            'ATTACH': '',
            'MENU': '',
            'SYSTEM': 'N',
            'URL_PREVIEW': 'Y',
            'CLIENT_ID': '',
            "KEYBOARD": [
                {"TEXT": "Показать последние 5 задач", "COMMAND": self.COMMAND, "COMMAND_PARAMS": param_prefix + params[0], "DISPLAY": "LINE",
                 "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
                {"TEXT": "Показать незавершенные задачи", "COMMAND": self.COMMAND, "COMMAND_PARAMS": param_prefix + params[1], "DISPLAY": "LINE",
                 "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            ]
        }
        result = self.but.call_api_method('imbot.command.answer', answer_data)
        return result
