from django import forms
from .models import Request, RequestedItems
from inventory_manager.models import OrgInventory
from constant import (EMERGENCY_REQUEST, FIELD_IS_EMERGENCY, INVENTORY ,FIELD_INVENTORY, FIELD_QUANTITY_REQUESTED,
                      )

class RequestForm(forms.ModelForm):
    """
        Form for creating a new request.
        This form allows users to create a new request and mark it as an emergency if needed.
    """
    is_emergency = forms.BooleanField(
        required=False,
        label=EMERGENCY_REQUEST,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Request
        fields = [FIELD_IS_EMERGENCY]


class RequestedItemForm(forms.ModelForm):
    """
        Form for requesting inventory items.
        This form allows users to request inventory items, specifying the inventory and quantity.
    """
    inventory = forms.ModelChoiceField(
        queryset=OrgInventory.objects.none(),
        label=INVENTORY,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = RequestedItems
        fields = [FIELD_INVENTORY, FIELD_QUANTITY_REQUESTED]

    @staticmethod
    def inventory_label(self, obj):
        return f"{obj.inventory.name} ({obj.quantity_in_stock} available)"

    def __init__(self, *args, **kwargs):
        nurse = kwargs.pop('nurse', None)
        super().__init__(*args, **kwargs)

        if nurse:
            self.fields[FIELD_INVENTORY].queryset = OrgInventory.objects.filter(organization=nurse.organization)
        self.fields[FIELD_INVENTORY].label_from_instance = self.inventory_label

