import requests
from django.conf import settings

PAYSTACK_SECRET = settings.PAYSTACK_SECRET_KEY
PAYSTACK_INIT_URL = "https://api.paystack.co/transaction/initialize"
PAYSTACK_VERIFY_URL = "https://api.paystack.co/transaction/verify/"

def initialize_payment(email, amount, callback_url):
    headers = {'Authorization': f'Bearer {PAYSTACK_SECRET}'}
    data = {
        "email": email,
        "amount": int(amount * 100),  # kobo
        "callback_url": callback_url
    }
    resp = requests.post(PAYSTACK_INIT_URL, headers=headers, json=data)
    return resp.json()
