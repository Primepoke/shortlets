
from django.conf import settings
import requests
from requests.exceptions import RequestException, JSONDecodeError


class Paystack:
    PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co/"

    def verify_payment(self, ref, amount):
        path = f'transaction/verify/{ref}'
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SK}",
            "Content-Type": "application/json",
        }
        url = self.base_url + path

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            response_data = response.json()
            return response_data['status'], response_data['data']

        except RequestException as e:
            # Handle network-related issues
            print(f"Error during request: {e}")
            return False, None

        except JSONDecodeError as e:
            # Handle JSON decoding errors
            print(f"Error decoding JSON: {e}")
            return False, None







# class Paystack:
#     PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
#     base_url = "https://api.paystack.co/"

#     def verify_payment(self, ref, *args, **kwargs):
#         path = f'transaction/verify/{ref}'
#         headers = {
#             "Authorization": f"Bearer {self.PAYSTACK_SK}",
#             "Content-Type": "application/json",
#         }
#         url = self.base_url + path
#         response = requests.get(url, headers=headers)

#         if response.status_code == 200:
#             response_data = response.json()
#             return response_data['status'], response_data['data']

#         response_data = response.json()

#         return response_data['status'], response_data['message']
