from django.urls import path
from .views import IndexView, SupplierOrderListView, SupplierOrderDetailView, SupplierOrderUpdateView

urlpatterns = [
    path("", IndexView.as_view(), name="supplier_dashboard"),
    path("orders/", SupplierOrderListView.as_view(), name="new-order"),
    path("dashboard/<uuid:order_id>/details/", SupplierOrderDetailView.as_view(), name="order_information"),
    path("dashboard/<uuid:order_id>/update/", SupplierOrderUpdateView.as_view(), name="supplier_order_update"),
]
