from django.apps import AppConfig
from constant import (INVENTORY_MANAGER)

class InventoryManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = INVENTORY_MANAGER
