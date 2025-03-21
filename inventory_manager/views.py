from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView ,DetailView
from inventory_manager.forms import NurseRegistrationForm, NurseUpdateForm, SupplierSelectionFrom
from inventory_manager.models import Nurse, OrgInventory
from main_admin.models import InventoryManager, Inventory
from nurse.models import Request, RequestedItems
from orders.models import Cart, Order
from users.models import CustomUser
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils.timezone import now
from base.access import RoleRequiredMixin
from constant import (INVENTORY__MANAGER, INVENTORY_MANAGER_DASHBOARD , PENDING , DELIVERED , NURSES,INVENTORY_REQUEST_LIST,
                      INVENTORY_NURSE_MANAGEMENT, INVENTORY_NURSE_REGISTER, REQUEST,INVENTORY_MANAGEMENTS,REQUESTS,APPROVED,
                      INVENTORY_NURSE_UPDATE, INVENTORY_NURSE_DELETE,INVENTORY_ITEMS,INVENTORY_SUPPLIER_SELECTION,REJECTED,
                      FIELD_SUPPLIER, INVENTORY_SUPPLIER_INVENTORY,SUPPLIER_ID,SUPPLIER,INVENTORY_ID,CART_ITEMS,
                      INVENTORY_RETURN_LIST, REQUEST_ID, REQUESTED_ITEM_ID, INVENTORY_REQUEST_DETAILS,RETURNABLE_ITEMS )

# Create your views here.

class InventoryManagerRequiredMixin(RoleRequiredMixin):
    """
    Verify that the current user is an Inventory Manager.
    """
    required_role = INVENTORY__MANAGER


class IndexView(InventoryManagerRequiredMixin, TemplateView):
    """
        Inventory Manager Dashboard View.
        Displays the main dashboard for inventory managers.
    """
    template_name = INVENTORY_MANAGER_DASHBOARD

    def get_context_data(self, **kwargs):
        """
            Get context data for the template.
            Adds order counts to the context.
        """
        context = super().get_context_data(**kwargs)
        inventory_manager = get_object_or_404(InventoryManager, user=self.request.user)

        order_counts = Order.objects.filter(inventory_manager=inventory_manager).aggregate(
            pending_orders_count=Count("id", filter=Q(status=PENDING)),
            approved_suppliers_count=Count("id", filter=Q(status=DELIVERED)),
        )

        context.update(order_counts)
        return context


class NurseListView(InventoryManagerRequiredMixin, ListView):
    model = Nurse
    template_name = INVENTORY_NURSE_MANAGEMENT
    context_object_name = NURSES
    paginate_by = 5

    def get_queryset(self):
        """
            Filters nurses based on the current inventory manager's organization.
        """
        inventory_manager = InventoryManager.objects.filter(user=self.request.user).first()
        if inventory_manager:
            return Nurse.objects.filter(inventory_manager=inventory_manager,
                                        organization_id=inventory_manager.organization)
        else:
            return Nurse.objects.none()


class NurseRegisterView(InventoryManagerRequiredMixin, CreateView):
    """
        Handles the registration of new nurses by inventory manager.
    """
    model = Nurse
    form_class = NurseRegistrationForm
    template_name = INVENTORY_NURSE_REGISTER
    success_url = reverse_lazy("nurse_management")

    def get_form_kwargs(self):
        """
            Pass request to form for dynamic fields.
        """
        kwargs = super().get_form_kwargs()
        kwargs[REQUEST] = self.request
        return kwargs

    def form_valid(self, form):
        """
            Handle valid form submission.
            Set created_by and updated_by dynamically.
        """
        nurse = form.save(commit=False)
        nurse.created_by = self.request.user
        nurse.updated_by = self.request.user
        nurse.save()
        return redirect(self.success_url)


