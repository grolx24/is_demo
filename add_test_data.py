import random
import string
from integration_utils.bitrix24.models.bitrix_user import BitrixUser


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def add_test_companies(but, num_companies=20):
    for _ in range(num_companies):
        company_name = generate_random_string(8) + " Company"
        company_data = {
            "fields": {
                "TITLE": company_name,
            }
        }
        response = but.call_api_method('crm.company.add', company_data)
        if response['result']:
            print(f"Company '{company_name}' успешно добавлена!")
        else:
            print(f"Ошибка при добавлении компании '{company_name}': {response['error_description']}")


if __name__ == "__main__":
    but = BitrixUser.objects.first()
    add_test_companies(but)
