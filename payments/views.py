import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from .models import Payment, StatusChoice
from .forms import PaymentForm
from .utils.paystack import initialize_payment
from dotenv import load_dotenv
import os
import uuid


load_dotenv()


def index(request):
    return redirect('payment-initiate')


def initiate(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.reference = str(uuid.uuid4())
            payment.save()

            callback_url = request.build_absolute_uri(reverse('payment-verify'))

            paystack_response = initialize_payment(
                email=payment.email,
                amount=payment.amount * 100,
                reference=payment.reference,
                callback_url=callback_url
            )

            if paystack_response.get('status'):
                return redirect(paystack_response['data']['authorization_url'])

    else:
        form = PaymentForm(initial={'amount': 10000})
    return render(request, 'payments/create_payment.html', {
        'title': 'Payment Platform',
        'form': form,
        'paystack_public_key': os.environ.get('PAYSTACK_PUBLIC_KEY')
        })



def verify(request):
    reference = request.GET.get('reference')
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f'Bearer {os.environ.get('PAYSTACK_SECRET_KEY')}'
    }

    response = requests.get(url, headers=headers)
    payment_verify = response.json()

    if (payment_verify['status']) and (payment_verify['data']['status'] == 'success'):
        payment = Payment.objects.get(reference=reference)
        payment.status = StatusChoice.CONFIRMED
        payment.save()
        return HttpResponse('Payment Successful')

    return HttpResponse('Payment Failed!')