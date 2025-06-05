from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import BaseModel
from .manager import UserManager
from django.core.mail import send_mail
from django.conf import settings
from constant import (FIELD_EMAIL, FIELD_ROLE, FIELD_PHONE_NUMBER, FILED_FIRST_NAME, FIELD_LAST_NAME)
from base.utils import send_registration_email

class Role(BaseModel):
    """
        Represents a user role.
        Stores the name of the role (e.g., 'Admin', 'Nurse', 'Supplier').
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomUser(BaseModel, AbstractUser):
    """
        Represents a custom user model.
        Uses email as the username field and includes a role, phone number, and first-time login status.
    """
    username = None
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    first_time_login = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = FIELD_EMAIL
    REQUIRED_FIELDS = [FIELD_PHONE_NUMBER, FILED_FIRST_NAME, FIELD_LAST_NAME]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def send_registration_email(self, raw_password):
        """Sends a registration email using the utility function."""
        send_registration_email(self, raw_password)

    class Meta:
        ordering = ['-created_at']
