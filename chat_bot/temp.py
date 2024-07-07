from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from chat_bot.utils.api_methods import *
from chat_bot.utils.intent_detection import *
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True)
def echo_command(request):
    # 'data[COMMAND][32][COMMAND_PARAMS]'
    return HttpResponse("hi")


@main_auth(on_start=True)
def register_bot_view(request):
    but = request.bitrix_user_token
    register_bot(but)
    # .EmptyCookie
    # request.POST.get('data[PARAMS][MESSAGE]')
    # 'data[PARAMS][DIALOG_ID]' 'data[PARAMS][TO_USER_ID]' 'data[PARAMS][CHAT_ID]'
    # POST.get('ONIMBOTMESSAGEADD')
    # 'data[COMMAND][32][COMMAND]'  'echo'
    # 'ONIMCOMMANDADD'
    # 'data[COMMAND][32][MESSAGE_ID]'


@main_auth(on_start=True)
def init_bot(request):
    but = request.bitrix_user_token
    register_bot(but)
    register_commands()


@main_auth(on_start=True)
def commands(request):
    pass


def analyze(input_message):
    """
    Запрос к gpt
    Определить к какому варианту относится
    варианты: создать, изменить, показать одну, показать несколько с фильтром, установить уведомления, сделать отчет
    """
    pass


@main_auth(on_start=True)
def chat_bot(request):
    but = request.bitrix_user_token

    input_message = request.POST.get('data[PARAMS][MESSAGE]')
    dialog_id = request.POST.get('data[PARAMS][DIALOG_ID]')
    user_id = request.POST.get('data[PARAMS][FROM_USER_ID]')
    chat_id = request.POST.get('data[PARAMS][CHAT_ID]')
    event = request.POST.get('event')  # 'ONIMBOTMESSAGEADD'
    """
    bot_send_message(but, "[send=текст]название кнопки[/send] - мгновенная отправка текста боту", "chat"+chat_id)
    bot_send_attach(but, "message", "chat"+chat_id)
    bot_send_keyboard(but, "message", "chat" + chat_id)
    bot_send_message(but, "[put=/search]Введите строку поиска[/put]", "chat" + chat_id)
    return HttpResponse("200")
    """
    """
    user_choice = option.get
if user_choice == "-"
user_choice = IntentDetectionMin
match(user_choice)
create
...
error
if user_choice == "create..."
match(user_choice)
create
...
error
получается от if option.get == "-"
зависит только нужно ли вызывать 
user_choice = IntentDetectionMin
"""
    option = f"wait_next_{user_id}_{chat_id}"
    user_choice = but.call_api_method("app.option.get", {"option": option})["result"]
    match user_choice:
        case "-":
            user_choice = IntentDetection(input_message)

            if user_choice == "ошибка":
                bot_send_message(but, "ошибка, введите другой запрос", "chat" + chat_id)
                but.call_api_method("app.option.set", {"options": {option: "-"}})
            else:
                message = "Для того, чтобы " + user_choice + ", введите параметры\n"
                bot_send_message(but, message, "chat" + chat_id)

                res = but.call_api_method("app.option.set", {"options": {option: user_choice}})["result"]
                if res is not True:
                    raise ValueError("app.option.set")
        case "создать задачу":
            dict_params = NER_create(input_message)
            create_task(but, dict_params, user_id, input_message)
            bot_send_message(but, "создана", "chat" + chat_id)
            res = but.call_api_method("app.option.set", {"options": {option: "-"}})["result"]
        case "изменить задачу":
            dict_params = NER_update(input_message)
            update_task(but, dict_params)
            bot_send_message(but, "изменена", "chat" + chat_id)
            res = but.call_api_method("app.option.set", {"options": {option: "-"}})["result"]
        case "показать задачи":
            dict_params = NER_show(input_message)
            tasks = show_tasks(but, dict_params)
            for i in tasks:
                bot_send_message(but, str(i), "chat" + chat_id)
            res = but.call_api_method("app.option.set", {"options": {option: "-"}})["result"]
        case "сгенерировать отчет":
            # dict_params = NER_gen_rep(input_message)
            gen_report()
            bot_send_message(but, "сгенерирован", "chat" + chat_id)
            res = but.call_api_method("app.option.set", {"options": {option: "-"}})["result"]
        case _:
            raise ValueError("default")

    return HttpResponse("200")


"""
Уведомления и напоминания:
Бот отправляет уведомления о важных изменениях в задачах, таких как изменение статуса, назначение новой задачи или приближающийся срок выполнения.
Возможность установки напоминаний о задачах на определенное время.

Интеграция с календарем:
Возможность интеграции с календарем Bitrix24 для автоматического создания событий на основе задач.
Уведомления о предстоящих событиях и сроках выполнения задач.

Отчеты и статистика:
Генерация отчетов о выполнении задач за определенный период.
Просмотр статистики по задачам, включая количество завершенных задач, задачи в процессе и другие метрики.
"""
