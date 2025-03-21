from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, UpdateView,TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from main_admin.models import InventoryManager
from .models import Cart, CartItem, Order, OrderItem
from orders.forms import AddToCartForm, OrderUpdateForm
from django.views import View
from constant import (FIELD_QUANTITY, FILED_TOTAL_PRICE, ADDED_TO_CART_SUCCESS, HTTP_REFERER, ACTION, INCREASE,
                      DECREASE,ITEM_REMOVED, FIELD_INVENTORY, ORDER_CART, CART_ITEMS, CART, ORDER_CONFIRMATION,
                      CART_ITEMS_BY_SUPPLIER,CART_IS_EMPTY, PENDING, ORDER, ORDER_DETAILS, ORDER_ID,
                      ORDER_BY_CREATED, ORDERS, ORDER_LIST, INVENTORY_MANAGER, ORDER_UPDATE)



class AddToCartView(FormView):
    """
        View for adding an item to the cart.
        Handles the form submission and updates the cart totals.
    """
    form_class = AddToCartForm

    def form_valid(self, form):
        inventory_manager = get_object_or_404(InventoryManager, user=self.request.user)
        cart = get_object_or_404(Cart, inventory_manager=inventory_manager)

        inventory = form.cleaned_data[FIELD_INVENTORY]
        quantity = form.cleaned_data.get(FIELD_QUANTITY, 1)  # Default to 1 if not provided

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, inventory=inventory, supplier_id=inventory.supplier_id,
            defaults={FIELD_QUANTITY: quantity, FILED_TOTAL_PRICE: inventory.unit_price * quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.total_price = cart_item.quantity * inventory.unit_price
            cart_item.save()

        self.update_cart_totals(cart)

        messages.success(self.request, ADDED_TO_CART_SUCCESS.format(item_name=inventory.name))
        return HttpResponseRedirect(self.request.META.get(HTTP_REFERER, '/'))

    def update_cart_totals(self, cart):
        """
            Updates the cart totals (total price and total products).
            This method recalculates and updates the cart's total price and
            total number of products based on the current cart items.
        """
        cart_items = cart.cart_items.all()
        cart.total_price = sum(item.total_price for item in cart_items)
        cart.total_products = cart_items.count()
        cart.save()


class UpdateCartQuantityView(View):
    """
        View for updating the quantity of an item in the cart.
        Handles increasing or decreasing the quantity, and removing the item if the quantity becomes zero.
    """

    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__inventory_manager__user=request.user)

        action = request.POST.get(ACTION)
        if action == INCREASE:
            cart_item.quantity += 1
        elif action == DECREASE:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                messages.success(request, ITEM_REMOVED)
                cart_item.cart.total_products = cart_item.cart.cart_items.values(FIELD_INVENTORY).distinct().count()
                cart_item.cart.save()
                return redirect("view_cart")

        cart_item.total_price = cart_item.quantity * cart_item.inventory.unit_price
        cart_item.save()

        # Update cart totals
        cart = cart_item.cart
        cart.total_price = sum(item.total_price for item in cart.cart_items.all())
        cart.total_products = cart.cart_items.values(FIELD_INVENTORY).distinct().count()
        cart.save()

        return redirect("view_cart")


class RemoveFromCartView(View):
    """
        View for removing an item from the cart.
        Handles removing the specified item and updating cart totals.
    """
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__inventory_manager__user=request.user)
        cart = cart_item.cart

        cart_item.delete()

        cart.total_price = sum(item.total_price for item in cart.cart_items.all())
        cart.total_products = cart.cart_items.values(FIELD_INVENTORY).distinct().count()
        cart.save()

        messages.success(request, ITEM_REMOVED)
        return redirect("view_cart")


