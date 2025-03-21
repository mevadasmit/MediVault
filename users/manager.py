from django.contrib.auth.base_user import BaseUserManager
from constant import (EMAIL_MUST_BE_SENDED, IS_STAFF, IS_ACTIVE, IS_SUPERUSER)

class UserManager(BaseUserManager):
    """
        Custom user manager for creating users and superusers.
        Uses email as the unique identifier instead of username.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(EMAIL_MUST_BE_SENDED)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        password = password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
            Creates a superuser with the given email and password.
            Sets is_staff, is_superuser, and is_active to True.
        """
        extra_fields.setdefault(IS_STAFF, True)
        extra_fields.setdefault(IS_SUPERUSER, True)
        extra_fields.setdefault(IS_ACTIVE, True)

        return self.create_user(email=email, password=password, **extra_fields)