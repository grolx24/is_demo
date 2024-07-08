import json

import requests
from django.conf import settings

from enum import Enum

from datetime import datetime, timedelta

COMMAND = "tasksBot"


class Choices(Enum):
    CREATE = 1
    UPDATE = 2
    SHOW = 3
    REPORT = 4
    ERROR = 5


def chat_add(but):
    chat_data = {
        'TYPE': 'CHAT',  # Тип чата
        'TITLE': 'Мой новый закрытый чат',  # Заголовок
        'DESCRIPTION': 'Очень важные события',  # Описание
        'COLOR': 'PINK',  # Цвет
        'MESSAGE': 'Добро пожаловать!',  # Первое сообщение
        'USERS': ["1", "12"],  # Участники
        #     'AVATAR': '/* base64 image */',  # Аватар в base64 формате
        'ENTITY_TYPE': 'CHAT',  # Идентификатор сущности
        'ENTITY_ID': "13",  # Числовой идентификатор сущности
        'OWNER_ID': "1",  # Идентификатор владельца
        'BOT_ID': "20"  # Идентификатор бота
    }

    # Пример преобразования изображения в base64 (если требуется)
    # with open("path_to_image.jpg", "rb") as image_file:
    #     encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    #     chat_data['AVATAR'] = encoded_image

    result = but.call_api_method('imbot.chat.add', chat_data)
    print(result)

    return result


def get_chat_id(but):
    chat_data = {
        'ENTITY_TYPE': 'CHAT',  # Идентификатор сущности
        'ENTITY_ID': "13",  # Числовой идентификатор сущности
        'BOT_ID': "20"  # Идентификатор чат-бота
    }
    result = but.call_api_method('imbot.chat.get', chat_data)

    return result


def bot_send_attach(but, message, attach, dialog_id="1"):
    if not attach:
        attach = ''
        message = "не найдено"
    data = {
        "DIALOG_ID": dialog_id,
        "MESSAGE": message,
        "COLOR": "#29619b",
        "ATTACH": attach
    }
    message_id = but.call_api_method('imbot.message.add', data)
    return message_id


def bot_send_message(but, message, dialog_id="1"):
    message_data = {
        'BOT_ID': "26",  # Идентификатор чат-бота
        'DIALOG_ID': dialog_id,  # Идентификатор диалога
        'MESSAGE': message,  # Текст сообщения
        'ATTACH': '',  # Вложение (необязательно)
        'KEYBOARD': '',  # Клавиатура (необязательно)
        'MENU': '',  # Контекстное меню (необязательно)
        'SYSTEM': 'N',  # Системное сообщение
        'URL_PREVIEW': 'Y'  # Преобразование ссылок в rich-ссылки
    }
    message_id = but.call_api_method('imbot.message.add', message_data)

    return message_id


def end_of_week():
    current_date = datetime.now()
    days_until_end_of_week = 6 - current_date.weekday() if current_date.weekday() < 6 else 0
    end_of_week_date = current_date + timedelta(days=days_until_end_of_week)
    formatted_end_of_week_date = end_of_week_date.strftime('%d.%m.%Y')
    return formatted_end_of_week_date


def tomorrow():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_formatted = tomorrow.strftime('%d.%m.%Y')
    return tomorrow_formatted


def last_five_tasks(but):
    tasks = but.call_api_method('tasks.task.list', {
        "select": ['ID'],
        "order": {'ID': 'desc'}})["result"]["tasks"]
    ids = [el["id"] for el in tasks][:5]
    return json.dumps(ids)


def register_command(but):
    command_data = {
        'BOT_ID': "26",  # Идентификатор чат-бота владельца команды
        'COMMAND': "tasksBot",  # Текст команды
        'COMMON': 'Y',  # Команда доступна во всех чатах
        'HIDDEN': 'N',  # Команда не скрытая
        'EXTRANET_SUPPORT': 'N',  # Команда недоступна пользователям Экстранет
        'CLIENT_ID': '',  # Идентификатор чат-бота (используется в режиме Вебхуков)
        'LANG': [
            {'LANGUAGE_ID': 'en', 'TITLE': 'Get echo message', 'PARAMS': 'intent'}  # Переводы команды
        ],
        'EVENT_COMMAND_ADD': "https://" + settings.APP_SETTINGS.app_domain + "/chat_bot/echo_command/"
        # Обработчик команд
    }
    result = but.call_api_method('imbot.command.register', command_data)

    print(result)
    return result


