from django.urls import path


from orders.views import AddToCartView, CartView, UpdateCartQuantityView, RemoveFromCartView, OrderDetailView, \
    OrderListView, OrderCreateView, OrderUpdateView , OrderConfirmationView

urlpatterns = [
    path("add_to_cart/",AddToCartView.as_view(),name="add_to_cart"),
    path("view_cart/",CartView.as_view(),name="view_cart"),
    path("update-cart/<uuid:item_id>/", UpdateCartQuantityView.as_view(), name="update_cart_quantity"),
    path("remove-cart/<uuid:item_id>/", RemoveFromCartView.as_view(), name="remove_from_cart"),
    path("order-confirm",OrderConfirmationView.as_view(),name="order_confirm"),
    path("orders-list/", OrderListView.as_view(), name="order_list"),
    path("orders-list/<uuid:order_id>/details", OrderDetailView.as_view(), name="order_detail"),
    path("orders-list/<uuid:order_id>/update", OrderUpdateView.as_view(), name="order_update"),
    path("order/new-create", OrderCreateView.as_view(), name="order_create"),

]