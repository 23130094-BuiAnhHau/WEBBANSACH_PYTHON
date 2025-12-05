from django.db import models

# Danh mục sách
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Tên danh mục

    def __str__(self):
        return self.name


# Sách
class Book(models.Model):
    title = models.CharField(max_length=200)                     # Tiêu đề sách
    author = models.CharField(max_length=100)                    # Tác giả
    price = models.DecimalField(max_digits=10, decimal_places=2) # Giá tiền
    description = models.TextField(blank=True)                   # Mô tả sách
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True) 
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='books'   # Một category có nhiều sách
    )
    stock = models.PositiveIntegerField(default=0)               # Số lượng tồn kho
    published_date = models.DateField(blank=True, null=True)     # Ngày xuất bản

    def __str__(self):
        return f"{self.title} - {self.author}"

    # Hiển thị giá dạng tiền VN
    def formatted_price(self):
        return f"{int(self.price):,} ₫".replace(",", ".")
    formatted_price.short_description = "Giá (VNĐ)"


# Đánh giá sách
class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'     # Một sách có nhiều review
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='reviews'     # Một user có nhiều review
    )
    content = models.TextField()              # Nội dung đánh giá
    rating = models.IntegerField(default=0)   # Điểm 1-5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.book.title} ({self.rating}/5)"
