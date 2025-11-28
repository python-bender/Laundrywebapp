from django import forms
from .models import OrderItem, ClothType

class NewOrderForm(forms.Form):
    # dynamic: we will create inputs for each cloth type on template
    pass