class NurseUpdateView(InventoryManagerRequiredMixin, UpdateView):
    """
        Handles updating nurse information by inventory managers.
    """
    model = CustomUser
    form_class = NurseUpdateForm
    template_name = INVENTORY_NURSE_UPDATE
    success_url = reverse_lazy("nurse_management")

    def get_object(self, queryset=None):
        """
            Retrieve the CustomUser object for the nurse.
        """
        return CustomUser.objects.get(pk=self.kwargs["pk"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs[REQUEST] = self.request
        return kwargs

    def form_valid(self, form):
        nurse = form.save(commit=False)
        nurse.updated_by = self.request.user
        nurse.save()
        return redirect(self.success_url)


class NurseDeleteView(InventoryManagerRequiredMixin, DeleteView):
    """
        Handles the deletion of nurses by inventory managers.
    """
    model = CustomUser
    template_name = INVENTORY_NURSE_DELETE
    success_url = reverse_lazy("nurse_management")

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        """
            Delete the nurse.
            Deletes the CustomUser object and redirects to success_url.
        """
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)


class InventoryItemListView(InventoryManagerRequiredMixin, ListView):
    """
        Displays a paginated list of inventory items associated with the
        current inventory manager's organization.
    """
    model = OrgInventory
    template_name = INVENTORY_MANAGEMENTS
    context_object_name = INVENTORY_ITEMS
    paginate_by = 5

    def get_queryset(self):
        """
            Filters inventory items based on the current inventory manager's organization.
        """
        inventory_manager = InventoryManager.objects.get(user=self.request.user)
        return OrgInventory.objects.filter(organization=inventory_manager.organization)


class SupplierSelectionView(InventoryManagerRequiredMixin, FormView):
    """
        Allows inventory managers to select a supplier to view their inventory.
    """
    template_name = INVENTORY_SUPPLIER_SELECTION
    form_class = SupplierSelectionFrom

    def form_valid(self, form):
        """
            Handle valid form submission.
            Redirects to the supplier's inventory view.
        """
        supplier = form.cleaned_data[FIELD_SUPPLIER]
        return redirect('supplier_inventory', supplier_id=supplier.id)


class SupplierInventoryView(InventoryManagerRequiredMixin, ListView):
    """
        Displays the inventory items of a specific supplier.
    """
    model = Inventory
    template_name = INVENTORY_SUPPLIER_INVENTORY
    context_object_name = INVENTORY_ITEMS

    def get_queryset(self):
        """
            Filters inventory items by the selected supplier.
        """
        supplier_id = self.kwargs.get(SUPPLIER_ID)
        supplier = get_object_or_404(CustomUser, id=supplier_id, role__name=SUPPLIER)
        return Inventory.objects.filter(supplier=supplier)

    def get_context_data(self, **kwargs):
        """
            Adds the supplier and cart items to the context.
        """
        context = super().get_context_data(**kwargs)
        context[FIELD_SUPPLIER] = get_object_or_404(CustomUser, id=self.kwargs.get(SUPPLIER_ID))
        inventory_manager = get_object_or_404(InventoryManager, user=self.request.user)
        cart = get_object_or_404(Cart, inventory_manager=inventory_manager)
        context[CART_ITEMS] = cart.cart_items.values_list(INVENTORY_ID, flat=True)
        return context


class RequestListView(InventoryManagerRequiredMixin, ListView):
    """
        Displays a paginated list of requests associated with the current
        inventory manager's organization.
    """
    model = Request
    template_name = INVENTORY_REQUEST_LIST
    context_object_name = REQUESTS
    paginate_by = 5

    def get_queryset(self):
        """
            Filters requests based on the current inventory manager's organization.
        """
        inventory_manager = InventoryManager.objects.filter(user=self.request.user).first()
        return Request.objects.filter(organization=inventory_manager.organization)


class RequestDetailView(InventoryManagerRequiredMixin, DetailView):
    """
        Displays the details of a specific request.
    """
    model = Request
    template_name = INVENTORY_REQUEST_DETAILS
    context_object_name = REQUEST


class ApproveRequestView(InventoryManagerRequiredMixin, UpdateView):
    """
        Approves a specific request, updating its status and timestamps.
    """
    model = Request
    fields = []
    success_url = reverse_lazy("request-list")

    def form_valid(self, form):
        """
            Sets the request status to APPROVED, updates timestamps and user,
            and redirects to the success URL.
        """
        request_instance = self.get_object()
        request_instance.status = APPROVED
        request_instance.approved_by = self.request.user
        request_instance.approved_at = now()
        request_instance.save()
        return redirect(self.success_url)


class RejectRequestView(InventoryManagerRequiredMixin, UpdateView):
    """
        Rejects a specific request, updating its status and timestamps.
    """
    model = Request
    fields = []
    success_url = reverse_lazy("request-list")

    def form_valid(self, form):
        """
            Sets the request status to REJECTED, updates timestamps and user,
            and redirects to the success URL.
        """
        request_instance = self.get_object()
        request_instance.status = REJECTED
        request_instance.rejected_by = self.request.user
        request_instance.rejected_at = now()
        request_instance.save()
        return redirect(self.success_url)



class ReturnableItemsListView(InventoryManagerRequiredMixin, ListView):
    """
        Displays a list of returnable items for a specific request.
    """
    model = RequestedItems
    template_name = INVENTORY_RETURN_LIST
    context_object_name = RETURNABLE_ITEMS

    def get_queryset(self):
        """
            Filters items based on request ID, return status, and reusability.
        """
        request_id = self.kwargs.get(REQUEST_ID)

        return RequestedItems.objects.filter(
            request_id=request_id,
            is_returned=False,
            inventory__inventory__is_reusable=True
        )


class ReturnInventoryView(InventoryManagerRequiredMixin, UpdateView):
    """
        Handles the return of reusable inventory items from a request.
    """
    model = RequestedItems
    fields = []

    def get_object(self, queryset=None):
        """
            Retrieves the object based on requested_item_uuid and ensures it
            has not already been returned.
        """
        requested_item_uuid = self.kwargs[REQUESTED_ITEM_ID]
        return get_object_or_404(RequestedItems, id=requested_item_uuid, is_returned=False)

    def form_valid(self, form):
        """
            Marks the requested item as returned if it is reusable.
        """
        requested_item = self.object

        if requested_item.inventory.inventory.is_reusable:
            requested_item.is_returned = True
            requested_item.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        """
            Redirects to the returnable items list for the request.
        """
        return reverse_lazy("returnable_items", kwargs={REQUEST_ID: self.object.request.id})





