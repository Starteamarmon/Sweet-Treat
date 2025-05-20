from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['telegram_id', 'cake_name', 'weight', 'date']
        widgets = {
            'telegram_id': forms.HiddenInput(),
            'cake_name': forms.HiddenInput(),
            'weight': forms.HiddenInput(),  # управляется слайдером
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }