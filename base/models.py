from django.conf import settings
from django.db import models
import uuid
from constant import (USER_PROVIDE)

class BaseModel(models.Model):
    """
        Abstract base model with common fields.
        Provides a UUID primary key, created_at, and updated_at timestamps.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomBaseModel(BaseModel):
    """
        Abstract base model with created_by and updated_by fields.
        Extends BaseModel and adds foreign keys for tracking user modifications.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name="%(class)s_created", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name="%(class)s_updated", null=True, blank=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
            Override the save method to automatically populate created_by and updated_by.
            Requires a 'user' keyword argument to be passed when creating a new instance.
        """
        if not (user := kwargs.pop('user', None)) and not self.pk:
            raise ValueError(USER_PROVIDE)
        elif user and not self.created_by:
            self.created_by = user
        elif user:
            self.updated_by = user
        super().save(*args, **kwargs)






