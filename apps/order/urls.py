from django.urls import path
from apps.order.views import checkout, order_history
from apps.order import views #them moi 
urlpatterns = [
    path('', views.checkout, name="root_checkout"), #them de chay checkout.html tinh
    path("checkout/", checkout, name="checkout"),
    path("history/", order_history, name="order_history"),
]
