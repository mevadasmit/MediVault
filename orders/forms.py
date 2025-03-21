from django import forms
from .models import CartItem, Inventory, Order
from constant import (SELECT_PRODUCT, QUANTITY, FIELD_QUANTITY, FIELD_INVENTORY, STATUS, FILED_STATUS ,
                      PENDING, CONFIRMED , CANCELLED )

class AddToCartForm(forms.Form):
    """
        Form for adding items to the cart.
        Allows users to select a product and specify the desired quantity.
    """

    inventory = forms.ModelChoiceField(
        queryset = Inventory.objects.all(),
        label = SELECT_PRODUCT,
        widget=forms.Select(attrs={'class':'form-control'}),
    )

    quantity = forms.IntegerField(
        label = QUANTITY,
        min_value = 1,
        initial = 1,
        widget=forms.NumberInput(attrs={'class':'form-control'}),
    )

    class Meta:
        model = CartItem
        fields = [FIELD_INVENTORY, FIELD_QUANTITY]

class OrderUpdateForm(forms.ModelForm):
    """
        Form for updating the status of an order.
        Provides a dropdown to select the order status.
    """
    status = forms.ChoiceField(
        choices= [(PENDING,PENDING),(CONFIRMED,CONFIRMED), (CANCELLED,CANCELLED)],
        label=STATUS,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Order
        fields = [FILED_STATUS]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields[FILED_STATUS].initial = self.instance.status

