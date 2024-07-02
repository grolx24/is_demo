from integration_utils.bitrix24.exceptions import BitrixApiError
from django.conf import settings
from dateutil.parser import parse

CALLS_TYPES = {
    '1': 'Исходящий звонок',
    '2': 'Входящий звонок',
    '3': 'Входящий с перенаправлением (на мобильный или стационарный телефон)',
    '4': 'Обратный звонок',
    None: 'Нет данных'
}


# Возвращает id всех юзеров
def get_users(but):
    users = but.call_list_method('user.get', {'ADMIN_MODE': True})
    return {user['ID']: user for user in users}


# Возвращает необработанные звонки с прикрепленными файлами
def get_calls_with_files(but, last_call_id):
    filter_dict = {'FILTER': {'>ID': last_call_id}}
    calls = but.call_list_method('voximplant.statistic.get', filter_dict)
    if len(calls) < 1:
        return {}

    but.call_api_method('app.option.set', {'options': {'last_call_id': calls[-1]["ID"]}})
    return {call.get('RECORD_FILE_ID'): call
            for call in calls if call.get('RECORD_FILE_ID')}


# генерирует сообщение для отправки в тг
def create_message(call, users):
    start_time = parse(call['CALL_START_DATE'])
    msg = f"{CALLS_TYPES[call['CALL_TYPE']]}\n" \
          f"{start_time.strftime('%d.%m.%Y %H:%M:%S')}\n" \
          f"Номер {call['PHONE_NUMBER']} \n" \
          f"Менеджер: {get_user_name(users, call['PORTAL_USER_ID'])}\n" \
          f"{call['CRM_ENTITY_TYPE'].capitalize() if call['CRM_ENTITY_TYPE'] else 'Нет связанной crm сущности'}: "
    return msg


# Добавляет в итоговое сообщение информацию о связанной crm сущности, если таковая имеется.
def add_entity_url(but, call):
    if call.get('CRM_ENTITY_TYPE'):
        url = f"https://{settings.APP_SETTINGS.portal_domain}/crm/{call['CRM_ENTITY_TYPE'].lower()}/details/{call['CRM_ENTITY_ID']}/"
        try:
            entity = but.call_list_method(f"crm.{call['CRM_ENTITY_TYPE'].lower()}.get", {'ID': call['CRM_ENTITY_ID'].lower()})
            name = f"{entity['LAST_NAME']} {entity['NAME']}".strip() if (entity.get('NAME') or entity.get('LAST_NAME')) else entity['TITLE']
        except BitrixApiError as e:
            if 'Not found' in str(e):
                name = f"{call['CRM_ENTITY_TYPE']} с id = {call['CRM_ENTITY_ID']}"
            else:
                raise
        return f"[{name}]\n({url})\n"
    return ''


# Возвращает имена пользователей по id.
def get_user_name(users, user_id):
    user = users[user_id]
    name = f"{user['LAST_NAME']} {user['NAME']}".strip()
    return f"{name}\n(https://{settings.APP_SETTINGS.portal_domain}/company/personal/user/{user_id}/)"
