# apps/order/views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

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
    cart_items = cart.items.select_related("book")

    # giỏ hàng trống
    if not cart_items.exists():
        messages.error(request, "Giỏ hàng đang trống")
        return redirect("cart:cart_detail")

    # tổng tiền gốc
    raw_total = sum(
        item.book.get_final_price() * item.quantity
        for item in cart_items
    )

    # phí vận chuyển
    shipping_fee = Decimal("0") if raw_total >= 500000 else Decimal("15000")
    promo_discount = Decimal("0")
    final_total = raw_total + shipping_fee
    
    # danh sách voucher của user (chỉ những voucher chưa dùng và còn hạn)
    user_vouchers = UserVoucher.objects.filter(
        user=request.user,
        used=False,
        voucher__is_active=True,
        voucher__start_date__lte=timezone.now(),
        voucher__end_date__gte=timezone.now(),
    ).select_related("voucher")

    # Biến để lưu voucher đang được chọn
    selected_user_voucher = None
    applied_voucher_id = None

    # Xử lý GET request - có thể có voucher từ query string
    if request.method == "GET":
        voucher_id = request.GET.get("user_voucher")
        if voucher_id:
            selected_user_voucher = UserVoucher.objects.filter(
                id=voucher_id,
                user=request.user,
                used=False,
                voucher__is_active=True,
                voucher__start_date__lte=timezone.now(),
                voucher__end_date__gte=timezone.now(),
            ).select_related("voucher").first()

            if selected_user_voucher:
                voucher = selected_user_voucher.voucher
                
                # Kiểm tra điều kiện sử dụng voucher
                if raw_total >= voucher.min_order_amount:
                    if voucher.voucher_type == "PERCENT":
                        discount = raw_total * voucher.discount_value / 100
                        if voucher.max_discount_amount:
                            discount = min(discount, voucher.max_discount_amount)
                        promo_discount = discount
                    else:
                        promo_discount = voucher.discount_value
                    
                    promo_discount = min(promo_discount, raw_total)
                    final_total = raw_total - promo_discount + shipping_fee
                    applied_voucher_id = voucher_id
                else:
                    messages.warning(
                        request, 
                        f"Đơn hàng chưa đạt tối thiểu {voucher.min_order_amount:,}₫ để sử dụng voucher này"
                    )

    # Xử lý POST request - đặt hàng
    if request.method == "POST":
        form = CheckoutForm(request.POST, user=request.user)

        if not form.is_valid():
            messages.error(request, "Vui lòng kiểm tra lại thông tin")
            return render(request, "order/checkout.html", {
                "cart": cart,
                "cart_items": cart_items,
                "form": form,
                "raw_total": raw_total,
                "shipping_fee": shipping_fee,
                "promo_discount": Decimal("0"),
                "final_total": raw_total + shipping_fee,
                "user_vouchers": user_vouchers,
                "applied_voucher_id": applied_voucher_id,
            })

        # Lấy dữ liệu từ form
        selected_user_voucher = form.cleaned_data.get("user_voucher")
        promo_code_input = form.cleaned_data.get("promo_code")
        promo = None
        promo_discount = Decimal("0")

        # Không cho dùng cả hai
        if selected_user_voucher and promo_code_input:
            messages.error(request, "Chỉ được dùng voucher hoặc mã giảm giá")
            return render(request, "order/checkout.html", {
                "cart": cart,
                "cart_items": cart_items,
                "form": form,
                "raw_total": raw_total,
                "shipping_fee": shipping_fee,
                "promo_discount": Decimal("0"),
                "final_total": raw_total + shipping_fee,
                "user_vouchers": user_vouchers,
                "applied_voucher_id": applied_voucher_id,
            })

        # Áp dụng voucher
        if selected_user_voucher:
            voucher = selected_user_voucher.voucher

            if not voucher.is_valid:
                messages.error(request, "Voucher không hợp lệ")
                return render(request, "order/checkout.html", {
                    "cart": cart,
                    "cart_items": cart_items,
                    "form": form,
                    "raw_total": raw_total,
                    "shipping_fee": shipping_fee,
                    "promo_discount": Decimal("0"),
                    "final_total": raw_total + shipping_fee,
                    "user_vouchers": user_vouchers,
                    "applied_voucher_id": applied_voucher_id,
                })

            if raw_total < voucher.min_order_amount:
                messages.error(
                    request,
                    f"Đơn tối thiểu {voucher.min_order_amount:,}₫"
                )
                return render(request, "order/checkout.html", {
                    "cart": cart,
                    "cart_items": cart_items,
                    "form": form,
                    "raw_total": raw_total,
                    "shipping_fee": shipping_fee,
                    "promo_discount": Decimal("0"),
                    "final_total": raw_total + shipping_fee,
                    "user_vouchers": user_vouchers,
                    "applied_voucher_id": applied_voucher_id,
                })

            # Tính giảm giá
            if voucher.voucher_type == "PERCENT":
                discount = raw_total * voucher.discount_value / 100
                if voucher.max_discount_amount:
                    discount = min(discount, voucher.max_discount_amount)
                promo_discount = discount
            else:
                promo_discount = voucher.discount_value

        # Áp dụng mã giảm giá
        elif promo_code_input:
            promo = PromoCode.objects.filter(
                code__iexact=promo_code_input,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            ).first()

            if not promo:
                messages.error(request, "Mã giảm giá không hợp lệ")
                return render(request, "order/checkout.html", {
                    "cart": cart,
                    "cart_items": cart_items,
                    "form": form,
                    "raw_total": raw_total,
                    "shipping_fee": shipping_fee,
                    "promo_discount": Decimal("0"),
                    "final_total": raw_total + shipping_fee,
                    "user_vouchers": user_vouchers,
                    "applied_voucher_id": applied_voucher_id,
                })

            if raw_total < promo.min_order_amount:
                messages.error(
                    request,
                    f"Đơn tối thiểu {promo.min_order_amount:,}₫"
                )
                return render(request, "order/checkout.html", {
                    "cart": cart,
                    "cart_items": cart_items,
                    "form": form,
                    "raw_total": raw_total,
                    "shipping_fee": shipping_fee,
                    "promo_discount": Decimal("0"),
                    "final_total": raw_total + shipping_fee,
                    "user_vouchers": user_vouchers,
                    "applied_voucher_id": applied_voucher_id,
                })

            promo_discount = (
                raw_total * promo.discount_percent / 100
                + promo.discount_amount
            )

        # Tính tổng tiền cuối
        promo_discount = min(promo_discount, raw_total)
        final_total = raw_total - promo_discount + shipping_fee

        # Tạo đơn hàng
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
                    price=item.book.price
                )

            # Đánh dấu voucher đã dùng
            if selected_user_voucher:
                selected_user_voucher.used = True
                selected_user_voucher.used_at = timezone.now()
                selected_user_voucher.save()

            # Lưu lịch sử mua hàng
            rec, _ = RecommendationEngine.objects.get_or_create(user=request.user)
            for item in cart_items:
                rec.order_history.add(item.book)

            cart_items.delete()

        messages.success(request, "Đặt hàng thành công")
        return redirect("order:process_payment", order_id=order.id)

    form = CheckoutForm(
        initial={
            "user_voucher": selected_user_voucher.id if selected_user_voucher else None
        },
        user=request.user
    )
    form.fields['user_voucher'].queryset = user_vouchers

    return render(request, "order/checkout.html", {
        "cart": cart,
        "cart_items": cart_items,
        "form": form,
        "raw_total": raw_total,
        "shipping_fee": shipping_fee,
        "promo_discount": promo_discount,
        "final_total": final_total,
        "user_vouchers": user_vouchers,
        "applied_voucher_id": applied_voucher_id,
    })

