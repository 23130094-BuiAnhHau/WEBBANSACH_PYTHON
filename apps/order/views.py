from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.order.models import Order, OrderItem, Promotion
from apps.cart.models import Cart
from decimal import Decimal

#them 
from django.views.generic import TemplateView
# them vao de test order_history va detail tinh

# Tạo View tĩnh mới (KHÔNG cần @login_required)
class StaticOrderHistoryView(TemplateView):
    # Trỏ thẳng đến template đã tạo
    template_name = "order/order_history.html"

class StaticOrderDetailView(TemplateView):
    # Trỏ thẳng đến template đã tạo
    template_name = "order/order_detail.html"
#



# --- Thanh toán ---
@login_required
def checkout(request):
    # cart = get_object_or_404(Cart, user=request.user)
    # if request.method == "POST":
    #     promo_code = request.POST.get("promo_code")
    #     promo = Promotion.objects.filter(code=promo_code).first() if promo_code else None
    #     order = Order.objects.create(user=request.user, total_price=0, total_amount=0, promotion=promo)
    #     total = Decimal("0.0")
    #     for item in cart.items.all():
    #         OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity, price=item.book.price)
    #         total += item.book.price * item.quantity
    #     # Áp dụng khuyến mãi
    #     order.total_price = total
    #     order.total_amount = total * (1 - Decimal(promo.discount_percent)/100) if promo else total
    #     order.save()
    #     cart.items.all().delete()
    #     return redirect("order_history")
    # return render(request, "order/checkout.html", {"cart": cart})

    # ----------------------------------------------
    #thêm, sửa để chạy templates tĩnh
    cart, created = Cart.objects.get_or_create(user=request.user) 
    if request.method == "POST":
        promo_code = request.POST.get("promo_code")
        promo = Promotion.objects.filter(code=promo_code).first() if promo_code else None
        
        # 1. Tạo Order (chưa có total_amount chính xác)
        order = Order.objects.create(user=request.user, total_price=0, total_amount=0, promotion=promo)
        total = Decimal("0.0")
        
        # 2. Tính tổng tiền (total_price)
        for item in cart.items.all():
            OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity, price=item.book.price)
            total += item.book.price * item.quantity
        
        # 3. Áp dụng khuyến mãi và tính total_amount
        order.total_price = total
        
        # ✅ SỬA LỖI LOGIC TÍNH TỔNG TIỀN CUỐI CÙNG
        if promo:
            # Nếu có khuyến mãi: Áp dụng chiết khấu
            discount_rate = Decimal(promo.discount_percent) / 100
            order.total_amount = total * (1 - discount_rate)
        else:
            # Nếu KHÔNG có khuyến mãi: Total amount bằng Total price
            order.total_amount = total
            
        order.save()
        cart.items.all().delete()
        return redirect("order_history")
        
    return render(request, "order/checkout.html", {"cart": cart})

# --- Lịch sử đơn hàng ---
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "order/order_history.html", {"orders": orders})
