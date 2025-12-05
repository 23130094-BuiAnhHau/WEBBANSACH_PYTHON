from django.urls import path
from apps.order.views import checkout, order_history

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("history/", order_history, name="order_history"),
]
