import traceback
from django.shortcuts import render
import settings

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.vendors.telegram import Bot

from .utils import get_id_chat, clear_updates


@main_auth(on_cookies=True)
def send_tg_message(request):
    if request.method == 'POST':
        try:
            chat_id = get_id_chat(request.POST.get("init_message"))

            bot = Bot(token=settings.TG_TOKEN)
            bot.send_message(text=request.POST.get("message"), chat_id=chat_id)
        except ValueError as e:
            return render(request, 'tg_message.html', {"error": e.args[0]})
        except:
            print(traceback.format_exc())
    clear_updates()
    return render(request, 'tg_message.html', {"error": None})