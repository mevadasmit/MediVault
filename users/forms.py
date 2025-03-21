from django import forms
from users.models import CustomUser, Role
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.crypto import get_random_string
from base.utils import send_registration_email
from constant import (SELECT_ROLE , FILED_FIRST_NAME , FIELD_LAST_NAME , FIELD_EMAIL, FIELD_PHONE_NUMBER, POST,
                      SUBMIT, REGISTER, OLD_PASSWORD , NEW_PASSWORD , CONFIRM_PASSWORD ,PASSWORD_NOT_MATCH)

class UserRegistrationForm(forms.ModelForm):
    """
        Form for registering new users.
        Includes fields for first name, last name, email, phone number, and role.
        Generates a random password and sends a registration email.
    """
    role_name = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label=SELECT_ROLE,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = [FILED_FIRST_NAME, FIELD_LAST_NAME, FIELD_EMAIL, FIELD_PHONE_NUMBER]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = POST
        self.helper.add_input(Submit(SUBMIT, REGISTER))

        for field in self.fields:
            self.fields[field].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data["role_name"]

        random_password = get_random_string(10)
        user.set_password(random_password)
        user.first_time_login = True

        if commit:
            user.save()
            send_registration_email(user,random_password)
        return user


class UserUpdateForm(forms.ModelForm):
    """
        Form for updating user information.
        Includes fields for first name, last name, email, and phone number.
    """
    class Meta:
        model = CustomUser
        fields = [FILED_FIRST_NAME,FIELD_LAST_NAME,FIELD_EMAIL,FIELD_PHONE_NUMBER]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True

class ChangePasswordForm(forms.Form):
    """
        Form for Changing password.
        Includes fields for old password , new password and confirm password with validation error.
    """

    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        old_password = self.cleaned_data.get(OLD_PASSWORD)
        new_password = self.cleaned_data.get(NEW_PASSWORD)
        confirm_password = self.cleaned_data.get(CONFIRM_PASSWORD)

        if old_password != confirm_password:
            raise forms.ValidationError(PASSWORD_NOT_MATCH)
        return new_password

