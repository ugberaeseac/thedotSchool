import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Payment, StatusChoice
from .forms import PaymentForm
from .utils.paystack import initialize_payment
from .utils.email import send_success_email_with_resend
from dotenv import load_dotenv
import os
import uuid


load_dotenv()


def index(request):
    return HttpResponse('<h3> Welcome </h3>')


def initiate(request, name, email):
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
        
        form = PaymentForm(initial={'full_name': name, 'email': email, 'amount': 50})
    return render(request, 'payments/payment.html', {
        'title': 'Payment Platform',
        'form': form,
        'paystack_public_key': os.environ.get('PAYSTACK_PUBLIC_KEY')
        })



def verify(request):
    reference = request.GET.get('reference')
    if not reference:
        return redirect('payment-failed')

    payment = Payment.objects.filter(reference=reference).first()
    if not payment:
        return redirect('payment failed')
        
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f"Bearer {os.environ.get('PAYSTACK_SECRET_KEY')}"
    }

    response = requests.get(url, headers=headers)
    payment_verify = response.json()

    if (payment_verify['status']) and (payment_verify['data']['status'] == 'success'):
        payment = Payment.objects.get(reference=reference)
        payment.status = StatusChoice.CONFIRMED
        payment.save()
        
        return redirect('payment-success', reference=payment.reference)
    return redirect('payment-failed', reference=payment.reference)

def success(request, reference):
    payment = get_object_or_404(
        Payment,
        reference=reference,
        status=StatusChoice.CONFIRMED
    )

    discord_links = {
        'Introduction to Software Engineering': 'https://discord.gg/r4qQXvXY',
        'Frontend Web Development(REACT)': 'https://discord.gg/RZcNcF8Q',
        'Backend Web Development (Python)': 'https://discord.gg/yrd4NYAD',
        'Backend Web Development (Node.js)': 'https://discord.gg/sSec7TKZ'
    }

    discord = discord_links.get(payment.course)
    if not discord:
        return redirect('payment-failed')
    send_success_email_with_resend(payment, discord)
    return render(request, 'payments/success.html', {'discord': discord})


def failed(request, reference):
    payment = get_object_or_404(
    Payment,
    reference=reference,
    status=StatusChoice.FAILED
    )

    return render(request, 'payments/failed.html', { 'payment': payment })


