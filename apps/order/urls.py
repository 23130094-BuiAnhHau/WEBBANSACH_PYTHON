# apps/order/urls.py
from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("process-payment/<int:order_id>/",views.process_payment,name="process_payment"),
    path("history/", views.order_history, name="order_history"),
    path("order/<int:pk>/", views.order_detail, name="order_detail"),
    path("order/<int:order_id>/bank/", views.bank_payment, name="bank_payment"),
    path("reorder/<int:pk>/", views.reorder, name="reorder"),
    path("apply-promotion/", views.apply_promotion, name="apply_promotion"),
    path("promotions/", views.promotion_list, name="promotion_list"),
    path("order/<int:pk>/delete/confirm/", views.delete_order_confirm, name="delete_order_confirm"),
    path("order/<int:pk>/delete/", views.delete_order, name="delete_order"),
    path("order/<int:order_id>/deleted/", views.order_deleted, name="order_deleted"),

]
