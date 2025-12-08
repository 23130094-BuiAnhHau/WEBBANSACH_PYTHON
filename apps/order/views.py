import datetime
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.order.models import Order, OrderItem, Promotion, RecommendationEngine
from apps.cart.models import Cart
from decimal import Decimal

# --- Thanh toán ---
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.error(request, "Giỏ hàng đang trống!")
        return redirect("cart_detail")

    promo = None
    if request.method == "POST":
        code = request.POST.get("promo_code")
        shipping = request.POST.get("shipping_address")

        if code:
            promo = Promotion.objects.filter(code=code).first()
            if not promo or promo.expire_date < datetime.date.today():
                promo = None

        order = Order.objects.create(
            user=request.user,
            promotion=promo,
            shipping_address=shipping
        )

        total = Decimal(0)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            total += item.book.price * item.quantity

        order.total_price = total

        if promo:
            discount = min(promo.discount_percent, 100)
            order.total_amount = total * (1 - Decimal(discount)/100)
        else:
            order.total_amount = total

        order.save()

        # Update recommendation
        rec, _ = RecommendationEngine.objects.get_or_create(user=request.user)
        for item in cart.items.all():
            rec.order_history.add(item.book)

        cart.items.all().delete()

        return redirect("order_history")

    return render(request, "order/checkout.html", {"cart": cart})

# --- Lịch sử đơn hàng ---
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "order/order_history.html", {"orders": orders})