def bot_send_keyboard(but, message="Нажмите на соответствующую кнопку", dialog_id="1"):
    data = {
        "DIALOG_ID": dialog_id,
        "MESSAGE": message,
        "COLOR": "#29619b",
        "KEYBOARD": [
            {"TEXT": "create", "COMMAND": COMMAND, "COMMAND_PARAMS": "create", "DISPLAY": "LINE",
             "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            {"TEXT": "update", "COMMAND": COMMAND, "COMMAND_PARAMS": "update", "DISPLAY": "LINE",
             "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            {"TEXT": "show", "COMMAND": COMMAND, "COMMAND_PARAMS": "show", "DISPLAY": "LINE",
             "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            {"TEXT": "report", "COMMAND": COMMAND, "COMMAND_PARAMS": "report", "DISPLAY": "LINE",
             "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
        ]
    }
    message_id = but.call_api_method('imbot.message.add', data)
    return message_id


def keyboard_create(but, message_text, message_id):
    param_prefix = "choicecreate_"
    params = [
        r'{"TITLE": "Закупить канц товары", "DESCRIPTION": "Закупить канцелярские товары"}',
        r'{"TITLE": "Подготовить годовой отчет", "DEADLINE": "' + end_of_week() + r'", "DESCRIPTION": "подготовить годовой отчет до конца недели"}',
        r'{"DEADLINE": "' + tomorrow() + '", "TITLE": "встретиться с заказчиком", "DESCRIPTION": "завтра встретиться с заказчиком"}'
    ]

    answer_data = {
        'COMMAND_ID': "72",  # Идентификатор команды
        'COMMAND': 'tasksBot',  # Название команды
        'MESSAGE_ID': message_id,  # Идентификатор сообщения
        'MESSAGE': message_text,  # Текст ответа
        'ATTACH': '',  # Вложение (необязательно)
        'MENU': '',  # Контекстное меню (необязательно)
        'SYSTEM': 'N',  # Системное сообщение (по умолчанию 'N')
        'URL_PREVIEW': 'Y',  # Преобразование ссылок в rich-ссылки (по умолчанию 'Y')
        'CLIENT_ID': '',  # Идентификатор чат-бота (для режима Вебхуков)
        "KEYBOARD": [
            {"TEXT": "закупить канц товары", "COMMAND": COMMAND,
             "COMMAND_PARAMS": param_prefix + params[0], "DISPLAY": "LINE", "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            {"TEXT": "подготовить годовой отчет до конца недели", "COMMAND": COMMAND,
             "COMMAND_PARAMS": param_prefix + params[1], "DISPLAY": "LINE",
             "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            {"TEXT": "Завтра встретиться с заказчиком", "COMMAND": COMMAND,
             "COMMAND_PARAMS": param_prefix + params[2], "DISPLAY": "LINE", "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
        ]
    }
    result = but.call_api_method('imbot.command.answer', answer_data)
    return result


def keyboard_update(but, message_text, message_id):
    param_prefix = "choiceupdate_"
    params = [
        r'{"TITLE": "Закупить канц товары", "DESCRIPTION": "Закупить канцелярские товары"}',
        r'{"TITLE": "Подготовить годовой отчет", "DEADLINE": "' + end_of_week() + r'", "DESCRIPTION": "подготовить годовой отчет до конца недели"}',
    ]
    answer_data = {
        'COMMAND_ID': "72",  # Идентификатор команды
        'COMMAND': 'tasksBot',  # Название команды
        'MESSAGE_ID': message_id,  # Идентификатор сообщения
        'MESSAGE': message_text,  # Текст ответа
        'ATTACH': '',  # Вложение (необязательно)
        'MENU': '',  # Контекстное меню (необязательно)
        'SYSTEM': 'N',  # Системное сообщение (по умолчанию 'N')
        'URL_PREVIEW': 'Y',  # Преобразование ссылок в rich-ссылки (по умолчанию 'Y')
        'CLIENT_ID': '',  # Идентификатор чат-бота (для режима Вебхуков)
        "KEYBOARD": [
            {"TEXT": "у последней задачи передвинуть дедлайн на завтра", "COMMAND": COMMAND,
             "COMMAND_PARAMS": "update_move dealine 1 day", "DISPLAY": "LINE",
             "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            {"TEXT": "завершить последнюю задачу", "COMMAND": COMMAND,
             "COMMAND_PARAMS": "update_complete last task", "DISPLAY": "LINE",
             "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
        ]
    }
    result = but.call_api_method('imbot.command.answer', answer_data)
    return result


def keyboard_show(but, message_text, message_id):
    param_prefix = "choiceshow_"
    params = [
        r'{"ID": ' + last_five_tasks(but) + '}',
        r'{"STATUS": "2"}',
    ]
    answer_data = {
        'COMMAND_ID': "72",  # Идентификатор команды
        'COMMAND': 'tasksBot',  # Название команды
        'MESSAGE_ID': message_id,  # Идентификатор сообщения
        'MESSAGE': message_text,  # Текст ответа
        'ATTACH': '',  # Вложение (необязательно)
        'MENU': '',  # Контекстное меню (необязательно)
        'SYSTEM': 'N',  # Системное сообщение (по умолчанию 'N')
        'URL_PREVIEW': 'Y',  # Преобразование ссылок в rich-ссылки (по умолчанию 'Y')
        'CLIENT_ID': '',  # Идентификатор чат-бота (для режима Вебхуков)
        "KEYBOARD": [
            {"TEXT": "Показать последние 5 задач", "COMMAND": COMMAND, "COMMAND_PARAMS": param_prefix + params[0], "DISPLAY": "LINE",
             "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
            {"TEXT": "Показать незавершенные задачи", "COMMAND": COMMAND, "COMMAND_PARAMS": param_prefix + params[1], "DISPLAY": "LINE",
             "BG_COLOR": "#29619b", "TEXT_COLOR": "#fff"},
        ]
    }
    result = but.call_api_method('imbot.command.answer', answer_data)
    return result


def register_bot(request):
    but = request.bitrix_user_token
    # Данные для регистрации бота
    bot_data = {
        'CODE': 'newbot',  # Строковой идентификатор бота, уникальный в рамках вашего приложения (обяз.)
        'TYPE': 'B',  # Тип, B – чат-бот, ответы поступают сразу, O – чат-бот для Открытых линий, S – чат-бот с
        # повышенными привилегиями (supervisor)
        'EVENT_HANDLER': "https://" + settings.APP_SETTINGS.app_domain + "/chat_bot/main",
        # Ссылка на обработчик событий, поступивших от сервера - см. Обработчики событий ниже (обяз).
        'OPENLINE': 'Y',  # Включение режима поддержки Открытых линий, можно не указывать, если TYPE = 'O'
        'CLIENT_ID': '',  # Строковой идентификатор, используется только в режиме Вебхуков
        'PROPERTIES': {  # Личные данные чат-бота (обяз.)
            'NAME': 'NewBot',  # Имя чат-бота (обязательное одно из полей NAME или LAST_NAME)
            'LAST_NAME': '',  # Фамилия (обязательное одно из полей NAME или LAST_NAME)
            'COLOR': 'GREEN',  # Цвет для мобильного приложения
            'EMAIL': 'test@test.ru',
            # E-mail для связи. НЕЛЬЗЯ использовать e-mail, дублирующий e-mail реальных пользователей
            'PERSONAL_BIRTHDAY': '2016-03-11',  # День рождения в формате YYYY-mm-dd
            'WORK_POSITION': 'Лучший сотрудник',  # Занимаемая должность, используется как описание чат-бота
            'PERSONAL_WWW': 'http://test.ru',  # Ссылка на сайт
            'PERSONAL_GENDER': 'F',
            # Пол, допустимые значения M – мужской, F – женский, пусто, если не требуется указывать
            'PERSONAL_PHOTO': '/* base64 image */',  # Аватар - base64
        }
    }

    # Регистрация бота
    response = but.call_api_method('imbot.register', bot_data)
    return response


if __name__ == "__main__":
    pass
