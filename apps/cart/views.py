from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from apps.cart.models import Cart, CartItem
from apps.book.models import Book


@login_required
def cart_detail(request):
    """Hiển thị giỏ hàng của user"""
    cart, _ = Cart.objects.prefetch_related("items__book").get_or_create(user=request.user)
    return render(request, "cart/cart_detail.html", {"cart": cart})

@login_required
@require_POST
def add_to_cart(request, book_id):
    """Thêm sách vào giỏ hàng"""
    book = get_object_or_404(Book, id=book_id)

    if book.stock <= 0:
        return redirect("cart:cart_detail")

    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={"quantity": 1}
    )

    if not created and item.quantity < book.stock:
        item.quantity += 1
        item.save()

    return redirect("cart:cart_detail")  # reload lại trang


@login_required
@require_POST
def decrease_quantity(request, item_id):
    """Giảm số lượng sách trong giỏ"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart:cart_detail")


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Xoá sách khỏi giỏ hàng"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("cart:cart_detail")


@login_required
@require_POST
def update_quantity(request, item_id):
    """Cập nhật số lượng sách"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        item.delete()
        return redirect("cart:cart_detail")

    if quantity > item.book.stock:
        quantity = item.book.stock

    item.quantity = quantity
    item.save()

    return redirect("cart:cart_detail")
