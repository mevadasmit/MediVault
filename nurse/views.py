from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib import messages
from django.db import transaction
from django.utils.timezone import now
from inventory_manager.models import OrgInventory
from nurse.forms import RequestForm, RequestedItemForm
from nurse.models import Request, RequestedItems
from base.access import RoleRequiredMixin
from constant import (NURSE, NURSE_DASHBOARD, NURSE_REQUEST_CART, ITEM_FORM, AVAILABLE_INVENTORY, APPROVED, PENDING,
                      GET_INVENTORY, QUANTITY_REQUESTED,REQUESTS, REQUEST, NURSE_REQUEST_LIST, NURSE_REQUEST_DETAILS )



class NurseRequiredMixin(RoleRequiredMixin):
    """
        Mixin to restrict access to nurse users.
    """
    required_role = NURSE


class IndexView(NurseRequiredMixin, TemplateView):
    """
        View for the nurse dashboard.
    """
    template_name = NURSE_DASHBOARD


class RequestCreateView(NurseRequiredMixin, CreateView):
    """
        View for creating a new request.
    """

    model = Request
    form_class = RequestForm
    template_name = NURSE_REQUEST_CART
    success_url = reverse_lazy("requests")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nurse = self.request.user.nurse
        context[ITEM_FORM] = RequestedItemForm(nurse=nurse)
        context[AVAILABLE_INVENTORY] = OrgInventory.objects.filter(organization=nurse.organization)
        return context

    def form_valid(self, form):
        """
            Handle valid form submission.
        """
        nurse = self.request.user.nurse
        request_instance = form.save(commit=False)
        request_instance.nurse = nurse
        request_instance.organization = nurse.organization

        if request_instance.is_emergency:
            request_instance.status = APPROVED
            request_instance.approved_by = self.request.user
            request_instance.approved_at = now()
        else:
            request_instance.status = PENDING

        with transaction.atomic():
            request_instance.save()

            inventory_ids = self.request.POST.getlist(GET_INVENTORY)
            quantities = self.request.POST.getlist(QUANTITY_REQUESTED)

            if inventory_ids and quantities:
                for inventory_id, qty in zip(inventory_ids, quantities):
                    inventory = OrgInventory.objects.get(id=inventory_id)
                    quantity = int(qty)
                    # Ensure stock is available
                    if inventory.quantity_in_stock >= quantity:
                        RequestedItems.objects.create(
                            request=request_instance,
                            inventory=inventory,
                            quantity_requested=quantity,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )

                        inventory.quantity_in_stock -= quantity
                        inventory.save()
                    else:
                        messages.error(self.request, f"Not enough stock for {inventory.inventory.name}")

            # Update total items in the request
            request_instance.total_items = request_instance.items.count()
            request_instance.save()

        return redirect(self.success_url)


class RequestListView(NurseRequiredMixin, ListView):
    """
        View for listing nurse's requests.
    """
    model = Request
    template_name = NURSE_REQUEST_LIST
    context_object_name = REQUESTS
    paginate_by = 5

    def get_queryset(self):
        return Request.objects.filter(nurse=self.request.user.nurse)


class RequestDetailView(NurseRequiredMixin, DetailView):
    """
        View for displaying details of a specific request.
    """
    model = Request
    template_name = NURSE_REQUEST_DETAILS
    context_object_name = REQUEST
