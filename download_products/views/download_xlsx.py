import os
import settings

from django.http import FileResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..utils.to_xlsx import save_file


@main_auth(on_cookies=True)
def download_xlsx(request):
    if request.method == 'POST':
        but = request.bitrix_user_token

        try:
            products = but.call_list_method('crm.product.list')
            users = but.call_list_method('user.get')

            file_path = os.path.join(settings.BASE_DIR, 'products.xlsx')
            save_file(products, users, file_path)

            file = open(file_path, 'rb')
            response = FileResponse(file)
            response['Content-Disposition'] = 'attachment; filename="example.xlsx"'
            return response

        except Exception as e:
            print(f"Error during file download: {e}")

    return render(request, 'load_xlsx.html')
