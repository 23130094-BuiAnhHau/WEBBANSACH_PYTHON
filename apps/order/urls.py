# apps/order/urls.py
from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("history/", views.order_history, name="order_history"),
    path("detail/<int:pk>/", views.order_detail, name="order_detail"),
    path("reorder/<int:pk>/", views.reorder, name="reorder"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("order/<int:order_id>/bank/", views.bank_payment, name="bank_payment")
]
