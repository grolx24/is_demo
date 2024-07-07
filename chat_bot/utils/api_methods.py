import requests
from django.conf import settings


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


def register_commands():
    pass


def get_chat_id(but):
    chat_data = {
        'ENTITY_TYPE': 'CHAT',  # Идентификатор сущности
        'ENTITY_ID': "13",  # Числовой идентификатор сущности
        'BOT_ID': "20"  # Идентификатор чат-бота
    }
    result = but.call_api_method('imbot.chat.get', chat_data)

    return result


def bot_send_attach(but, message, dialog_id="1"):
    data = {
        "DIALOG_ID": dialog_id,
        "MESSAGE": message,
        "COLOR": "#29619b",
        "ATTACH": [
            {"MESSAGE": "API будет доступно [CHAT=52]текст[/CHAT] в обновлении [B]im 16.0.0[/B]"},
            {"DELIMITER": {"SIZE": "200", "COLOR": "#a6a6a6"}},
            {"USER": {"NAME": "Иван Иванов", "BOT_ID": "26"}},
        ]
    }
    message_id = but.call_api_method('imbot.message.add', data)
    return message_id


def bot_send_keyboard(but, message, dialog_id="1"):
    data = {
        "DIALOG_ID": dialog_id,
        "MESSAGE": "Нажмите на соответствующую кнопку",
        "COLOR": "#29619b",
        "KEYBOARD": [
            {"TEXT": "create", "COMMAND": "tasksBot", "COMMAND_PARAMS": "create", "DISPLAY": "LINE", },
            {"TEXT": "update", "COMMAND": "tasksBot", "COMMAND_PARAMS": "update", "DISPLAY": "LINE", },
            {"TEXT": "show", "COMMAND": "tasksBot", "COMMAND_PARAMS": "show", "DISPLAY": "LINE", },
            {"TEXT": "gen rep", "COMMAND": "tasksBot", "COMMAND_PARAMS": "report", "DISPLAY": "LINE", },
        ]
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


def register_command(but):
    command_data = {
        'BOT_ID': "44",  # Идентификатор чат-бота владельца команды
        'COMMAND': "tasksBot",  # Текст команды
        'COMMON': 'Y',  # Команда доступна во всех чатах
        'HIDDEN': 'N',  # Команда не скрытая
        'EXTRANET_SUPPORT': 'N',  # Команда недоступна пользователям Экстранет
        'CLIENT_ID': '',  # Идентификатор чат-бота (используется в режиме Вебхуков)
        'LANG': [
            {'LANGUAGE_ID': 'en', 'TITLE': 'Get echo message', 'PARAMS': 'some text'}  # Переводы команды
        ],
        'EVENT_COMMAND_ADD': "https://" + settings.APP_SETTINGS.app_domain + "/chat_bot/echo_command/"
        # Обработчик команд
    }
    result = but.call_api_method('imbot.command.register', command_data)

    print(result)
    return result


def answer_command(but):
    # 'data[COMMAND][32][COMMAND]'  'echo'
    # 'ONIMCOMMANDADD'
    answer_data = {
        'COMMAND_ID': 13,  # Идентификатор команды
        'COMMAND': 'echo',  # Название команды
        'MESSAGE_ID': 1122,  # Идентификатор сообщения
        'MESSAGE': 'answer text',  # Текст ответа
        'ATTACH': '',  # Вложение (необязательно)
        'MENU': '',  # Контекстное меню (необязательно)
        'SYSTEM': 'N',  # Системное сообщение (по умолчанию 'N')
        'URL_PREVIEW': 'Y',  # Преобразование ссылок в rich-ссылки (по умолчанию 'Y')
        'CLIENT_ID': '',  # Идентификатор чат-бота (для режима Вебхуков)
        "KEYBOARD": [
            {"TEXT": "create", "COMMAND": "tasksBot", "COMMAND_PARAMS": "create", "DISPLAY": "LINE", },
            {"TEXT": "update", "COMMAND": "tasksBot", "COMMAND_PARAMS": "update", "DISPLAY": "LINE", },
            {"TEXT": "show", "COMMAND": "tasksBot", "COMMAND_PARAMS": "show", "DISPLAY": "LINE", },
            {"TEXT": "gen rep", "COMMAND": "tasksBot", "COMMAND_PARAMS": "report", "DISPLAY": "LINE", },
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


def get_recent_history(but, chat_id):
    result = but.call_api_method('im.dialog.messages.get', {
        'DIALOG_ID': 'chat' + chat_id
    })

    return result


def analyze(message):
    pass


if __name__ == "__main__":
    pass
