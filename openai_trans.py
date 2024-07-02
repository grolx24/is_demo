import os

import openai
import requests

import settings
from settings import BASE_DIR

# Настройка прокси
proxies = {
    'http': 'http://EH9BCkyd:CfPdEkvk@46.232.26.62:62082',
    'https': 'http://EH9BCkyd:CfPdEkvk@46.232.26.62:62082'
}


def create_proxy_session(proxies):
    session = requests.Session()
    session.proxies.update(proxies)
    return session

session = create_proxy_session(proxies)

openai.requestssession = session

openai.api_key = settings.OPEN_AI_API_KEY

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "hello! how r u?"}
    ]
)

# Вывод ответа текстовой модели
print(response.choices[0].message['content'])
