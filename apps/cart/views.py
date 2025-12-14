from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from apps.cart.models import Cart, CartItem
from apps.book.models import Book

# xem giỏ hàng
@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/cart_detail.html", {
        "cart": cart
    })
#thêm sản phaanamr vào giỏ
@login_required
@require_POST
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={
            "price": book.price,
            "quantity": 1
        }
    )

    if not created:
        item.quantity += 1
        item.save()

    return JsonResponse ({
        "success": True,
        "message": "Đã thêm sản phẩm vào giỏ hàng 🛒",
        "quantity": item.quantity
    })
#giảm số lượng
@login_required
@require_POST
def decrease_quantity(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart:cart_detail")
#Xóa sane phẩm khỏi giỏ
@login_required
@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )
    item.delete()
    return redirect("cart:cart_detail")

#tùy chọn
@login_required
@require_POST
def update_quantity(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    if quantity < 1:
        item.delete()
    else:
        item.quantity = quantity
        item.save()

    return redirect("cart:cart_detail")
