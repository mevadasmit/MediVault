from django import forms
from users.models import CustomUser , Role
from .models import Organization
from constant import (FIELD_NAME,FIELD_ADDRESS,FIELD_EMAIL,INVENTORY_MANAGER, INVENTORY__MANAGER, SELECT_ROLE,
                      FILED_FIRST_NAME,FIELD_LAST_NAME,FIELD_PHONE_NUMBER,FIELD_ROLE)


class OrganizationRegistrationForm(forms.ModelForm):
    """
        Form for registering a new organization.
        This form allows users to register a new organization by providing
        the organization's name, address, email, and selecting an inventory manager.
    """
    inventory_manager = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role__name=INVENTORY__MANAGER), required=True ,
                                               widget = forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Organization
        fields = [FIELD_NAME , FIELD_ADDRESS , FIELD_EMAIL , INVENTORY_MANAGER]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True


class UserUpdateForm(forms.ModelForm):
    """
        Form for updating user information.
        This form allows updating a user's first name, last name,
        email, phone number, and role.
    """

    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label=SELECT_ROLE,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = [FILED_FIRST_NAME,FIELD_LAST_NAME,FIELD_EMAIL,FIELD_PHONE_NUMBER,FIELD_ROLE]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True
