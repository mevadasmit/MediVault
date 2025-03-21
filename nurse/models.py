from django.core.exceptions import ValidationError
from django.db import models
from base.models import CustomBaseModel , BaseModel
from inventory_manager.models import Nurse, OrgInventory
from main_admin.models import  Organization
from users.models import CustomUser
from constant import (VALIDATION_ERROR, )

class Request(BaseModel):
    STATUS_CHOICES = [("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")]

    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_emergency = models.BooleanField(default=False)
    total_items = models.IntegerField(default=0)
    approved_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="approved_requests", null=True, blank=True
    )
    rejected_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="rejected_requests", null=True, blank=True
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="updated_requests", null=True, blank=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    def update_totals(self):
        """Updates total requested items for the request."""
        self.total_items = self.items.aggregate(total=models.Sum("quantity_requested"))["total"] or 0
        self.save()


    def __str__(self):
        return f"{self.nurse.user.first_name} - {self.status}"

class RequestedItems(CustomBaseModel):
    request = models.ForeignKey(Request, related_name="items", on_delete=models.CASCADE)
    inventory = models.ForeignKey(OrgInventory, on_delete=models.CASCADE)
    quantity_requested = models.IntegerField()
    is_returned = models.BooleanField(default=False)

    def clean(self):
        """Validate available stock before requesting."""
        if self.quantity_requested > self.inventory.quantity_in_stock:
            raise ValidationError(VALIDATION_ERROR)

    def save(self, *args, **kwargs):
        """Handle stock updates correctly to prevent double update."""
        if self.pk is None:  # New Request
            self.inventory.quantity_in_stock -= self.quantity_requested
        elif self.is_returned and not RequestedItems.objects.get(id=self.id).is_returned:
            # Only update stock for the first time
            self.inventory.quantity_in_stock += self.quantity_requested

        self.inventory.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory.inventory.name} - {self.quantity_requested}"