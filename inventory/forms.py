from django import forms
from .models import StockRequest, StockRequestItem, FulfilledItemSerial

class StockRequestForm(forms.ModelForm):
    class Meta:
        model = StockRequest
        fields = ['warehouse']  # You can add more fields as per your requirement

class StockRequestItemForm(forms.ModelForm):
    class Meta:
        model = StockRequestItem
        fields = ['product', 'quantity']

class FulfilledItemSerialForm(forms.ModelForm):
    class Meta:
        model = FulfilledItemSerial
        fields = ['serial_number']
