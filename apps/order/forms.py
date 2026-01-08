# apps/order/forms.py
from django import forms
from apps.order.models import UserVoucher


class CheckoutForm(forms.Form):
    #Thông tin người nhận
    fullname = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Họ và tên",
            "class": "form-control"
        })
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "placeholder": "Số điện thoại",
            "class": "form-control"
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            "placeholder": "Email (không bắt buộc)",
            "class": "form-control"
        })
    )

    country = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Quốc gia",
            "class": "form-control"
        })
    )

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Tỉnh / Thành phố",
            "class": "form-control"
        })
    )

    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Địa chỉ giao hàng",
            "rows": 3,
            "class": "form-control"
        })
    )

    # Hình thức thanh toán
    PAYMENT_CHOICES = [
        ("COD", "Thanh toán khi nhận hàng"),
        ("BANK", "Chuyển khoản ngân hàng"),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect
    )

    # Voucher hiện coa của user
    user_voucher = forms.ModelChoiceField(
        queryset=UserVoucher.objects.none(),
        required=False,
        empty_label="-- Không dùng voucher --",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )

    #Mã voucher user nhập vào
    promo_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Nhập mã giảm giá",
            "class": "form-control"
        })
    )

    # Ghi chú đơn hàng
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "placeholder": "Ghi chú đơn hàng",
            "rows": 2,
            "class": "form-control"
        })
    )

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Chỉ load voucher của user hiện tại
        if user:
            self.fields["user_voucher"].queryset = (
                UserVoucher.objects.filter(
                    user=user,
                    used=False,
                    voucher__is_active=True
                )
            )
    def clean(self):
        cleaned_data = super().clean()

        user_voucher = cleaned_data.get("user_voucher")
        promo_code = cleaned_data.get("promo_code")

        #  Không cho dùng cả 2 cùng lúc
        if user_voucher and promo_code:
            raise forms.ValidationError(
                "Bạn chỉ được sử dụng Voucher HOẶC Mã giảm giá, không thể dùng cả hai."
            )

        return cleaned_data
