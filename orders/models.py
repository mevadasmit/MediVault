from base.models import CustomBaseModel , BaseModel
from django.db import models
from main_admin.models import Inventory, InventoryManager
from users.models import CustomUser


class Cart(BaseModel):
    """
        Represents a shopping cart for an inventory manager.
        Stores the manager, total products, and total price of items in the cart.
    """
    inventory_manager = models.ForeignKey(InventoryManager, on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField(default=0,null=True,blank=True)
    total_price = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return f"Cart For  {self.inventory_manager.user.first_name} -  {self.inventory_manager.organization.name}"


class CartItem(BaseModel):
    """
        Represents an item in a shopping cart.
        Stores the cart, inventory item, supplier, quantity, and total price.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , related_name='cart_items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={"role__name": "Supplier"}
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.IntegerField()


    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.inventory.unit_price
        super().save(*args, **kwargs)
        self.update_cart_totals()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_cart_totals()

    def update_cart_totals(self):
        cart_items = self.cart.cart_items.all()
        self.cart.total_price = sum(item.total_price for item in cart_items)
        self.cart.total_products = cart_items.values("inventory").distinct().count()  # Count unique inventory items
        self.cart.save()

    def __str__(self):
        return f"{self.inventory.name} - {self.quantity}"


class Order(CustomBaseModel):
    """
        Represents an order placed by an inventory manager.
        Stores information about the supplier, manager, total price, products, and status.
    """
    supplier = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={"role__name": "Supplier"}
    )
    inventory_manager = models.ForeignKey(InventoryManager,on_delete=models.CASCADE , related_name='orders')
    total_price = models.IntegerField()
    total_products = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Delivered", "Delivered") , ("Cancelled", "Cancelled")],
        default="Pending"
    )

    def update_totals(self):
        self.total_price = sum(item.total_price for item in self.order_items.all())
        self.total_products = self.order_items.count()
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.total_products = 0
        super().save(*args, **kwargs)

    def order_count(self):
        return self.inventory_manager.orders.count()

    def __str__(self):
        return f"Order {self.id} - {self.inventory_manager.user.first_name}"


class OrderItem(BaseModel):
    """
        Represents an item within an order.
        Stores the order, inventory item, quantity, unit price, and total price.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE , related_name='order_items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.IntegerField()
    total_price = models.IntegerField()

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.order.update_totals()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_totals()

    def __str__(self):
        return f"{self.inventory.name} - {self.quantity}"


