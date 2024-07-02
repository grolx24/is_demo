from django import forms
from .models import EmployeeDepartmentSelection


class EmployeeDepartmentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDepartmentSelection
        fields = ['employee', 'department']

    def __init__(self, *args, **kwargs):
        employee_choices = kwargs.pop('employee_choices', [])
        department_choices = kwargs.pop('department_choices', [])

        super(EmployeeDepartmentForm, self).__init__(*args, **kwargs)

        self.fields['employee'] = forms.ChoiceField(choices=[('0', 'Все')], required=False, label='Сотрудник')
        self.fields['department'] = forms.ChoiceField(choices=[('0', 'Все')], required=False, label='Отдел')

        self.fields['employee'].choices = [('0', 'Все')] + employee_choices
        self.fields['department'].choices = [('0', 'Все')] + department_choices
