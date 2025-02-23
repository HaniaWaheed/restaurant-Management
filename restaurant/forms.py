from django import forms
from .models import Order
from .models import ReturnRequest, CustomerContact
from .models import Payment

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['order', 'return_reason']

class ContactForm(forms.ModelForm):
    class Meta:
        model = CustomerContact
        fields = ['order', 'contact_type', 'message']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'readonly': True})
        }        