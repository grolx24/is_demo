from django.http import HttpResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from save_companies_bd.models.company_model import Company


@main_auth(on_cookies=True)
def save_companies(request):
    but = request.bitrix_user_token
    if request.method == 'POST':
        num = Company.sync_companies(but)
        return HttpResponse(num)

    return render(request, 'save_companies_template.html')
