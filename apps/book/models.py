# apps/book/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(default=0)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    average_rating = models.FloatField(default=0)  # Cache để hiển thị nhanh (cập nhật khi có review)

    def __str__(self):
        return self.title

    def get_display_price(self):
        return self.sale_price if self.sale_price is not None else self.price
    def get_final_price(self):

        #  Giảm theo chương trình
        if hasattr(self, "productdiscount") and self.productdiscount.is_active:
            return self.productdiscount.get_discount_price()

        #  Giảm trực tiếp
        if self.sale_price is not None and self.sale_price < self.price:
            return self.sale_price

        #  Giá gốc
        return self.price
    
    @property
    def has_discount(self):
        if hasattr(self, "productdiscount") and self.productdiscount.is_active:
            return True
        if self.sale_price is not None and self.sale_price < self.price:
            return True
        return False

class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="book_images/")

    def __str__(self):
        return f"Hình của {self.book.title}"

class Review(models.Model):
    # Dùng Review làm rating + comment; 1 user chỉ review 1 sách
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=5)  # 1–5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("book", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review {self.rating} sao - {self.book.title}"
# Giamr giá theo sản phẩm 
class ProductDiscount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    discount_percent = models.IntegerField(default=0)   # giảm %
    discount_amount = models.IntegerField(default=0)    # giảm cố định
    is_active = models.BooleanField(default=True)

    def get_discount_price(self):
        """
        Trả về giá sau khi giảm
        """
        price = self.book.price
        if self.discount_percent > 0:
            return price - price * (self.discount_percent / 100)
        return price - self.discount_amount

# LƯU LỊCH SỬ XEM SÁCH (dùng cho AI)
class BookViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="view_history")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="viewed_by")
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-viewed_at"]

# Yêu thích / wishlist
class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")

# Cache gợi ý (nếu muốn persist score)
class RecommendationCache(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendation_cache")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-score"]
