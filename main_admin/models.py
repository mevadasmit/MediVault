from django.db import models
from base.models import CustomBaseModel
from users.models import CustomUser
# Create your models here

class Organization(CustomBaseModel):
    """
        Stores information about an organization, including its name,
        address, and email.
    """
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class InventoryManager(CustomBaseModel):
    """
        Links a user to an organization as an inventory manager.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.organization.name} And IM : {self.user.first_name}"


class InventoryCategory(CustomBaseModel):
    """
        Stores the name of the category.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Inventory(CustomBaseModel):
    """
        Stores information about an inventory item, including its name,
        supplier, category, unit price, and reusability status.
    """
    name = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    inventory_category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE)
    unit_price = models.IntegerField(default=0)
    is_reusable = models.BooleanField(default=False)

    def __str__(self):
        return f"Product Name : {self.name}"


