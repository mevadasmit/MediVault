from django.contrib import admin

from orders.models import Order, OrderItem, CartItem,Cart

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
