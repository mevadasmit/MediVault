from django import forms
from orders.models import Order
from constant import (STATUS, FILED_STATUS,PENDING,DELIVERED,CANCELLED)


class SupplierOrderUpdateForm(forms.ModelForm):
    """
        Form for updating the status of an order by a supplier.
        Provides a dropdown to select the order status.
    """
    status = forms.ChoiceField(
        choices=[(PENDING,PENDING),(DELIVERED, DELIVERED), (CANCELLED, CANCELLED)],
        label=STATUS,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Order
        fields = [FILED_STATUS]