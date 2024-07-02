from django.conf import settings
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from ..forms import EmployeeDepartmentForm
from ..utils.search_manager import search_manager
from ..utils.make_table import table


@main_auth(on_cookies=True)
def employee_list(request):
    but = request.bitrix_user_token
    user_dict, department_dict = search_manager(but)

    employee_choices = [(user_id, user['FULL_NAME']) for user_id, user in user_dict.items()]
    department_choices = [(dept_id, dept_info['NAME']) for dept_id, dept_info in department_dict.items()]

    selected_employee = '0'
    selected_department = '0'

    if not request.method == 'POST':
        form = EmployeeDepartmentForm(employee_choices=employee_choices, department_choices=department_choices)
    else:
        form = EmployeeDepartmentForm(request.POST, employee_choices=employee_choices, department_choices=department_choices)
        if form.is_valid():
            selection = form.save()
            selected_employee = selection.employee
            selected_department = selection.department

    context = {
        'table': table(user_dict, department_dict, selected_employee, selected_department),
        'form': form,
        "domain": settings.APP_SETTINGS.portal_domain,
    }

    return render(request, 'supervisor_departament.html', context)

