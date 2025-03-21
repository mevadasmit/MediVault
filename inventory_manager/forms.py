from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from main_admin.models import  Inventory
from users.models import CustomUser, Role
from inventory_manager.models import Nurse, InventoryManager
from django.utils.crypto import get_random_string
from base.utils import send_registration_email
from constant import (FILED_FIRST_NAME, FIELD_LAST_NAME, FIELD_EMAIL, FIELD_PHONE_NUMBER, REQUEST, POST, VALIDATION_ERROR_IM,
                      NURSE, SUPPLIER, SELECT_SUPPLIER , SELECT_AVAILABLE_SUPPLIER , FIELD_SUPPLIER)

class NurseRegistrationForm(forms.ModelForm):
    """
        Form for registering a new nurse.
        Handles creating a new user with the Nurse role and associated Nurse entry.
    """
    class Meta:
        model = CustomUser
        fields = [FILED_FIRST_NAME, FIELD_LAST_NAME, FIELD_EMAIL, FIELD_PHONE_NUMBER]

        REQUIRED_FIELDS = [FILED_FIRST_NAME, FIELD_LAST_NAME,FIELD_PHONE_NUMBER]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop(REQUEST, None)  # Get request object
        super().__init__(*args, **kwargs)

        # Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = POST
        self.helper.add_input(Submit("submit", "Register Nurse"))

        for field in self.fields:
            self.fields[field].required = True

        if self.request and self.request.user.is_authenticated:
            # Get the logged-in user
            inventory_manager = InventoryManager.objects.filter(user=self.request.user).first()

            if not inventory_manager:
                raise ValueError(VALIDATION_ERROR_IM)

            # Store Inventory Manager & Organization in the form for validation
            self.inventory_manager = inventory_manager
            self.organization = inventory_manager.organization

    def save(self, commit=True):
        """
            Save the new nurse user and create a Nurse entry.
            Generates a random password, sets it for the user, and sends a registration email.
        """
        # Create the Nurse user
        nurse_user = CustomUser.objects.create(
            first_name=self.cleaned_data[FILED_FIRST_NAME],
            last_name=self.cleaned_data[FIELD_LAST_NAME],
            email=self.cleaned_data[FIELD_EMAIL],
            phone_number=self.cleaned_data[FIELD_PHONE_NUMBER],
            role=Role.objects.get(name=NURSE),  # Automatically assign role
        )

        password = get_random_string(10)  # Generate a password
        nurse_user.set_password(password)  # Set generated password
        nurse_user.first_time_login = True
        nurse_user.save()
        send_registration_email(nurse_user,password)

        # Create Nurse entry
        return Nurse.objects.create(
            user=nurse_user,
            inventory_manager=self.inventory_manager,  # Auto-assign Inventory Manager
            organization=self.organization,  # Auto-assign Organization
            created_by=self.request.user,
            updated_by=self.request.user,
        )

class NurseUpdateForm(forms.ModelForm):
    """
        Form for updating nurse information.
        Updates the user details and the associated Nurse entry's updated_by field.
    """
    class Meta:
        model = CustomUser
        fields = [FILED_FIRST_NAME, FIELD_LAST_NAME, FIELD_EMAIL, FIELD_PHONE_NUMBER]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop(REQUEST, None)
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True

        self.helper = FormHelper()
        self.helper.form_method = POST
        self.helper.add_input(Submit("submit", "Update Nurse"))

    def save(self, commit=True):
        nurse_user = super().save(commit=True)
        if self.request:
            Nurse.objects.filter(user_id=nurse_user).update(updated_by=self.request.user)
        return nurse_user

class SupplierSelectionFrom(forms.ModelForm):
    """
        Form for selecting a supplier for an inventory item.
        Provides a dropdown to choose from available suppliers.
    """
    supplier = forms.ModelChoiceField(
        queryset = CustomUser.objects.filter(role__name = SUPPLIER),
        label=SELECT_SUPPLIER,
        required=True,
        empty_label=SELECT_AVAILABLE_SUPPLIER,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Inventory
        fields = [FIELD_SUPPLIER]
