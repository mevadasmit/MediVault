from django.urls import path
from .views import IndexView, UserListView, OrganizationManagementView, OrganizationRegistrationView, \
    OrganizationUpdateView, OrganizationDeleteView, UserUpdateView, UserDeleteView,NewUserView,ProductCategoryListView, \
    ProductCategoryCreateView , ProductCategoryUpdateView , ProductCategoryDeleteView

urlpatterns = [
    path('',IndexView.as_view() , name='admin_dashboard'),
    path('success/',NewUserView.as_view() , name='register_success'),
    path('usermanagement/',UserListView.as_view() , name='user_management'),
    path('organizationmanagement/',OrganizationManagementView.as_view() , name='organization_management'),
    path('organization/register',OrganizationRegistrationView.as_view() , name='register_organization'),
    path("organizations/edit/<uuid:pk>/", OrganizationUpdateView.as_view(), name="organization_edit"),
    path("organizations/delete/<uuid:pk>/", OrganizationDeleteView.as_view(), name="organization_delete"),
    path("user/edit/<uuid:pk>/", UserUpdateView.as_view(), name="user_edit"),
    path("user/delete/<uuid:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path('product/catgories',ProductCategoryListView.as_view() , name='product_category_list'),
    path('product/catgories/new',ProductCategoryCreateView.as_view() , name='product_category_new'),
    path('product/catgories/edit/<uuid:pk>/',ProductCategoryUpdateView.as_view() , name='product_category_edit'),
    path('product/catgories/delete/<uuid:pk>/',ProductCategoryDeleteView.as_view() , name='product_category_delete'),
]