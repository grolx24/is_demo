def find_supervisor(departments_dict, cache, current_dep='1', order=0):
    """Рекурсивая функция, осуществляющая поиск начальника, если в настоящем
    подразделении он не был найден."""

    # не распространяется на кешированные данные с более низких уровней дерева сотрудников
    if current_dep in cache:
        if order > cache[current_dep][1]:
            return (cache[current_dep][0], cache[current_dep][1] + order)
        elif order == cache[current_dep][1]:
            return cache[current_dep]

    department = departments_dict[current_dep]
    parent_exists = ('PARENT' in department)
    supervisor = department.get('UF_HEAD')
    supervisor_exists = (supervisor and (supervisor != '0'))

    if supervisor_exists:
        result = (department['UF_HEAD'], order)
    else:
        if not parent_exists:
            result = ("None", order)
        else:
            result = find_supervisor(departments_dict, cache, department['PARENT'], order + 1)

    cache[current_dep] = result
    return result


def search_manager(but):
    """Осуществляет поиск начальника для пользователя."""

    users = but.call_list_method('user.get')
    departments = but.call_list_method('department.get')

    #  Записываем в словарь юзеров только поля из массива user_fields и их значения.
    user_fields = ['NAME', 'LAST_NAME', 'SECOND_NAME', 'UF_DEPARTMENT']
    user_dict = {}
    for element in users:
        user_dict.update({element['ID']: {}})
        for field in user_fields:
            try:
                user_dict[element['ID']].update({field: element[field]})
            except KeyError:
                pass

    #  Записываем в словарь подразделения
    departments_dict = {}
    for element in departments:
        departments_dict.update({element['ID']: element})
        departments_dict[element['ID']].pop('ID')

    supervisor_cache = {}

    # Проходимся по всем юзерам, для каждого ищем руководителей.
    for user_id, user in user_dict.items():

        user.update({'SUPERVISORS': {}})
        user.update({'SUPERVISORS_ORDER': {}})
        # for department_id, departament_val in departments_dict.items():
        for department_id in user["UF_DEPARTMENT"]:
            department_id = str(department_id)
            departament_val = departments_dict[department_id]

            if departament_val.get('UF_HEAD') == user_id:
                if "PARENT" in departament_val:
                    department = departament_val['PARENT']
                    supervisor_id, order = find_supervisor(departments_dict, supervisor_cache, department, order=1)
                else:
                    supervisor_id = "None"

            else:
                if int(department_id) in user['UF_DEPARTMENT']:
                    department = department_id
                    supervisor_id, order = find_supervisor(departments_dict, supervisor_cache, department)
                else:
                    continue
            #  В функцию поиска передается родительское подразделение, если в текущем
            #   юзер является руководителем. В ином случае передается текущее.

            if supervisor_id != "None" and supervisor_id not in user['SUPERVISORS']:
                user['SUPERVISORS'][department_id] = supervisor_id
                user['SUPERVISORS_ORDER'][department_id] = order

    for user_id, user in user_dict.items():
        conj_str = ""
        for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
            try:
                conj_str += f"{user[key]} "
            except KeyError:
                pass
        conj_str += f"| ID: {user_id}"
        user.update({'FULL_NAME': conj_str})

    return user_dict, departments_dict
