from django.contrib.auth import logout, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.contrib import messages
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from users.models import CustomUser
from users.forms import UserRegistrationForm, UserUpdateForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from constant import (BASE_DASHBOARD, BASE_REGISTER, USER_REGISTER, USER_LOGIN, ADMIN, INVENTORY__MANAGER, SUPPLIER, NURSE,
                      USER_CHANGE_PASSWORD, USER_PROFILE_UPDATE, )

# Create your views here.
class IndexView(TemplateView):
    template_name = BASE_DASHBOARD


class NewUserView(TemplateView):
    template_name = BASE_REGISTER


class RegisterView(LoginRequiredMixin, CreateView):
    """
        View for registering a new user.
        Creates a new user account and redirects to a success page.
    """
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = USER_REGISTER

    def form_valid(self, form):
        self.object = form.save()
        return redirect("register_success")


class UserLoginView(LoginView):
    """
        View for user login.
        Logs in the user and redirects them to the appropriate dashboard based on their role.
        If it's the user's first time logging in, redirects them to change their password.
    """
    template_name = USER_LOGIN

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        role_name = user.role.name if user.role else None

        if user.first_time_login:
            return redirect('change-password')

        # Redirect based on role
        if role_name == ADMIN:
            return redirect("admin_dashboard")
        elif role_name == INVENTORY__MANAGER:
            return redirect("inventory_manager_dashboard")
        elif role_name == SUPPLIER:
            return redirect("supplier_dashboard")
        elif role_name == NURSE:
            return redirect("nurse_dashboard")
        else:
            return redirect("new-user")


class UserLogoutView(View):
    """
        View for logging users out.
        Logs the user out and redirects them to the login page.
    """

    def get(self, request):
        logout(request)
        return redirect('user-login')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
        View for updating user profiles.
        Allows logged-in users to update their profile information.
    """
    form_class = UserUpdateForm
    template_name = USER_PROFILE_UPDATE
    success_url = reverse_lazy("edit-profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)



class UserPasswordChangeView(PasswordChangeView):
    """
        View for changing user passwords.
        Handles password change and updates the first_time_login status. Logs the user out after a successful password change.
    """
    template_name = USER_CHANGE_PASSWORD
    form_class = PasswordChangeForm
    success_url = reverse_lazy("user-login")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        user.first_time_login = False
        user.save()
        logout(self.request)
        return response


class DashboardView(LoginRequiredMixin,TemplateView):
    """
        View for redirecting users to their respective dashboards.
    """
    def get(self, request, *args, **kwargs):
        user = self.request.user
        role_name = user.role.name if user.role else None

        if role_name == ADMIN:
            return redirect("admin_dashboard")
        elif role_name == INVENTORY__MANAGER:
            return redirect("inventory_manager_dashboard")
        elif role_name == SUPPLIER:
            return redirect("supplier_dashboard")
        elif role_name == NURSE:
            return redirect("nurse_dashboard")
        else:
            return redirect("new-user")

