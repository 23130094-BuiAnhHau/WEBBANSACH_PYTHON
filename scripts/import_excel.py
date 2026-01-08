import os
import sys
import django
import pandas as pd
from decimal import Decimal
from django.utils import timezone

# SETUP DJANGO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BookStore.settings")
django.setup()

# IMPORT MODELS
from apps.user.models import User, Profile
from apps.book.models import (
    Category, Author, Book, BookImage,
    Review, FavoriteBook, BookViewHistory, ProductDiscount
)
from apps.cart.models import Cart, CartItem
from apps.home.models import Banner
from apps.order.models import (
    Order, OrderItem, PromoCode,
    Promotion, Voucher, UserVoucher
)

# EXCEL FILE
EXCEL_FILE = os.path.join(BASE_DIR, "data", "excel", "Book_db.xlsx")
xls = pd.ExcelFile(EXCEL_FILE)

# HELPER FUNCTIONS
def parse_bool(value):
    if pd.isna(value):
        return False
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes")

def convert_value(field, value):
    if pd.isna(value):
        return None

    field_type = field.get_internal_type()

    try:
        if field_type == "BooleanField":
            return parse_bool(value)

        if field_type in ("DecimalField", "FloatField"):
            return Decimal(str(value))

        if field_type in ("IntegerField", "PositiveIntegerField"):
            return int(value)

        if field_type == "DateTimeField":
            dt = pd.to_datetime(value)
            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt

        if field_type == "DateField":
            return pd.to_datetime(value).date()

    except Exception:
        return None

    return value

# SHEET -> MODEL (THỨ TỰ IMPORT ĐÚNG)
SHEET_MODEL_MAP = {
    "Sheet1": User,
    "profile": Profile,
    "category": Category,
    "author": Author,
    "book": Book,
    "book_image": BookImage,
    "review": Review,
    "favourite_book": FavoriteBook,
    "book_view_history": BookViewHistory,
    "cart": Cart,
    "cart_item": CartItem,
    "banner": Banner,
    "promotion": Promotion,
    "voucher": Voucher,
    "user_voucher": UserVoucher,
    "order_": Order,
    "order_item": OrderItem,
    "promo_code": PromoCode,
    "product_discount": ProductDiscount,
}

# IMPORT DATA
for sheet_name, model in SHEET_MODEL_MAP.items():
    if sheet_name not in xls.sheet_names:
        print(f" Sheet '{sheet_name}' không tồn tại → Bỏ qua")
        continue

    df = pd.read_excel(xls, sheet_name=sheet_name)
    print(f"\n Import {len(df)} dòng cho model {model.__name__}")

    for _, row in df.iterrows():
        obj_data = {}
        skip_row = False

        # DUYỆT FIELD THỰC SỰ TRONG DB
        for field in model._meta.fields:

            # ===== FOREIGN KEY =====
            if field.many_to_one:
                col_name = f"{field.name}_id"

                if col_name not in df.columns:
                    continue

                fk_id = row[col_name]

                if pd.isna(fk_id):
                    print(f"  Bỏ qua {model.__name__}: thiếu {col_name}")
                    skip_row = True
                    break

                try:
                    obj_data[field.name] = field.related_model.objects.get(
                        id=int(fk_id)
                    )
                except field.related_model.DoesNotExist:
                    print(
                        f"  Bỏ qua {model.__name__}: "
                        f"{col_name}={fk_id} không tồn tại"
                    )
                    skip_row = True
                    break

            # ===== FIELD THƯỜNG =====
            else:
                if field.name in df.columns:
                    obj_data[field.name] = convert_value(
                        field, row[field.name]
                    )

        if skip_row:
            continue

        # ===== LOOKUP THEO ID (NẾU CÓ) =====
        lookup = {}
        if "id" in df.columns and not pd.isna(row["id"]):
            lookup["id"] = int(row["id"])

        try:
            obj, created = model.objects.update_or_create(
                **lookup,
                defaults=obj_data
            )
            print(
                f"{' Created' if created else ' Updated'} "
                f"{model.__name__} (id={lookup.get('id')})"
            )
        except Exception as e:
            print(
                f" Lỗi {model.__name__} (id={lookup.get('id')}): {e}"
            )

print("\n  HOÀN TẤT IMPORT EXCEL!")
