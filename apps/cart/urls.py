from django.urls import path
from apps.cart import views

app_name = "cart"

urlpatterns = [
    path("detail/", views.cart_detail, name="cart_detail"),

    path("add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),

    path("decrease/<int:item_id>/", views.decrease_quantity, name="decrease_quantity"),

    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),

    path("update/<int:item_id>/", views.update_quantity, name="update_quantity"),
]
