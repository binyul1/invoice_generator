from django import forms
from .models import Customer, Invoice, Item
from django.forms import modelformset_factory


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description', 'quantity', 'price']

ItemFormSet = forms.inlineformset_factory(Invoice, Item, form=ItemForm, extra=1, can_delete=False)