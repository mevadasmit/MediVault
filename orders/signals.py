from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory_manager.models import OrgInventory
from main_admin.models import InventoryManager
from orders.models import Cart, Order
from constant import (CONFIRMED, QUANTITY_IN_STOCK , CREATED_BY, UPDATED_BY)


@receiver(post_save, sender=InventoryManager)
def create_cart_for_inventory_manager(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(inventory_manager=instance)


@receiver(post_save, sender=Order)
def update_stock_on_confirmation(sender, instance, **kwargs):
    if instance.status == CONFIRMED:
        updated_by_user = instance.updated_by

        for order_item in instance.order_items.all():
            inventory = order_item.inventory
            organization = instance.inventory_manager.organization

            org_inventory, created = OrgInventory.objects.get_or_create(
                inventory=inventory,
                organization=organization,
                defaults={
                    QUANTITY_IN_STOCK : order_item.quantity,
                    CREATED_BY: updated_by_user,
                    UPDATED_BY: updated_by_user,
                }
            )

            if not created:
                org_inventory.quantity_in_stock += order_item.quantity
                org_inventory.updated_by = updated_by_user
                org_inventory.save()
