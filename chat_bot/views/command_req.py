import json
from time import time

from django.http import HttpResponse

from chat_bot.utils.text_req_answer import TaskRequestHandler
from chat_bot.utils.chat_keyboard import Choices, ChatKeyboard
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True)
def command(request):  # 'COMMAND': "tasksBot",
    start = time()
    but = request.bitrix_user_token

    input_message = request.POST.get('data[PARAMS][MESSAGE]')
    dialog_id = request.POST.get('data[PARAMS][DIALOG_ID]')
    user_id = request.POST.get('data[PARAMS][FROM_USER_ID]')
    event = request.POST.get('event')
    command_params = request.POST.get('data[COMMAND][72][COMMAND_PARAMS]')
    message_id = request.POST.get('data[PARAMS][MESSAGE_ID]')

    option = f"wait_next_{user_id}_{dialog_id}"
    chat_keyboard = ChatKeyboard(but)

    if event == "ONIMCOMMANDADD":
        match command_params:
            case "":
                chat_keyboard.bot_send_keyboard(dialog_id=dialog_id)
            case "create":
                chat_keyboard.keyboard_create("напишите параметры задачи", message_id)
                but.call_api_method("app.option.set", {"options": {option: "создать задачу"}})
            case "update":
                chat_keyboard.keyboard_update("напишите параметры задачи", message_id)
                but.call_api_method("app.option.set", {"options": {option: "изменить задачу"}})
            case "show":
                chat_keyboard.keyboard_show("напишите параметры задач", message_id)
                but.call_api_method("app.option.set", {"options": {option: "показать задачи"}})
            case "report":
                TaskRequestHandler(but, input_message, user_id, dialog_id).success_extract(Choices.REPORT, {})
                but.call_api_method("app.option.set", {"options": {option: "сгенерировать отчет"}})
            case _ if command_params.startswith("choice"):
                choice = param_to_choice(command_params)
                ind = command_params.find("_")
                dict_params = json.loads(command_params[ind + 1:])
                if choice == Choices.CREATE:
                    dict_params["CREATED_BY"] = user_id
                TaskRequestHandler(but, input_message, user_id, dialog_id).success_extract(choice, dict_params)
                chat_keyboard.bot_send_keyboard('Выберите функцию', dialog_id)

    print((time() - start)*1000, "ms")
    return HttpResponse(status=204)


def param_to_choice(param):
    match param:
        case _ if param.startswith("choicecreate"):
            return Choices.CREATE
        case _ if param.startswith("choiceupdate"):
            return Choices.UPDATE
        case _ if param.startswith("choiceshow"):
            return Choices.SHOW
        case _ if param.startswith("choicereport"):
            return Choices.REPORT


"""
bot_send_message(but, "[send=текст]название кнопки[/send] - мгновенная отправка текста боту", "chat"+chat_id)
bot_send_attach(but, "message", "chat"+chat_id)
bot_send_keyboard(but, "message", "chat" + chat_id)
bot_send_message(but, "[put=/search]Введите строку поиска[/put]", "chat" + chat_id)
return HttpResponse("200")
"""
