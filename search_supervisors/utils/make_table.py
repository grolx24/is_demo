def table(user_dict, department_dict, selected_employee, selected_department):
    res = list()
    try:
        selected_department = int(selected_department)
    except ValueError:
        return res

    for user_id, user_info in user_dict.items():
        if selected_employee != '0' and user_id != selected_employee:
            continue
        for department in user_info['UF_DEPARTMENT']:
            if selected_department != 0 and department != selected_department:
                continue
            department = str(department)

            user_supervisor = dict()
            user_supervisor["employee"] = user_info['FULL_NAME']
            user_supervisor["dep_employee"] = department_dict[department]["NAME"]

            supervisors = user_info['SUPERVISORS']
            if len(supervisors) > 0:
                user_supervisor["supervisor"] = user_dict[supervisors[department]]["FULL_NAME"]
                user_supervisor["order"] = user_info['SUPERVISORS_ORDER'][department]
            else:
                user_supervisor["supervisor"] = "Нет руководителя"
                user_supervisor["order"] = "-"

            user_supervisor["ID"] = user_id

            res.append(user_supervisor)
    return res