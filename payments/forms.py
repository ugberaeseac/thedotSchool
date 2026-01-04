from django import forms
from .models import Payment, StatusChoice


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('full_name', 'email', 'course', 'amount')
        widgets = {
        'amount': forms.TextInput(attrs={
            'type': 'text',          # Removes arrows by treating as text
            'inputmode': 'numeric',  # Still triggers numeric keypad on mobile
            'pattern': '[0-9]*',     # Basic browser validation for numbers
            'placeholder': '0.00'
        }),
    }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if Payment.objects.filter(email=email, status=StatusChoice.CONFIRMED).exists():
            raise forms.ValidationError('Payment already made for this user')
        return email


    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 10000:
            raise forms.ValidationError('Enter the required amount')
        return amount