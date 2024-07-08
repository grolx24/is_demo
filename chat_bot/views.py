import json

from django.http import HttpResponse

from chat_bot.utils.text_req_answer import TextReqAnswer
from chat_bot.utils.api_methods import *
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


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
    # register_commands()


@main_auth(on_start=True)
def commands_main(request):
    pass


@main_auth(on_start=True)
def chat_bot(request):
    but = request.bitrix_user_token

    input_message = request.POST.get('data[PARAMS][MESSAGE]')
    dialog_id = request.POST.get('data[PARAMS][DIALOG_ID]')
    user_id = request.POST.get('data[PARAMS][FROM_USER_ID]')
    chat_id = request.POST.get('data[PARAMS][CHAT_ID]')
    event = request.POST.get('event')  # 'ONIMBOTMESSAGEADD'


    answer = TextReqAnswer(but, input_message, user_id, dialog_id)

    if event == "ONIMBOTMESSAGEADD":
        answer.process_user_request()

    return HttpResponse("200")


@main_auth(on_start=True)
def command_intent(request):  # 'COMMAND': "tasksBot",
    but = request.bitrix_user_token

    input_message = request.POST.get('data[PARAMS][MESSAGE]')
    dialog_id = request.POST.get('data[PARAMS][DIALOG_ID]')
    user_id = request.POST.get('data[PARAMS][FROM_USER_ID]')
    chat_id = request.POST.get('data[PARAMS][CHAT_ID]')
    event = request.POST.get('event')  # 'ONIMBOTMESSAGEADD'
    command_params = request.POST.get('data[COMMAND][72][COMMAND_PARAMS]')  # 72
    message_id = request.POST.get('data[PARAMS][MESSAGE_ID]')
    command = request.POST.get('data[COMMAND][72][COMMAND]')

    if event == "ONIMCOMMANDADD":
        if command_params == "":
            bot_send_keyboard(but, dialog_id=dialog_id)
        elif command_params == "create":
            keyboard_create(but, "напишите параметры задачи", message_id)
        elif command_params == "update":
            keyboard_update(but, "напишите параметры задачи", message_id)
        elif command_params == "show":
            keyboard_show(but, "напишите параметры задач", message_id)
        elif command_params == "report":
            TextReqAnswer(but, input_message, user_id, dialog_id).success_extract(Choices.REPORT, {})
        elif command_params.startswith("choice"):
            choice = param_to_choice(command_params)
            ind = command_params.find("_")
            dict_params = json.loads(command_params[ind + 1:])
            if choice == Choices.CREATE:
                dict_params["CREATED_BY"] = user_id
            TextReqAnswer(but, input_message, user_id, dialog_id).success_extract(choice, dict_params)

    return HttpResponse("200")


def param_to_choice(param):
    if param.startswith("choicecreate"):
        return Choices.CREATE
    elif param.startswith("choiceupdate"):
        return Choices.UPDATE
    elif param.startswith("choiceshow"):
        return Choices.SHOW
    elif param.startswith("choicereport"):
        return Choices.REPORT


"""
bot_send_message(but, "[send=текст]название кнопки[/send] - мгновенная отправка текста боту", "chat"+chat_id)
bot_send_attach(but, "message", "chat"+chat_id)
bot_send_keyboard(but, "message", "chat" + chat_id)
bot_send_message(but, "[put=/search]Введите строку поиска[/put]", "chat" + chat_id)
return HttpResponse("200")
"""
