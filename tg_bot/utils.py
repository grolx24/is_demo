import json

import requests
import settings


def get_id_chat(init_message):
    url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/getUpdates"

    resp = requests.get(url)
    if resp.status_code == 200:
        json_resp = json.loads(resp.text)

        if len(json_resp["result"]) < 1:
            raise ValueError("Боту не было отправлено никаких сообщений")

        messages_list = json_resp["result"]
        for message in messages_list:
            if message["message"]["text"] == init_message:
                return message["message"]["chat"]["id"]

        raise ValueError("Боту не было отправлено указанное сообщение")
    raise requests.exceptions.RequestException()


def clear_updates():
    url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        json_resp = response.json()
        if "result" in json_resp and json_resp["result"]:
            last_update_id = json_resp["result"][-1]["update_id"]
            clear_url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/getUpdates?offset={last_update_id + 1}"
            requests.get(clear_url)


if __name__ == "__main__":
    chat_id = get_id_chat("привет")
    print(chat_id)
