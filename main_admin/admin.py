from django.contrib import admin
from .models import Organization , InventoryManager , InventoryCategory , Inventory

# Register your models here.

admin.site.register(Organization)
admin.site.register(InventoryManager)
admin.site.register(InventoryCategory)
admin.site.register(Inventory)