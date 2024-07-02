from django import forms
from django.forms import DateInput

from .models.call_info_model import CallInfo
from .models.choices_models import NumberChoicesShow, NumberChoicesCreateCRM


class CallInfoForm(forms.ModelForm):
    class Meta:
        model = CallInfo
        fields = ['user_phone', 'user_id', 'phone_number', 'call_date',
                  'type', 'add_to_chat', 'file', 'show_call', 'create_crm',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_phone'].label = 'Внутренний номер пользователя'
        self.fields['user_id'].label = 'Идентификатор пользователя'
        self.fields['phone_number'].label = 'Номер телефона'
        self.fields['call_date'].label = 'Дата/время звонка'
        self.fields['type'].label = 'Тип звонка'
        self.fields['add_to_chat'].label = 'Уведомление сотрудника Б24'
        self.fields['file'].label = 'Файл с записью звонка (.mp3)'
        self.fields['call_date'].widget = DateInput(
            attrs={'type': 'datetime-local'})
        self.fields['show_call'].label = 'Показать звонок'
        self.fields['create_crm'].label = 'Создать CRM сущность связанную со звонком'
        self.fields['show_call'].initial = NumberChoicesShow.one
        self.fields['create_crm'].initial = NumberChoicesCreateCRM.zero
