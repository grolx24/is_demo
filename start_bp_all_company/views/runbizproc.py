import asyncio

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms.select_bp import BPForm
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from ..models.companybp import CompanyBPModel


@main_auth(on_cookies=True)
def run_bizproc(request):
    success = None

    but = request.bitrix_user_token
    CompanyBPModel.find_all_bizprocs(but)

    if request.method == 'POST':
        form = BPForm(request.POST)
        if form.is_valid():
            companies_id = but.call_list_method('crm.company.list', {'select': ['ID']})
            cur_bp = form.cleaned_data['bp']
            results = asyncio.run(cur_bp.run_multiple_bp(but, companies_id))
            success = len(companies_id) - results.count(None)
    else:
        form = BPForm()
    return render(request, 'start_bp.html', context={'form': form, 'success': success})
