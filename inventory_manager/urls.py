from django.urls import path
from .views import IndexView, NurseListView, NurseRegisterView, NurseDeleteView, NurseUpdateView, InventoryItemListView, \
    SupplierSelectionView, SupplierInventoryView, ApproveRequestView, RejectRequestView, RequestListView, \
    ReturnInventoryView , ReturnableItemsListView , RequestDetailView

urlpatterns = [
    path("", IndexView.as_view(), name="inventory_manager_dashboard"),
    path("dashboard/nurse",NurseListView.as_view(), name="nurse_management"),
    path("dashboard/nurse/add",NurseRegisterView.as_view(), name="nurse-register"),
    path("dashboard/nurse/edit/<uuid:pk>/",NurseUpdateView.as_view(), name="nurse-update"),
    path("dashboard/nurse/delete/<uuid:pk>/",NurseDeleteView.as_view(), name="nurse-delete"),
    path("dashboard/inventory", InventoryItemListView.as_view(), name="inventory-management"),
    path("dashboard/select_supplier", SupplierSelectionView.as_view(), name="supplier-selection"),
    path('supplier/<uuid:supplier_id>/inventory/', SupplierInventoryView.as_view(), name='supplier_inventory'),
    path("request/<uuid:pk>/approve/", ApproveRequestView.as_view(), name="approve_request"),
    path("request/<uuid:pk>/reject/", RejectRequestView.as_view(), name="reject_request"),
    path("request/",RequestListView.as_view(), name="request-list"),
    path("requests/<uuid:pk>", RequestDetailView.as_view(), name="request_details"),
    path("returnable-items/<uuid:request_id>/", ReturnableItemsListView.as_view(), name="returnable_items"),
    path("return/<uuid:requested_item_id>/", ReturnInventoryView.as_view(), name="return_inventory")

]