import requests
from dotenv import load_dotenv
import os

load_dotenv()

PAYSTACK_BASE_URL = 'https://api.paystack.co'


def initialize_payment(email, amount, reference, callback_url):
    url = f'{PAYSTACK_BASE_URL}/transaction/initialize'
    headers = {
        'Authorization': f'Bearer {os.environ.get('PAYSTACK_SECRET_KEY')}',
        'Content-Type': 'application/json'
    }

    data = {
        'email': email,
        'amount': amount,
        'reference': reference,
        'callback_url': callback_url
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()