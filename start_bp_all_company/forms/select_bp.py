from django import forms
from ..models.companybp import CompanyBPModel


class BPForm(forms.ModelForm):
    class Meta:
        model = CompanyBPModel
        fields = []

    bp = forms.ModelChoiceField(
        queryset=CompanyBPModel.objects.all(),
        to_field_name='process_id',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Не выбрано',
        label='БП'
    )
