from django.urls import path , include
from users.views import (RegisterView, NewUserView, UserLoginView, UserLogoutView,
                         UserPasswordChangeView, UserProfileUpdateView, DashboardView)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", UserLoginView.as_view(), name='user-login'),
    path('new-user', NewUserView.as_view(), name='new-user'),
    path("register", RegisterView.as_view(), name='user-register'),
    path("logout", UserLogoutView.as_view(), name='user-logout'),
    path("changepassword", UserPasswordChangeView.as_view(), name='change-password'),
    path('dashboard',DashboardView.as_view(), name='dashboard_redirect'),
    path('editprofile/', UserProfileUpdateView.as_view(), name="edit-profile"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="users/reset_password.html"),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_complete'),
]
