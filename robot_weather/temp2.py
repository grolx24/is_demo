import json
import pprint as pp
import uuid

import requests


def getToken():
    request_uuid = uuid.uuid4()
    # Укажите данные для авторизации
    client_id = "f2c84f15-72c8-48f3-92da-ebab26fffc35"
    client_secret = "a14e7397-bc8d-4db3-9096-cb652409e30a"
    scope = "GIGACHAT_API_PERS"
    auth_data = "ZjJjODRmMTUtNzJjOC00OGYzLTkyZGEtZWJhYjI2ZmZmYzM1OmExNGU3Mzk3LWJjOGQtNGRiMy05MDk2LWNiNjUyNDA5ZTMwYQ=="

    # Задание параметров
    url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': f'{request_uuid}',  # Укажите нужный идентификатор запроса
        'Authorization': 'Basic ZjJjODRmMTUtNzJjOC00OGYzLTkyZGEtZWJhYjI2ZmZmYzM1OmExNGU3Mzk3LWJjOGQtNGRiMy05MDk2LWNiNjUyNDA5ZTMwYQ=='
    }
    data = {
        'scope': 'GIGACHAT_API_PERS'
    }

    # Выполнение POST-запроса
    response = requests.post(url, headers=headers, data=data, verify=False)
    resp_token = dict(response.json())["access_token"]
    return resp_token


def gchat(text):
    text2 = (f"{str(text)}\nПреобразуй эти' данные о погоде в человеческую форму. "
             f"Обобщи все до пары небольших предложений. Маловажные пункты отбрось, передай только суть. "
             f"Кроме этих предложений в ответе ничего не должно быть. В ответе только кириллица")

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    resp_token = getToken()
    data = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": text2
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1
    }
    payload = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {resp_token}'
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)
    pp.pprint(dict(json.loads(response.text)))

    res = dict(json.loads(response.text))
    return res["choices"][0]['message']['content']


if __name__ == "__main__":
    res = gchat("как делать запросы к gigachat?")
    print(res)
