from django.http import HttpResponse

from chat_bot.utils.chat_keyboard import ChatKeyboard
from chat_bot.utils.text_req_answer import TaskRequestHandler
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from time import time


@main_auth(on_start=True)
def chat_bot(request):
    start = time()
    but = request.bitrix_user_token

    input_message = request.POST.get('data[PARAMS][MESSAGE]')
    dialog_id = request.POST.get('data[PARAMS][DIALOG_ID]')
    user_id = request.POST.get('data[PARAMS][FROM_USER_ID]')
    event = request.POST.get('event')

    req_handler = TaskRequestHandler(but, input_message, user_id, dialog_id)
    chat_keyboard = ChatKeyboard(but)

    if event == "ONIMBOTMESSAGEADD":
        req_handler.process_user_request()

    try:
        chat_keyboard.bot_send_keyboard('Выберите функцию', dialog_id)
    except:
        pass
    print((time() - start)*1000, "ms")
    return HttpResponse(status=204)
