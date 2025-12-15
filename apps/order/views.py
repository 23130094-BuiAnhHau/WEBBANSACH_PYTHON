# apps/order/views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils import timezone

from .models import (
    Order,
    OrderItem,
    RecommendationEngine,
    PromoCode,
    UserVoucher,
)
from apps.cart.models import Cart, CartItem
from .forms import CheckoutForm



@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related("book").all()

    if not cart_items:
        messages.error(request, "Giỏ hàng đang trống.")
        return redirect("cart:cart_detail")

    # 1. TÍNH TỔNG TIỀN GỐC
    
    raw_total = Decimal("0")
    for item in cart_items:
        raw_total += item.book.get_final_price() * item.quantity


    shipping_fee = Decimal("15000")
    if raw_total >= 500000:
        shipping_fee = Decimal("0")

    promo_discount = Decimal("0")
    final_total = raw_total + shipping_fee


    # 2. LẤY VOUCHER CỦA USER
    
    user_vouchers = UserVoucher.objects.filter(
        user=request.user,
        used=False,
        voucher__is_active=True,
        voucher__start_date__lte=timezone.now(),
        voucher__end_date__gte=timezone.now(),
    ).select_related("voucher")

    # 3. POST – THANH TOÁN
    
    if request.method == "POST":
        form = CheckoutForm(request.POST, user=request.user)
        if not form.is_valid():
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
            return render(request, "order/checkout.html", {
                "cart": cart,
                "cart_items": cart_items,
                "form": form,
                "raw_total": raw_total,
                "shipping_fee": shipping_fee,
                "final_total": final_total,
                "user_vouchers": user_vouchers,
            })

        user_voucher_id = form.cleaned_data.get("user_voucher")
        promo_code_input = form.cleaned_data.get("promo_code")

        #  KHÔNG CHO DÙNG CẢ 2
        if user_voucher_id and promo_code_input:
            messages.error(
                request,
                "Bạn chỉ được sử dụng MỘT trong hai: Voucher hoặc Mã giảm giá."
            )
            return render(request, "order/checkout.html", {
                "cart": cart,
                "cart_items": cart_items,
                "form": form,
                "raw_total": raw_total,
                "shipping_fee": shipping_fee,
                "final_total": final_total,
                "user_vouchers": user_vouchers,
            })

        selected_user_voucher = None
        promo = None

        
        # 4. ÁP DỤNG VOUCHER
        
        if user_voucher_id:
            selected_user_voucher = get_object_or_404(
                UserVoucher,
                id=user_voucher_id,
                user=request.user,
                used=False
            )

            voucher = selected_user_voucher.voucher

            if raw_total < voucher.min_order_amount:
                messages.error(
                    request,
                    f"Đơn hàng tối thiểu {voucher.min_order_amount:,}₫ để dùng voucher này."
                )
                return redirect("order:checkout")

            if not voucher.is_valid():
                messages.error(request, "Voucher không còn hợp lệ.")
                return redirect("order:checkout")

            if voucher.voucher_type == "PERCENT":
                promo_discount = raw_total * voucher.discount_value / 100
            else:
                promo_discount = voucher.discount_value

        
        # 5. ÁP DỤNG PROMO CODE (CHỈ KHI KHÔNG CÓ VOUCHER)
        
        elif promo_code_input:
            promo = PromoCode.objects.filter(
                code__iexact=promo_code_input,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            ).first()

            if not promo:
                messages.error(request, "Mã giảm giá không hợp lệ.")
                return redirect("order:checkout")

            if raw_total < Decimal(promo.min_order_amount):
                messages.error(
                    request,
                    f"Đơn hàng tối thiểu {promo.min_order_amount:,}₫ để dùng mã này."
                )
                return redirect("order:checkout")

            promo_discount = raw_total * Decimal(promo.discount_percent) / 100
            promo_discount += Decimal(promo.discount_amount)

        
        # 6. TÍNH TIỀN CUỐI

        final_total = raw_total - promo_discount + shipping_fee
        if final_total < 0:
            final_total = Decimal("0")

        
        # 7. TẠO ORDER
        
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                shipping_address=form.cleaned_data["shipping_address"],
                payment_method=form.cleaned_data["payment_method"],
                total_price=raw_total,
                total_amount=final_total,
                user_voucher=selected_user_voucher,
                promo_code=promo
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.price
                )

            # Đánh dấu voucher đã dùng
            if selected_user_voucher:
                selected_user_voucher.used = True
                selected_user_voucher.save()

                voucher = selected_user_voucher.voucher
                voucher.quantity -= 1
                voucher.save()

            # Gợi ý sản phẩm
            rec, _ = RecommendationEngine.objects.get_or_create(user=request.user)
            for item in cart_items:
                rec.order_history.add(item.book)

            cart_items.delete()

        messages.success(request, "Đặt hàng thành công!")
        return redirect("order:order_history")

    
    # 8. GET
    form = CheckoutForm(user=request.user)
    return render(request, "order/checkout.html", {
        "cart": cart,
        "cart_items": cart_items,
        "form": form,
        "raw_total": raw_total,
        "shipping_fee": shipping_fee,
        "final_total": final_total,
        "user_vouchers": user_vouchers,
    })

@login_required
def reorder(request, pk):
    # 1. Lấy đơn hàng của chính user
    order = get_object_or_404(Order, pk=pk, user=request.user)

    # 2. Lấy hoặc tạo cart (OneToOne)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # 3. Duyệt từng sản phẩm trong đơn cũ
    for order_item in order.items.all():

        # Nếu sách đã bị xoá khỏi hệ thống thì bỏ qua
        if not order_item.book:
            continue

        cart_item = CartItem.objects.filter(
            cart=cart,
            book=order_item.book
        ).first()

        if cart_item:
            # Đã có trong cart → cộng số lượng
            cart_item.quantity += order_item.quantity
            cart_item.save()
        else:
            # Chưa có tthif tạo mới
            CartItem.objects.create(
                cart=cart,
                book=order_item.book,
                quantity=order_item.quantity,
                price=order_item.book.get_final_price()

            )

    messages.success(request, "Đã thêm sản phẩm vào giỏ hàng.")
    return redirect("cart:cart_detail")
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "order/order_history.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "order/order_detail.html", {"order": order})
