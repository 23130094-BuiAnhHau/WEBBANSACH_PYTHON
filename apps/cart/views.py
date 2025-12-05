from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.cart.models import Cart, CartItem
from apps.book.models import Book

# --- Xem giỏ hàng ---
@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/cart_detail.html", {"cart": cart})

# --- Thêm sách vào giỏ ---
@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("cart_detail")

# --- Xóa sách khỏi giỏ ---
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("cart_detail")
