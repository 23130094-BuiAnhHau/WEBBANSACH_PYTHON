from django.urls import path
from apps.cart.views import cart_detail, add_to_cart, remove_from_cart

urlpatterns = [
    path("", cart_detail, name="cart_detail"),
    path("add/<int:book_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
]