@login_required
def apply_promotion(request):
    if request.method == "POST":
        voucher = get_object_or_404(
            UserVoucher,
            id=request.POST.get("promo_id"),
            user=request.user,
            used=False
        )

        if not voucher.voucher.is_valid():
            messages.error(request, "Voucher không còn hiệu lực.")
            return redirect("order:promotion_list")

        request.session["selected_voucher_id"] = voucher.id
        messages.success(request, "Đã áp dụng voucher.")

    return redirect("order:checkout")

@login_required
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.payment_method == "COD":
        order.payment_status = "unpaid"
        order.status = "Pending"
        order.save()
        return redirect("order:order_detail", order.id)

    if order.payment_method == "BANK":
        return redirect("order:bank_payment", order.id)


@login_required
def bank_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "order/bank_payment.html", {
        "order": order,
        "bank_name": "Vietcombank",
        "account_name": "NGUYEN VAN A",
        "account_number": "0123456789",
        "qr_image": "images/qr.png",
    })


@login_required
def reorder(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    cart, created = Cart.objects.get_or_create(user=request.user)

    for order_item in order.items.all():
        if not order_item.book:
            continue

        cart_item = CartItem.objects.filter(
            cart=cart,
            book=order_item.book
        ).first()

        if cart_item:
            cart_item.quantity += order_item.quantity
            cart_item.save()
        else:
            CartItem.objects.create(
                cart=cart,
                book=order_item.book,
                quantity=order_item.quantity,
                price=order_item.book.get_final_price()
            )

    messages.success(request, "Đã thêm sản phẩm vào giỏ hàng.")
    return redirect("cart:cart_detail")


@login_required
def promotion_list(request):
    now = timezone.now()

    vouchers = (
        UserVoucher.objects
        .filter(
            user=request.user,
            used=False,
            voucher__is_active=True,
            voucher__start_date__lte=now,
            voucher__end_date__gte=now,
        )
        .select_related("voucher")
    )
    for uv in vouchers:
        delta = uv.voucher.end_date.date() - now.date()
        uv.days_left = delta.days
        uv.is_expiring = 0 < uv.days_left <= 3

    return render(request, "order/promotion_list.html", {
        "vouchers": vouchers
    })



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "order/order_history.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "order/order_detail.html", {"order": order})

@login_required
def delete_order_confirm(request, pk):
    """Xác nhận xóa đơn hàng"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    if order.status != "Pending":
        messages.error(request, "Chỉ có thể hủy đơn hàng đang ở trạng thái Đang xử lý")
        return redirect("order:order_detail", pk=pk)
    
    return render(request, "order/delete_order_confirm.html", {
        "order": order
    })

@login_required
@require_POST
def delete_order(request, pk):
    """Xóa đơn hàng (chỉ khi ở trạng thái Pending)"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    # Kiểm tra trạng thái
    if order.status != "Pending":
        messages.error(request, "Chỉ có thể hủy đơn hàng đang ở trạng thái Đang xử lý")
        return redirect("order:order_detail", pk=pk)
    try:
        # Lấy lại voucher nếu có
        if order.user_voucher:
            user_voucher = order.user_voucher
            user_voucher.used = False
            user_voucher.used_at = None
            user_voucher.save()
        
        # Xóa đơn hàng
        order_id = order.id
        order.delete()
        
        messages.success(request, f"Đã hủy đơn hàng #{order_id} thành công")
        return redirect("order:order_deleted", order_id=order_id)
        
    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra: {str(e)}")
        return redirect("order:order_detail", pk=pk)

@login_required
def order_deleted(request, order_id):
    """Hiển thị trang thông báo đã xóa đơn hàng"""
    return render(request, "order/order_deleted.html", {
        "order_id": order_id
    })