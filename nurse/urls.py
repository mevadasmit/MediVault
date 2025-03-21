from django.urls import path
from .views import IndexView, RequestCreateView, RequestListView, RequestDetailView

urlpatterns = [
    path("", IndexView.as_view(), name="nurse_dashboard"),
    path("new/request",RequestCreateView.as_view(), name="new_request"),
    path("requests",RequestListView.as_view(), name="requests"),
    path("requests/<uuid:pk>", RequestDetailView.as_view(), name="request_detail"),
]