class CartView(ListView):
    """
        View for displaying the cart.
        Lists all items currently in the user's cart.
    """
    model = CartItem
    template_name = ORDER_CART
    context_object_name = CART_ITEMS

    def get_queryset(self):
        inventory_manager = get_object_or_404(InventoryManager, user=self.request.user)
        cart = get_object_or_404(Cart, inventory_manager=inventory_manager)
        return CartItem.objects.filter(cart=cart)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventory_manager = get_object_or_404(InventoryManager, user=self.request.user)
        context[CART] = get_object_or_404(Cart, inventory_manager=inventory_manager)
        return context


class OrderConfirmationView(TemplateView):
    """
        View for displaying order confirmation.
        Groups cart items by supplier and prepares the context for order creation.
    """
    template_name = ORDER_CONFIRMATION

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventory_manager = get_object_or_404(InventoryManager, user=self.request.user)
        cart = get_object_or_404(Cart, inventory_manager=inventory_manager)

        cart_items_by_supplier = {}
        for item in cart.cart_items.all():
            cart_items_by_supplier.setdefault(item.supplier, []).append(item)

        context[CART_ITEMS_BY_SUPPLIER] = cart_items_by_supplier
        context[CART] = cart
        return context


class OrderCreateView(View):
    """
        View for creating orders from the cart.
        Groups cart items by supplier and creates individual orders.
    """
    def post(self, request, *args, **kwargs):
        """
            Handles the POST request to create orders.
            Groups cart items by supplier and creates individual orders for each supplier.
            Clears the cart after order creation.
        """
        inventory_manager = get_object_or_404(InventoryManager, user=request.user)
        cart = get_object_or_404(Cart, inventory_manager=inventory_manager)

        if not cart.cart_items.exists():
            messages.warning(request, CART_IS_EMPTY)
            return redirect("view_cart")

        # Group cart items by supplier
        cart_items_by_supplier = {}
        for item in cart.cart_items.all():
            cart_items_by_supplier.setdefault(item.supplier, []).append(item)

        orders = []
        for supplier, items in cart_items_by_supplier.items():
            total_price = sum(item.total_price for item in items)
            total_products = len(items)

            order = Order.objects.create(
                inventory_manager=inventory_manager,
                supplier=supplier,
                total_price=total_price,
                total_products=total_products,
                created_by=request.user,
                updated_by=request.user,
                status=PENDING,
            )
            orders.append(order)

            order_items = [
                OrderItem(
                    order=order,
                    inventory=item.inventory,
                    quantity=item.quantity,
                    unit_price=item.inventory.unit_price,
                    total_price=item.total_price,
                )
                for item in items
            ]
            OrderItem.objects.bulk_create(order_items)

            # Recalculate order total after OrderItems are created
            order.update_totals()

        # Clear Cart
        cart.cart_items.all().delete()
        cart.total_price = 0
        cart.total_products = 0
        cart.save()

        return redirect("order_list")


class OrderDetailView(DetailView):
    """
        View for displaying order details.
        Retrieves and displays the details of a specific order.
    """
    model = Order
    template_name = ORDER_DETAILS
    context_object_name = ORDER

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs.get(ORDER_ID), inventory_manager__user=self.request.user)


class OrderListView(ListView):
    """
        View for listing orders.
        Displays a paginated list of orders for the current inventory manager.
    """
    model = Order
    template_name = ORDER_LIST
    context_object_name = ORDERS
    paginate_by = 3

    def get_queryset(self):
        inventory_manager = get_object_or_404(InventoryManager, user=self.request.user)
        return Order.objects.filter(inventory_manager=inventory_manager).order_by(ORDER_BY_CREATED)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[INVENTORY_MANAGER] = get_object_or_404(InventoryManager, user=self.request.user)
        return context


class OrderUpdateView(UpdateView):
    """
        View for updating an order.
        Allows updating the status of an existing order.
    """
    model = Order
    form_class = OrderUpdateForm
    template_name = ORDER_UPDATE
    success_url = reverse_lazy("order_list")

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs.get(ORDER_ID))

    def form_valid(self, form):
        order = form.save(commit=False)
        order.updated_by = self.request.user
        order.save()
        return redirect("order_list")
