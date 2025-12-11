import os
import django
import random
import requests
from datetime import date, timedelta
from django.core.files.base import ContentFile
import sys

# CẤU HÌNH DJANGO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookStore.settings')
django.setup()

from apps.book.models import Category, Book, Review
from apps.user.models import User, Profile
from apps.cart.models import Cart, CartItem
from apps.order.models import (
    Order, OrderItem, Promotion, RecommendationEngine, ShippingInfo
)

#DANH MỤC
CATEGORIES = [
    "Văn học", "Tiểu thuyết", "Kỹ năng sống", "Kinh tế",
    "Tâm lý học", "Lập trình", "Trinh thám", "Thiếu nhi", "Khoa học","Tiểu sử",
]

#SÁCH
BOOKS = [
    {"title": "Đắc Nhân Tâm", "author": "Dale Carnegie", "price": 120000, "category": "Kỹ năng sống"},
    {"title": "Nhà Giả Kim", "author": "Paulo Coelho", "price": 95000, "category": "Tiểu thuyết"},
    {"title": "7 Thói Quen Hiệu Quả", "author": "Stephen R. Covey", "price": 135000, "category": "Kỹ năng sống"},
    {"title": "Clean Code", "author": "Robert C. Martin", "price": 250000, "category": "Lập trình"},
    {"title": "Harry Potter và Hòn Đá Phù Thủy", "author": "J.K. Rowling", "price": 160000, "category": "Tiểu thuyết"},
    {"title": "Tôi Thấy Hoa Vàng Trên Cỏ Xanh", "author": "Nguyễn Nhật Ánh", "price": 67000, "category": "Tiểu thuyết"},
    {"title": "Atomic Habits", "author": "James Clear", "price": 145000, "category": "Kỹ năng sống"},

    {"title": "Cà Phê Cùng Tony", "author": "Tony Buổi Sáng", "price": 65000, "category": "Kỹ năng sống"},
    {"title": "Mắt Biếc", "author": "Nguyễn Nhật Ánh", "price": 59000, "category": "Tiểu thuyết"},
    {"title": "Hạt Giống Tâm Hồn", "author": "Nhiều tác giả", "price": 85000, "category": "Kỹ năng sống"},
    {"title": "Sapiens: Lược Sử Loài Người", "author": "Yuval Noah Harari", "price": 185000, "category": "Kinh tế"},
    {"title": "Homo Deus", "author": "Yuval Noah Harari", "price": 195000, "category": "Kinh tế"},
    {"title": "Think and Grow Rich", "author": "Napoleon Hill", "price": 130000, "category": "Kỹ năng sống"},
    {"title": "The Power of Now", "author": "Eckhart Tolle", "price": 140000, "category": "Kỹ năng sống"},
    {"title": "The 4-Hour Workweek", "author": "Timothy Ferriss", "price": 175000, "category": "Kỹ năng sống"},
    {"title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "price": 115000, "category": "Kinh tế"},

    {"title": "Bí Quyết Tư Duy Triệu Phú", "author": "T. Harv Eker", "price": 98000, "category": "Kỹ năng sống"},
    {"title": "Lược Sử Thời Gian", "author": "Stephen Hawking", "price": 150000, "category": "Khoa học"},
    {"title": "How to Win Friends & Influence People", "author": "Dale Carnegie", "price": 125000, "category": "Kỹ năng sống"},
    {"title": "Lãnh Đạo Không Chức Danh", "author": "Robin Sharma", "price": 90000, "category": "Kỹ năng sống"},
    {"title": "Muôn Kiếp Nhân Sinh", "author": "Nguyên Phong", "price": 135000, "category": "Tiểu thuyết"},
    {"title": "Điềm Tĩnh và Nóng Giận", "author": "Thiền sư Ajahn Brahm", "price": 95000, "category": "Kỹ năng sống"},
    {"title": "Sống Chậm Lại", "author": "Nhiều tác giả", "price": 70000, "category": "Kỹ năng sống"},

    {"title": "Tuổi Trẻ Không Hối Tiếc", "author": "Khuyết Danh", "price": 79000, "category": "Kỹ năng sống"},
    {"title": "Dám Nghĩ Lớn", "author": "David Schwartz", "price": 140000, "category": "Kỹ năng sống"},
    {"title": "Đừng Bao Giờ Đi Ăn Một Mình", "author": "Keith Ferrazzi", "price": 160000, "category": "Kỹ năng sống"},
    {"title": "Tư Duy Nhanh và Chậm", "author": "Daniel Kahneman", "price": 180000, "category": "Kỹ năng sống"},
    {"title": "Làm Ít Được Nhiều", "author": "Cal Newport", "price": 155000, "category": "Kỹ năng sống"},
    {"title": "Thiên Tài Bên Trái, Kẻ Điên Bên Phải", "author": "Cao Minh", "price": 135000, "category": "Kỹ năng sống"},
    {"title": "Steve Jobs", "author": "Walter Isaacson", "price": 195000, "category": "Tiểu sử"},

    {"title": "Elon Musk", "author": "Ashlee Vance", "price": 200000, "category": "Tiểu sử"},
    {"title": "Bố Già", "author": "Mario Puzo", "price": 160000, "category": "Tiểu thuyết"},
    {"title": "Hoàng Tử Bé", "author": "Antoine de Saint-Exupéry", "price": 75000, "category": "Thiếu nhi"},
    {"title": "Nhà Lãnh Đạo Tài Ba", "author": "Peter Drucker", "price": 155000, "category": "Kinh tế"},
    {"title": "Tốt Đến Vĩ Đại", "author": "Jim Collins", "price": 170000, "category": "Kinh tế"},
    {"title": "Quẳng Gánh Lo Đi Và Vui Sống", "author": "Dale Carnegie", "price": 115000, "category": "Kỹ năng sống"},
    {"title": "Đời Thay Đổi Khi Chúng Ta Thay Đổi", "author": "Andrew Matthews", "price": 95000, "category": "Kỹ năng sống"},

    {"title": "Tuổi Trẻ Không Hối Hận", "author": "Khuyết Danh", "price": 82000, "category": "Kỹ năng sống"},
    {"title": "The Psychology of Money", "author": "Morgan Housel", "price": 165000, "category": "Kinh tế"},
    {"title": "Ikigai", "author": "Héctor García", "price": 125000, "category": "Kỹ năng sống"},
    {"title": "Start With Why", "author": "Simon Sinek", "price": 150000, "category": "Kỹ năng sống"},
    {"title": "Zero to One", "author": "Peter Thiel", "price": 145000, "category": "Kinh tế"},
    {"title": "The Lean Startup", "author": "Eric Ries", "price": 160000, "category": "Kinh tế"},
    {"title": "Deep Work", "author": "Cal Newport", "price": 155000, "category": "Kỹ năng sống"},
    {"title": "Mindset", "author": "Carol Dweck", "price": 140000, "category": "Kỹ năng sống"},
    {"title": "Grit", "author": "Angela Duckworth", "price": 150000, "category": "Kỹ năng sống"},

    {"title": "Lập Trình Hướng Đối Tượng", "author": "Nguyễn Văn A", "price": 135000, "category": "Lập trình"},
    {"title": "Python Cơ Bản", "author": "Trần Minh Quân", "price": 145000, "category": "Lập trình"},
    {"title": "Django Thực Hành", "author": "Lê Hoàng Long", "price": 165000, "category": "Lập trình"},
    {"title": "Cấu Trúc Dữ Liệu Và Giải Thuật", "author": "Ngô Minh Tuấn", "price": 175000, "category": "Lập trình"},
    {"title": "Lập Trình Java Từ Cơ Bản Đến Nâng Cao", "author": "Phạm Văn Đức", "price": 185000, "category": "Lập trình"},
    {"title": "Thiết Kế Hệ Thống", "author": "Alex Xu", "price": 200000, "category": "Lập trình"},
    {"title": "System Design Interview", "author": "Alex Xu", "price": 210000, "category": "Lập trình"},
    {"title": "Cracking the Coding Interview", "author": "Gayle Laakmann", "price": 230000, "category": "Lập trình"},
    {"title": "Refactoring", "author": "Martin Fowler", "price": 220000, "category": "Lập trình"},
    {"title": "Design Patterns", "author": "Erich Gamma", "price": 240000, "category": "Lập trình"},

    {"title": "Biến Mọi Thứ Thành Tiền", "author": "Dan Lok", "price": 175000, "category": "Kinh tế"},
    {"title": "Luật Hấp Dẫn", "author": "Esther Hicks", "price": 120000, "category": "Kỹ năng sống"},
    {"title": "Tư Duy Phản Biện", "author": "Richard Paul", "price": 135000, "category": "Kỹ năng sống"},
    {"title": "Đọc Vị Bất Kỳ Ai", "author": "David J. Lieberman", "price": 145000, "category": "Kỹ năng sống"},
    {"title": "Bán Hàng Bằng Cảm Xúc", "author": "Jeffrey Gitomer", "price": 155000, "category": "Kinh tế"},
    {"title": "Nghệ Thuật Đàm Phán", "author": "William Ury", "price": 160000, "category": "Kỹ năng sống"},
    {"title": "Thói Quen Thành Công", "author": "Brian Tracy", "price": 140000, "category": "Kỹ năng sống"},
    {"title": "Sức Mạnh Của Kỷ Luật", "author": "Ryan Holiday", "price": 165000, "category": "Kỹ năng sống"},
    {"title": "Nghĩ Giàu Làm Giàu (Bản Đặc Biệt)", "author": "Napoleon Hill", "price": 190000, "category": "Kỹ năng sống"},
    {"title": "Sống Tối Giản", "author": "Joshua Becker", "price": 125000, "category": "Kỹ năng sống"},

    {"title": "Hành Trình Về Phương Đông", "author": "Nguyên Phong", "price": 150000, "category": "Tiểu thuyết"},
    {"title": "Đi Tìm Lẽ Sống", "author": "Viktor Frankl", "price": 135000, "category": "Kỹ năng sống"},
    {"title": "Thuật Quản Trị", "author": "Peter Drucker", "price": 175000, "category": "Kinh tế"},
    {"title": "Từ Tốt Đến Vĩ Đại", "author": "Jim Collins", "price": 180000, "category": "Kinh tế"},
    {"title": "Bí Quyết Học Nhanh", "author": "Tony Buzan", "price": 145000, "category": "Kỹ năng sống"},
    {"title": "Nghệ Thuật Tập Trung", "author": "Cal Newport", "price": 155000, "category": "Kỹ năng sống"},
    {"title": "Bí Mật Tư Duy Triệu Phú (Bản Mới)", "author": "T. Harv Eker", "price": 160000, "category": "Kỹ năng sống"},
    {"title": "Tâm Lý Học Đám Đông", "author": "Gustave Le Bon", "price": 140000, "category": "Kinh tế"},
    {"title": "Quyền Năng Hiện Tại", "author": "Eckhart Tolle", "price": 150000, "category": "Kỹ năng sống"},
    {"title": "Đời Ngắn Đừng Ngủ Quên", "author": "Robin Sharma", "price": 135000, "category": "Kỹ năng sống"},

    {"title": "Marketing 4.0", "author": "Philip Kotler", "price": 190000, "category": "Kinh tế"},
    {"title": "Copywriting Đỉnh Cao", "author": "Robert W. Bly", "price": 175000, "category": "Kinh tế"},
    {"title": "Influence", "author": "Robert Cialdini", "price": 185000, "category": "Kinh tế"},
    {"title": "Hooked", "author": "Nir Eyal", "price": 155000, "category": "Kinh tế"},
    {"title": "The Art of War", "author": "Tôn Tử", "price": 98000, "category": "Kinh tế"},
    {"title": "Chiến Quốc Sách", "author": "Nhiều tác giả", "price": 110000, "category": "Kinh tế"},
    {"title": "Tam Quốc Diễn Nghĩa", "author": "La Quán Trung", "price": 175000, "category": "Tiểu thuyết"},
    {"title": "Thủy Hử", "author": "Thi Nại Am", "price": 165000, "category": "Tiểu thuyết"},
    {"title": "Tây Du Ký", "author": "Ngô Thừa Ân", "price": 160000, "category": "Tiểu thuyết"},
]

#USERS
USERS = [
    {"username": "nguyenvana", "full_name": "Nguyễn Văn A"},
    {"username": "tranthib", "full_name": "Trần Thị B"},
    {"username": "leminhduc", "full_name": "Lê Minh Đức"},
    {"username": "phamquanghuy", "full_name": "Phạm Quang Huy"},
    {"username": "nguyenthilan", "full_name": "Nguyễn Thị Lan"},
    {"username": "hoangminh", "full_name": "Hoàng Minh"},
    {"username": "phamhuong", "full_name": "Phạm Hương"},
    {"username": "vothanhtrung", "full_name": "Võ Thành Trung"},
    {"username": "dangquocbao", "full_name": "Đặng Quốc Bảo"},
    {"username": "nguyenthanhdat", "full_name": "Nguyễn Thành Đạt"},
    {"username": "buituananh", "full_name": "Bùi Tuấn Anh"},
    {"username": "phamngocanh", "full_name": "Phạm Ngọc Anh"},
    {"username": "lethanhtruc", "full_name": "Lê Thanh Trúc"},
    {"username": "trankhanhlinh", "full_name": "Trần Khánh Linh"},
    {"username": "ngovankhoa", "full_name": "Ngô Văn Khoa"},
    {"username": "doanhthu", "full_name": "Đỗ Anh Thư"},
    {"username": "luukhanhvy", "full_name": "Lưu Khánh Vy"},
    {"username": "phamhoangnam", "full_name": "Phạm Hoàng Nam"},
    {"username": "nguyenductri", "full_name": "Nguyễn Đức Trí"},
    {"username": "vuduykhanh", "full_name": "Vũ Duy Khánh"},
]
#TẠO PROFILE
for user in User.objects.all():
    Profile.objects.get_or_create(
        user=user,
        defaults={
            "gender": random.choice(["Nam", "Nữ", "Khác"]),
            "date_of_birth": date(
                random.randint(1985, 2010),
                random.randint(1, 12),
                random.randint(1, 28)
            )
        }
    )

ADDRESSES = [
    "123 Lê Lợi, Quận 1, TP. Hồ Chí Minh",
    "45 Nguyễn Trãi, Quận 5, TP. Hồ Chí Minh",
    "78 Trần Hưng Đạo, Quận Hoàn Kiếm, Hà Nội",
    "12 Phan Đình Phùng, TP. Huế",
    "90 Cách Mạng Tháng 8, Quận Ninh Kiều, Cần Thơ",
    "56 Điện Biên Phủ, Quận Bình Thạnh, TP. Hồ Chí Minh",
    "34 Lý Thường Kiệt, Quận Hoàn Kiếm, Hà Nội",
    "221 Hai Bà Trưng, Quận 3, TP. Hồ Chí Minh",
    "67 Nguyễn Văn Linh, Quận Thanh Khê, Đà Nẵng",
    "10 Hùng Vương, TP. Nha Trang, Khánh Hòa",
    "88 Lạch Tray, Quận Ngô Quyền, Hải Phòng",
    "15 Quang Trung, TP. Vinh, Nghệ An",
    "101 Phạm Văn Đồng, TP. Thủ Đức, TP. Hồ Chí Minh",
    "202 Nguyễn Huệ, TP. Biên Hòa, Đồng Nai",
    "19 Trần Phú, TP. Đà Lạt, Lâm Đồng",
    "77 Võ Văn Tần, Quận 3, TP. Hồ Chí Minh",
    "5 Lê Duẩn, TP. Buôn Ma Thuột, Đắk Lắk",
    "66 Trần Hưng Đạo, TP. Rạch Giá, Kiên Giang",
    "44 Nguyễn Tất Thành, TP. Pleiku, Gia Lai",
    "9 Lý Tự Trọng, TP. Quy Nhơn, Bình Định",
]

REVIEWS = [
    "Sách có nội dung rất hay, cách trình bày dễ hiểu và phù hợp với nhiều đối tượng người đọc.",
    "Cốt truyện hấp dẫn, các tình tiết được xây dựng hợp lý khiến mình đọc một mạch không muốn dừng lại.",
    "Nội dung sách mang lại nhiều kiến thức bổ ích và giúp mình thay đổi cách suy nghĩ tích cực hơn.",
    "Văn phong mượt mà, dễ đọc, rất phù hợp để đọc thư giãn vào buổi tối.",
    "Sách mang lại nhiều cảm hứng trong cuộc sống và công việc, rất đáng để mua.",
    "Nội dung khá sâu sắc, tuy nhiên có một vài đoạn hơi dài dòng nhưng vẫn rất đáng đọc.",
    "Mình rất thích cách tác giả truyền tải thông điệp một cách nhẹ nhàng nhưng rất thấm.",
    "Đọc xong cảm thấy học được rất nhiều điều bổ ích cho bản thân.",
    "Sách phù hợp cho những ai đang tìm kiếm động lực và định hướng trong cuộc sống.",
    "Một cuốn sách rất ý nghĩa, giúp mình nhìn nhận lại nhiều vấn đề trong cuộc sống.",
    "Nội dung thực tế, ví dụ sinh động, dễ áp dụng vào đời sống hàng ngày.",
    "Đây là một trong những cuốn sách mình thích nhất từ trước đến nay.",
    "Sách đọc rất cuốn, càng đọc càng bị cuốn vào nội dung bên trong.",
    "Thông điệp của sách rất nhân văn, phù hợp với nhiều lứa tuổi.",
    "Cách viết của tác giả rất gần gũi, tạo cảm giác thân thiện khi đọc.",
    "Sách phù hợp để đọc trong những lúc rảnh rỗi hoặc muốn thư giãn đầu óc.",
    "Nội dung hay, bố cục rõ ràng, dễ theo dõi và không bị rối.",
    "Có nhiều đoạn rất hay, đọc xong phải suy ngẫm lại rất lâu.",
    "Cuốn sách giúp mình có thêm động lực để cố gắng hơn mỗi ngày.",
    "Sách mang tính thực tế cao và rất phù hợp cho những ai thích phát triển bản thân.",
    "Văn phong nhẹ nhàng, dễ hiểu, không quá học thuật nên rất dễ tiếp cận.",
    "Có những bài học rất hay và rất gần với những gì mình đang gặp phải.",
    "Đọc rất thoải mái, không bị nặng nề nhưng vẫn mang lại nhiều giá trị.",
    "Sách có nội dung ổn, phù hợp với người mới bắt đầu tìm hiểu chủ đề này.",
    "Nội dung thú vị, cách dẫn dắt câu chuyện rất tự nhiên.",
    "Mình cảm thấy rất hài lòng sau khi đọc xong cuốn sách này.",
    "Một cuốn sách rất đáng để đọc ít nhất một lần trong đời.",
    "Cách tác giả kể chuyện rất thu hút, dễ tạo cảm xúc cho người đọc.",
    "Nội dung truyền tải rất thực tế và dễ liên hệ với cuộc sống.",
    "Đọc xong cảm thấy tinh thần thoải mái và tích cực hơn.",
    "Sách hay, đáng mua, phù hợp đọc lâu dài chứ không bị chán.",
    "Nội dung được trình bày logic, dễ theo dõi từ đầu đến cuối.",
    "Sách rất phù hợp để làm quà tặng cho bạn bè và người thân.",
    "Có nhiều đoạn hay, đọc đi đọc lại vẫn thấy ý nghĩa.",
    "Mình đánh giá cao nội dung và cách viết của cuốn sách này.",
    "Nội dung khá ổn, có thể áp dụng được vào công việc và học tập.",
    "Sách mang lại nhiều góc nhìn mới và thú vị.",
    "Mình thích cách sách phân tích vấn đề rất rõ ràng và dễ hiểu.",
    "Cuốn sách này rất phù hợp để đọc trong những lúc cần thư giãn.",
    "Nội dung gần gũi, dễ đồng cảm với những trải nghiệm mà sách chia sẻ.",
    "Một cuốn sách mang tính truyền cảm hứng rất cao.",
    "Cách viết rất cuốn, đọc một lúc là hết mấy chương.",
    "Nội dung sâu sắc, nhưng vẫn rất dễ hiểu với người mới.",
    "Cuốn sách này giúp mình thay đổi một vài thói quen xấu.",
    "Đọc xong cảm thấy có thêm nhiều động lực để phát triển bản thân.",
    "Sách viết rất chân thực, đọc rất có cảm xúc.",
    "Nội dung phù hợp để đọc nhiều lần mà không bị nhàm chán.",
    "Mình cảm thấy đây là một trong những cuốn sách đáng đọc nhất.",
    "Cách triển khai nội dung rất tự nhiên, không bị gượng ép.",
    "Sách rất phù hợp cho những ai đang cảm thấy mất phương hướng.",
]

#HÀM XOÁ DỮ LIỆU CŨ
def clear_data():
    RecommendationEngine.objects.all().delete()
    Review.objects.all().delete()
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    Book.objects.all().delete()
    Category.objects.all().delete()
    Promotion.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.all().delete()

# SEED CATEGORIES 
def seed_categories():
    return {c: Category.objects.create(name=c) for c in CATEGORIES}

# LẤY ẢNH BÌA TỰ ĐỘNG TỪ OPEN LIBRARY
def get_cover_image(title):
    url = f"https://openlibrary.org/search.json?title={title}"
    try:
        res = requests.get(url).json()
        cover_id = res["docs"][0].get("cover_i")
        if cover_id:
            return f"http://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    except:
        return None
    return None

# SEED BOOKS
def seed_books(category_objs):
    books = []
    for b in BOOKS:
        cat = category_objs[b["category"]]
        book_obj = Book.objects.create(
            title=b["title"],
            author=b["author"],
            price=b["price"],
            description=f"{b['title']} là một trong những cuốn sách bán chạy nhất.",
            category=cat,
            stock=random.randint(5, 50),
            published_date=date.today() - timedelta(days=random.randint(100, 5000))
        )
        books.append(book_obj)  # thêm vào list
    return books  

# SEED USERS + PROFILES + CART 
def seed_users():
    users = []

    for u in USERS:
        # Kiểm tra chắc chắn u là dict
        if not isinstance(u, dict):
            print(f"WARNING: Người dùng không phải dict: {u}")
            continue

        # Tách first_name và last_name từ full_name
        full_name = u.get("full_name", "")
        names = full_name.split(" ", 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ""

        # Tạo user
        user_obj = User.objects.create_user(
            username=u["username"],
            password="123456",  # mật khẩu mặc định
            email=f"{u['username']}@gmail.com",
            phone="09" + str(random.randint(10000000, 99999999)),
            address=random.choice(ADDRESSES),
            first_name=first_name,
            last_name=last_name,
            is_customer=True,
            is_admin=False,
        )

        # Tạo Profile
        Profile.objects.create(
            user=user_obj,
            gender=random.choice(["Nam", "Nữ"]),
            date_of_birth=date.today() - timedelta(days=random.randint(7000, 12000))
        )

        # Tạo Cart trống
        Cart.objects.create(user=user_obj)

        # Thêm vào list
        users.append(user_obj)

    return users

# SEED PROMOTIONS
def seed_promotions():
    return [
        Promotion.objects.create(
            code="SALE10",
            name="Giảm 10%",
            discount_percent=10,
            description="Giảm 10% cho đơn từ 100.000đ",
            applicable_price=100000,
            quantity=100,
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() + timedelta(days=20),
        ),
        Promotion.objects.create(
            code="FREESHIP50",
            name="Miễn phí ship 50k",
            discount_percent=random.randint(5, 30),
            description="Miễn phí ship 50.000đ cho đơn từ 150.000đ",
            applicable_price=150000,
            quantity=100,
            start_date=date.today() - timedelta(days=7),
            end_date=date.today() + timedelta(days=15),
        )
    ]

# SEED ORDERS + ITEMS 
def seed_orders(users, books, promotions):
    for u in users:
        order = Order.objects.create(
            user=u,
            status=random.choice(["Pending", "Shipped", "Completed"]),
            promotion=random.choice(promotions + [None])
        )

        for _ in range(random.randint(1, 3)):
            b = random.choice(books)
            qty = random.randint(1, 3)

            OrderItem.objects.create(
                order=order,
                book=b,                
                quantity=qty,
                price=b.price,         
            )

        # Cập nhật tổng tiền
        order.total_price = sum(item.price * item.quantity for item in order.items.all())
        order.total_amount = order.total_price
        order.save()


# SEED SHIPPING INFO
def seed_shipping_info():
    """
    Tạo ShippingInfo cho tất cả Order chưa có (order.shipping is None).
    Dùng order.user.address nếu có, nếu không thì random từ ADDRESSES.
    """
    # đảm bảo ADDRESSES tồn tại
    try:
        _ = ADDRESSES
    except NameError:
        print("ERROR: ADDRESSES không được định nghĩa.")
        return

    orders_without_shipping = Order.objects.filter(shipping__isnull=True)

    for order in orders_without_shipping:
        user = getattr(order, "user", None)
        username = getattr(user, "username", "Người nhận")
        phone = getattr(user, "phone", None) or ("09" + str(random.randint(10000000, 99999999)))
        raw_address = getattr(user, "address", None)

        # nếu user.address rỗng -> lấy ngẫu nhiên từ ADDRESSES
        if not raw_address:
            raw_address = random.choice(ADDRESSES)

        # raw_address dạng: "số + đường, Quận X, TP. Y"
        parts = [p.strip() for p in raw_address.split(",")]

        # mặc định
        address_line = parts[0] if len(parts) >= 1 else raw_address
        district = parts[1] if len(parts) >= 2 else ""
        city = parts[2] if len(parts) >= 3 else ""

        # chuẩn hoá một chút (nếu district chứa từ 'Quận' hay 'Quận X' giữ nguyên)
        if district and not any(k in district.lower() for k in ["quận", "huyện", "tp.", "tp"]):
            # nếu district chưa có tiền tố, cố gắng thêm "Quận"
            if district.isdigit():
                district = f"Quận {district}"
        if city and not any(k in city.lower() for k in ["tp.", "tỉnh", "tp", "thành phố"]):
            # nếu city là tên thành phố ngắn, giữ nguyên
            pass

        note = f"Tạo tự động vào {date.today().isoformat()}"

        # tạo ShippingInfo cho order nếu chưa có
        try:
            ShippingInfo.objects.create(
                order=order,
                full_name=username,
                phone=phone,
                address=address_line,
                city=city or "Không rõ",
                district=district or "Không rõ",
                ward=f"Phường {random.randint(1,20)}",
                note=note
            )
        except Exception as e:
            print(f"Lỗi khi tạo ShippingInfo cho Order id={getattr(order,'id',None)}: {e}")

# SEED REVIEWS
def seed_reviews(users, books):
    for _ in range(20):
        Review.objects.create(
            user=random.choice(users),
            book=random.choice(books),
            content=random.choice(REVIEWS),
            rating=random.randint(3, 5)
        )

# TẠO GIỎ HÀNG
for user in User.objects.all():
    Cart.objects.get_or_create(user=user)

# SEED CART ITEMS
def seed_cart_items(users, books):
    for u in users:
        cart = u.cart
        for _ in range(random.randint(1, 3)):
            CartItem.objects.create(
                cart=cart,
                book=random.choice(books),
                quantity=random.randint(1, 3)
            )

def seed_recommendations(users, books):
    real_users = {u.id: u for u in User.objects.all()}  # map user thật trong DB

    for user in users:
        if user.id not in real_users:
            print(f"BỎ QUA user id={user.id} (không tồn tại trong DB)")
            continue

        user_obj = real_users[user.id]

        # tạo engine nếu chưa có
        engine, created = RecommendationEngine.objects.get_or_create(user=user_obj)

        # random 5–10 sách để đưa vào lịch sử mua hàng (order_history)
        purchased_books = random.sample(list(books), random.randint(3, 10))

        engine.order_history.set(purchased_books)
        engine.save()

        print(f"Đã tạo RecommendationEngine cho user {user_obj.id}")

# RUN SEED
if __name__ == "__main__":
    print("Xoá dữ liệu cũ...")
    clear_data()

    print("Seeding categories...")
    category_objs = seed_categories()

    print("Seeding books...")
    books = seed_books(category_objs)

    print("Seeding users...")
    users = seed_users()

    print("Seeding promotions...")
    promotions = seed_promotions()

    print("Seeding cart items...")
    seed_cart_items(users, books)

    print("Seeding orders...")
    seed_orders(users, books, promotions)

    print("Seeding shipping info...") 
    seed_shipping_info() 

    print("Seeding reviews...")
    seed_reviews(users, books)

    print("Seeding recommendations...")
    seed_recommendations(users, books)

    print("Seed dữ liệu hoàn tất!")
