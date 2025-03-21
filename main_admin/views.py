from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from base.access import RoleRequiredMixin
from main_admin.forms import OrganizationRegistrationForm
from main_admin.models import Organization, InventoryManager, InventoryCategory
from users.models import CustomUser
from .forms import UserUpdateForm
from constant import (ADMIN, ADMIN_DASHBOARD, ROLE, ROLE_COUNTS, ROLE_NAME, ADMIN_NEW_USER_REGISTER,ADMIN_USER_MANAGEMENT,
                      USERS,ADMIN_USER_UPDATE, ADMIN_USER_DELETE, ADMIN_ORGANIZATION_MANAGEMENT, ORGANIZATIONS,FIELD_NAME,
                      ADMIN_ORGANIZATION_REGISTER,CREATED_BY , USER, INVENTORY_MANAGER, UPDATED_BY, ADMIN_ORGANIZATION_UPDATE,
                      ADMIN_ORGANIZATION_DELETE, ADMIN_INVENTORY_CATEGORY, INVENTORY_CATEGORY, ADMIN_INVENTORY_CATEGORY_FORM,
                      ADMIN_INVENTORY_CATEGORY_UPDATE,ADMIN_INVENTORY_CATEGORY_DELETE )

# Create your views here.

class AdminRequiredMixin(RoleRequiredMixin):
    """
        A mixin that requires the user to have the 'ADMIN' role.
    """
    required_role = ADMIN

class IndexView(AdminRequiredMixin, TemplateView):
    """
        Displays the admin dashboard with user role counts.
    """

    model = CustomUser
    template_name = ADMIN_DASHBOARD
    context_object_name = ROLE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[ROLE_COUNTS] = (
            CustomUser.objects.filter(role__isnull=False)
            .values(ROLE_NAME).annotate(user_count=Count('id'))
        )
        return context


class NewUserView(AdminRequiredMixin, TemplateView):
    """
        This view renders the new user registration form.
    """
    template_name = ADMIN_NEW_USER_REGISTER


class UserListView(AdminRequiredMixin, ListView):
    """
        Displays a list of users, excluding those without a role.
    """
    model = CustomUser
    template_name = ADMIN_USER_MANAGEMENT
    context_object_name = USERS
    paginate_by = 5

    def get_queryset(self):
        return CustomUser.objects.exclude(role__isnull=True)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    """
        This view handles the update of a user's information, including their role.
    """
    model = CustomUser
    template_name = ADMIN_USER_UPDATE
    form_class = UserUpdateForm
    success_url = reverse_lazy("user_management")

    def form_valid(self, form):
        admin = form.save(commit=False)
        admin.updated_by = self.request.user
        admin.save()
        return redirect(self.success_url)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    """
        This view handles the deletion of a user.
    """
    model = CustomUser
    template_name = ADMIN_USER_DELETE
    success_url = reverse_lazy("user_management")
    context_object_name = USERS

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)


class OrganizationManagementView(AdminRequiredMixin, ListView):
    """
        Displays a list of all organizations.
    """
    model = Organization
    template_name = ADMIN_ORGANIZATION_MANAGEMENT
    paginate_by = 3
    context_object_name = ORGANIZATIONS

    def get_queryset(self):
        return Organization.objects.all()


class OrganizationRegistrationView(AdminRequiredMixin, CreateView):
    """
        This view handles the creation of a new organization and its associated inventory manager.
    """
    model = Organization
    form_class = OrganizationRegistrationForm
    template_name = ADMIN_ORGANIZATION_REGISTER
    success_url = reverse_lazy("organization_management")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        organization = self.object
        inventory_manager = form.cleaned_data.get(INVENTORY_MANAGER)
        InventoryManager.objects.create(user=inventory_manager, organization=organization, created_by=self.request.user,
                                        updated_by=self.request.user)
        return response


class OrganizationUpdateView(AdminRequiredMixin, UpdateView):
    """
        This view handles the update of an organization's information, including its inventory manager.
    """
    model = Organization
    form_class = OrganizationRegistrationForm
    template_name = ADMIN_ORGANIZATION_UPDATE
    success_url = reverse_lazy("organization_management")

    def get_object(self, queryset=None):
        return get_object_or_404(Organization, pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        organization = self.get_object()

        new_inventory_manager = form.cleaned_data.get(INVENTORY_MANAGER)
        inventory_manager_entry, created = InventoryManager.objects.get_or_create(
            organization=organization,
            defaults={USER: new_inventory_manager,
                      CREATED_BY: self.request.user,
                      UPDATED_BY: self.request.user
                      }
        )

        if not created:
            inventory_manager_entry.user = new_inventory_manager
            inventory_manager_entry.updated_by = self.request.user
            inventory_manager_entry.save()

        return response


class OrganizationDeleteView(AdminRequiredMixin, DeleteView):
    """
        This view handles the deletion of an organization and its associated inventory managers.
    """
    model = Organization
    template_name = ADMIN_ORGANIZATION_DELETE
    success_url = reverse_lazy("organization_management")

    def get_object(self, queryset=None):
        return get_object_or_404(Organization, pk=self.kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        organization = self.get_object()
        InventoryManager.objects.filter(organization=organization).delete()
        return super().delete(request, *args, **kwargs)


class ProductCategoryListView(AdminRequiredMixin, ListView):
    """
        Displays a list of all product categories.
    """
    model = InventoryCategory
    template_name = ADMIN_INVENTORY_CATEGORY
    context_object_name = INVENTORY_CATEGORY
    paginate_by = 5

    def get_queryset(self):
        return InventoryCategory.objects.all()


class ProductCategoryCreateView(AdminRequiredMixin, CreateView):
    """
        This view handles the creation of a new product category.
    """
    model = InventoryCategory
    fields = [FIELD_NAME]
    template_name = ADMIN_INVENTORY_CATEGORY_FORM
    success_url = reverse_lazy("product_category_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ProductCategoryUpdateView(AdminRequiredMixin, UpdateView):
    """
        This view handles the update of a product category.
    """
    model = InventoryCategory
    fields = [FIELD_NAME]
    template_name = ADMIN_INVENTORY_CATEGORY_UPDATE
    success_url = reverse_lazy("product_category_list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ProductCategoryDeleteView(AdminRequiredMixin, DeleteView):
    """
        This view handles the deletion of a product category.
    """
    model = InventoryCategory
    template_name = ADMIN_INVENTORY_CATEGORY_DELETE
    success_url = reverse_lazy("product_category_list")

    def get_object(self, queryset=None):
        return get_object_or_404(InventoryCategory, pk=self.kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        product_category = self.get_object()
        product_category.delete()
        return HttpResponseRedirect(self.success_url)
