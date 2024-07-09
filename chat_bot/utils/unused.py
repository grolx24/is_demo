from django.conf import settings


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