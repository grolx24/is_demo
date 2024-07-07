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
    register_commands()


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
    command_params = request.POST.get('data[COMMAND][54][COMMAND_PARAMS]')
    command_params = request.POST.get('data[PARAMS][MESSAGE_ID]')

    if event == "ONIMBOTMESSAGEADD":
        answer = TextReqAnswer(but, input_message, user_id, dialog_id)
        answer.process_user_request()

    if event == "ONIMCOMMANDADD":
        pass

    return HttpResponse("200")

"""
bot_send_message(but, "[send=текст]название кнопки[/send] - мгновенная отправка текста боту", "chat"+chat_id)
bot_send_attach(but, "message", "chat"+chat_id)
bot_send_keyboard(but, "message", "chat" + chat_id)
bot_send_message(but, "[put=/search]Введите строку поиска[/put]", "chat" + chat_id)
return HttpResponse("200")
"""


@main_auth(on_start=True)
def echo_command(request):
    # 'data[COMMAND][32][COMMAND_PARAMS]'
    if request.POST.get('event') == 'ONIMCOMMANDADD':
        pass
    if request.POST.get('event') == 'ONIMCOMMANDADD':
        pass
    return HttpResponse("200")

