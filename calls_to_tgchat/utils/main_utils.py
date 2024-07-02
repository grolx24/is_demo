import requests
import time

from settings import CALLS_TO_TGCHAT_SYNCH_PERIOD
from .secondary_utils import *


from integration_utils.vendors.telegram import Bot


def keep_call_info_synced(but, bot_token, calls_chat_id):
    """
    Вызывается в отдельном потоке, синхронизирует новые звонки
    """
    bot = Bot(token=bot_token)

    flag = "true"
    while flag == "true":
        try:
            last_call_id = but.call_api_method('app.option.get')['result']['last_call_id']
        except TypeError:
            # если вдруг в базе нет id последнего просмотренного звонка, берем последний звонок
            last_call_id = but.call_list_method('voximplant.statistic.get', {'SORT': 'ID', 'ORDER': 'DESC'}, limit=1)[0]['ID']

        send_calls(but, bot, calls_chat_id, last_call_id)

        flag = but.call_api_method('app.option.get')['result']['call_sync_flag']
        time.sleep(CALLS_TO_TGCHAT_SYNCH_PERIOD)


def export_calls_to_telegram(but, bot_token, calls_chat_id):
    bot = Bot(token=bot_token)

    done = send_calls(but, bot, calls_chat_id)
    return done


def send_calls(but, bot, calls_chat_id, last_checked_call_id='-1'):
    """
    1) Получаем словарь несинхронизированных звонков с прилепленной записью разговора
    2) Получаем файлы звонков (главарь с метаинформацией) из п.1
    3) Отправляем в тг чат

    """
    calls_with_files = get_calls_with_files(but, last_checked_call_id)
    if not calls_with_files:
        return False

    methods = []
    for file_id in calls_with_files.keys():
        methods.append(('disk.file.get', {'id': file_id}))
    call_files = but.batch_api_call(methods)

    users = get_users(but)
    for call_file in call_files.successes.values():
        call = calls_with_files[int(call_file['result']['ID'])]
        msg = create_message(call, users)
        msg += add_entity_url(but, call)
        file_content = requests.get(call_file['result']['DOWNLOAD_URL'])
        file_content = file_content.content
        bot.send_audio(
            chat_id=calls_chat_id,
            audio=file_content,
            filename=call_file['result']['NAME'],
            caption=msg,
        )

    return True
