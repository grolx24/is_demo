import locale


def sort_bitrix(but, field_id):
    user_field_list = but.call_api_method("crm.company.userfield.list", {
        "order": {"SORT": "ASC"},
        "filter": {"ID": field_id}
    })["result"][0]["LIST"]

    locale.setlocale(locale.LC_ALL, '')  # ('Russian_Russia', '1251')

    def sort_key(item):
        return locale.strxfrm(item["VALUE"])  # преобразует строку в формат, подходящий для сравнения с использованием правил сортировки текущей локали.

    sorted_data = sorted(user_field_list, key=sort_key)
    for index, company in enumerate(sorted_data):
        company["SORT"] = index + 1

    but.call_api_method("crm.company.userfield.update", {"ID": field_id, "FIELDS": {"LIST": sorted_data}})