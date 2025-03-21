from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView
from orders.models import Order ,OrderItem
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from supplier.forms import SupplierOrderUpdateForm
from django.db.models import Count, Q
from base.access import RoleRequiredMixin
from constant import (SUPPLIER, SUPPLIER_DASHBOARD, PENDING , CONFIRMED , CANCELLED, ID, SUPPLIER_MANAGEMENT, SUPPLIER_ORDERS,
                      ORDER_BY_CREATED, INVENTORY_MANAGER, FIELD_SUPPLIER, SUPPLIER_ORDER_DETAILS, ORDER, ORDER_ID, ORDER_ITEMS,
                      SUPPLIER_ORDER_UPDATE, )

class SupplierRequiredMixin(RoleRequiredMixin):
    """
    Mixin to restrict access to supplier users.
    """
    required_role = SUPPLIER

class IndexView(SupplierRequiredMixin,TemplateView):
    """
        Dashboard view for suppliers.
        Displays order counts categorized by status.
    """
    template_name = SUPPLIER_DASHBOARD

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = self.request.user

        order_counts = Order.objects.filter(supplier=supplier).aggregate(
            new_orders_count=Count(ID, filter=Q(status=PENDING)),
            delivery_confirmation_count=Count(ID, filter=Q(status=CONFIRMED)),
            delivery_cancelled_count=Count(ID, filter=Q(status=CANCELLED)),
        )

        context.update(order_counts)
        return context


class SupplierOrderListView(SupplierRequiredMixin, ListView):
    """
        View for listing a supplier's orders.
        Displays a list of orders for the currently logged-in supplier.
    """
    model = Order
    template_name = SUPPLIER_MANAGEMENT
    context_object_name = SUPPLIER_ORDERS

    def get_queryset(self):
        supplier = self.request.user
        return Order.objects.filter(supplier=supplier).select_related(INVENTORY_MANAGER).order_by(ORDER_BY_CREATED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[FIELD_SUPPLIER] = self.request.user
        return context


class SupplierOrderDetailView(SupplierRequiredMixin, DetailView):
    """
        View for displaying details of a specific supplier order.
        Retrieves and displays the details of an order, including its items.
    """
    model = Order
    template_name = SUPPLIER_ORDER_DETAILS
    context_object_name = ORDER

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs.get(ORDER_ID), supplier=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[ORDER_ITEMS] = OrderItem.objects.filter(order=self.object)
        return context


class SupplierOrderUpdateView(SupplierRequiredMixin, UpdateView):
    """
        View for updating a supplier's order.
        Allows the supplier to update the status of their order.
    """
    model = Order
    form_class = SupplierOrderUpdateForm
    template_name = SUPPLIER_ORDER_UPDATE

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs.get(ORDER_ID), supplier=self.request.user)

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("new-order")

