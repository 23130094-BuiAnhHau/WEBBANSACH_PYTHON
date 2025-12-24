\encoding UTF8
-- User 
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(254),
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    phone VARCHAR(15),
    address TEXT,
    role VARCHAR(20) NOT NULL DEFAULT 'user');

-- Profile
CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    avatar VARCHAR(255),
    date_of_birth DATE,
    gender VARCHAR(10) CHECK (gender IN ('Nam', 'Nữ', 'Khác')));

-- Bảng Category
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL);

-- Bảng Author
CREATE TABLE author (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT);

-- Bảng Book
CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    sale_price NUMERIC(10,2),
    stock INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER REFERENCES category(id) ON DELETE SET NULL,
    author_id INTEGER REFERENCES author(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    average_rating REAL DEFAULT 0);

-- Bảng BookImage
CREATE TABLE book_image (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES book(id) ON DELETE CASCADE,
    image VARCHAR(255) NOT NULL);

-- Bảng Review
CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES book(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    rating SMALLINT NOT NULL DEFAULT 5,
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_book_user UNIQUE (book_id, user_id));

-- Bảng FavoriteBook
CREATE TABLE favorite_book (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    book_id INTEGER REFERENCES book(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_book UNIQUE (user_id, book_id));
	
-- Bảng BookViewHistory
CREATE TABLE book_view_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    book_id INTEGER REFERENCES book(id) ON DELETE CASCADE,
    viewed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);

-- Bảng Cart
CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);

-- Bảng CartItem
CREATE TABLE cart_item (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES cart(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES book(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 1),
    price NUMERIC(10,2) NOT NULL,
    CONSTRAINT unique_cart_book UNIQUE (cart_id, book_id));

-- Voucher
CREATE TABLE voucher (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    voucher_type VARCHAR(10) NOT NULL,
    discount_value NUMERIC(12,2) NOT NULL,
    min_order_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE);

-- UserVoucher
CREATE TABLE user_voucher (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    voucher_id INTEGER NOT NULL REFERENCES voucher(id) ON DELETE CASCADE,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    claimed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_voucher UNIQUE (user_id, voucher_id));

-- PromoCode
CREATE TABLE promo_code (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    discount_percent INTEGER NOT NULL DEFAULT 0,
    discount_amount INTEGER NOT NULL DEFAULT 0,
    min_order_amount INTEGER NOT NULL DEFAULT 0,
    valid_from TIMESTAMP WITH TIME ZONE NOT NULL,
    valid_to TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE);

-- Order
CREATE TABLE "order" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    payment_method VARCHAR(10) NOT NULL DEFAULT 'COD',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    shipping_address TEXT,
    user_voucher_id INTEGER REFERENCES user_voucher(id) ON DELETE SET NULL,
    promo_code_id INTEGER REFERENCES promo_code(id) ON DELETE SET NULL,
    total_price NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00);

-- OrderItem
CREATE TABLE order_item (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES "order"(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES book(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1,
    price NUMERIC(12,2) NOT NULL);

-- RecommendationEngine
CREATE TABLE recommendation_engine (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);

-- Bảng trung gian cho ManyToMany (order_history)
CREATE TABLE recommendation_engine_order_history (
    recommendation_engine_id INTEGER NOT NULL REFERENCES recommendation_engine(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES book(id) ON DELETE CASCADE,
    PRIMARY KEY (recommendation_engine_id, book_id));

-- Banner
CREATE TABLE banner (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    subtitle VARCHAR(300) NOT NULL,
    image VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE);

-- Promotion
CREATE TABLE promotion (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    discount_percent INTEGER NOT NULL CHECK (discount_percent >= 0 AND discount_percent <= 100),
    expire_date DATE NOT NULL);

-- CustomerPromotion
CREATE TABLE customer_promotion (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    promo_type VARCHAR(20) NOT NULL CHECK (promo_type IN ('NEW', 'VIP', 'BIRTHDAY')),
    discount_percent INTEGER NOT NULL DEFAULT 0,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE);

-- Bảng ProductDiscount
CREATE TABLE product_discount (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES book(id) ON DELETE CASCADE,
    discount_percent INTEGER NOT NULL DEFAULT 0,
    discount_amount INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE);

-- Bảng RecommendationCache
CREATE TABLE recommendation_cache (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    book_id INTEGER REFERENCES book(id) ON DELETE CASCADE,
    score REAL NOT NULL DEFAULT 0.0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);

----------- 40 users --------------
INSERT INTO "user" (username, password, email, first_name, last_name, is_staff, is_active, is_superuser, last_login, date_joined, phone, address, role)
VALUES
('nguyen.hoan', 'password123', 'nguyen.hoan@gmail.com', 'Nguyễn', 'Hoàn', FALSE, TRUE, FALSE, '2025-12-05', '2025-12-02', '0912345671', 'Quận 1, Hà Nội', 'user'),
('tran.anh', 'password123', 'tran.anh@gmail.com', 'Trần', 'Anh', FALSE, TRUE, FALSE, '2025-12-05', '2025-12-05', '0912345672', 'Quận 3, Hồ Chí Minh', 'user'),
('le.hieu', 'password123', 'le.hieu@gmail.com', 'Lê', 'Hiếu', FALSE, TRUE, FALSE, '2025-12-15', '2025-12-07', '0912345673', 'Quận Hải Châu, Đà Nẵng', 'user'),
('pham.tu', 'password123', 'pham.tu@gmail.com', 'Phạm', 'Tú', FALSE, TRUE, FALSE, '2025-12-03', '2025-12-01', '0912345674', 'Quận Ngô Quyền, Hải Phòng', 'user'),
('doan.linh', 'password123', 'doan.linh@gmail.com', 'Đoàn', 'Linh', FALSE, TRUE, FALSE, '2025-12-20', '2025-12-10', '0912345675', 'Quận Ninh Kiều, Cần Thơ', 'user'),
('vu.thanh', 'password123', 'vu.thanh@gmail.com', 'Vũ', 'Thanh', FALSE, TRUE, FALSE, '2025-12-13', '2025-12-12', '0912345676', 'Quận Ba Đình, Hà Nội', 'user'),
('hoang.ngoc', 'password123', 'hoang.ngoc@gmail.com', 'Hoàng', 'Ngọc', FALSE, TRUE, FALSE, '2025-12-15', '2025-12-03', '0912345677', 'Quận 5, Hồ Chí Minh', 'user'),
('nguyen.trung', 'password123', 'nguyen.trung@gmail.com', 'Nguyễn', 'Trung', FALSE, TRUE, FALSE, '2025-12-19', '2025-12-08', '0912345678', 'Quận Sơn Trà, Đà Nẵng', 'user'),
('tran.quang', 'password123', 'tran.quang@gmail.com', 'Trần', 'Quang', FALSE, TRUE, FALSE, '2025-12-25', '2025-12-15', '0912345679', 'Quận Lê Chân, Hải Phòng', 'user'),
('le.thao', 'password123', 'le.thao@gmail.com', 'Lê', 'Thảo', FALSE, TRUE, FALSE,'2025-12-22', '2025-12-20', '0912345680', 'Quận Bình Thủy, Cần Thơ', 'user'),
('pham.ha', 'password123', 'pham.ha@gmail.com', 'Phạm', 'Hà', FALSE, TRUE, FALSE, '2025-01-03', '2025-12-18', '0912345681', 'Quận Đống Đa, Hà Nội', 'user'),
('doan.phuc', 'password123', 'doan.phuc@gmail.com', 'Đoàn', 'Phúc', FALSE, TRUE, FALSE, '2025-12-25', '2025-12-22', '0912345682', 'Quận Tân Phú, Hồ Chí Minh', 'user'),
('vu.hien', 'password123', 'vu.hien@gmail.com', 'Vũ', 'Hiền', FALSE, TRUE, FALSE,'2025-12-09', '2025-12-04', '0912345683', 'Quận Thanh Khê, Đà Nẵng', 'user'),
('hoang.minh', 'password123', 'hoang.minh@gmail.com', 'Hoàng', 'Minh', FALSE, TRUE, FALSE, '2025-01-05', '2025-12-25', '0912345684', 'Quận Hồng Bàng, Hải Phòng', 'user'),
('nguyen.ha', 'password123', 'nguyen.ha@gmail.com', 'Nguyễn', 'Hà', FALSE, TRUE, FALSE, '2025-12-30', '2025-12-28', '0912345685', 'Quận Cái Răng, Cần Thơ', 'user'),
('tran.tuan', 'password123', 'tran.tuan@gmail.com', 'Trần', 'Tuấn', FALSE, TRUE, FALSE, '2025-12-06', '2025-12-06', '0912345686', 'Quận Hai Bà Trưng, Hà Nội', 'user'),
('le.nam', 'password123', 'le.nam@gmail.com', 'Lê', 'Nam', FALSE, TRUE, FALSE, '2025-12-17', '2025-12-09', '0912345687', 'Quận Phú Nhuận, Hồ Chí Minh', 'user'),
('pham.anh', 'password123', 'pham.anh@gmail.com', 'Phạm', 'Anh', FALSE, TRUE, FALSE, '2025-12-21', '2025-12-11', '0912345688', 'Quận Ngũ Hành Sơn, Đà Nẵng', 'user'),
('doan.trang', 'password123', 'doan.trang@gmail.com', 'Đoàn', 'Trang', FALSE, TRUE, FALSE, '2025-12-23', '2025-12-13', '0912345689', 'Quận Kiến An, Hải Phòng', 'user'),
('vu.hoang', 'password123', 'vu.hoang@gmail.com', 'Vũ', 'Hoàng', FALSE, TRUE, FALSE, '2025-12-15', '2025-12-14', '0912345690', 'Quận Ninh Kiều, Cần Thơ', 'user'),
('hoang.lan', 'password123', 'hoang.lan@gmail.com', 'Hoàng', 'Lan', FALSE, TRUE, FALSE, '2025-12-16', '2025-12-16', '0912345691', 'Quận Hoàn Kiếm, Hà Nội', 'user'),
('nguyen.duy', 'password123', 'nguyen.duy@gmail.com', 'Nguyễn', 'Duy', FALSE, TRUE, FALSE, '2025-12-27', '2025-12-17', '0912345692', 'Quận 7, Hồ Chí Minh', 'user'),
('tran.ha', 'password123', 'tran.ha@gmail.com', 'Trần', 'Hà', FALSE, TRUE, FALSE, '2025-12-22', '2025-12-19', '0912345693', 'Quận Hải Châu, Đà Nẵng', 'user'),
('le.phuong', 'password123', 'le.phuong@gmail.com', 'Lê', 'Phương', FALSE, TRUE, FALSE, '2025-12-29', '2025-12-21', '0912345694', 'Quận Hồng Bàng, Hải Phòng', 'user'),
('pham.tung', 'password123', 'pham.tung@gmail.com', 'Phạm', 'Tùng', FALSE, TRUE, FALSE, '2025-12-25', '2025-12-23', '0912345695', 'Quận Bình Thủy, Cần Thơ', 'user'),
('doan.van', 'password123', 'doan.van@gmail.com', 'Đoàn', 'Văn', FALSE, TRUE, FALSE, '2025-12-29', '2025-12-24', '0912345696', 'Quận Ba Đình, Hà Nội', 'user'),
('vu.mai', 'password123', 'vu.mai@gmail.com', 'Vũ', 'Mai', FALSE, TRUE, FALSE, '2025-12-30', '2025-12-26', '0912345697', 'Quận 10, Hồ Chí Minh', 'user'),
('hoang.phi', 'password123', 'hoang.phi@gmail.com', 'Hoàng', 'Phi', FALSE, TRUE, FALSE, '2025-12-28', '2025-12-27', '0912345698', 'Quận Cẩm Lệ, Đà Nẵng', 'user'),
('nguyen.ngoc', 'password123', 'nguyen.ngoc@gmail.com', 'Nguyễn', 'Ngọc', FALSE, TRUE, FALSE, '2025-12-29', '2025-12-29', '0912345699', 'Quận Ngô Quyền, Hải Phòng', 'user'),
('tran.hien', 'password123', 'tran.hien@gmail.com', 'Trần', 'Hiền', FALSE, TRUE, FALSE, '2025-12-30', '2025-12-30', '0912345700', 'Quận Bình Thủy, Cần Thơ', 'user'),
('le.ha', 'password123', 'le.ha@gmail.com', 'Lê', 'Hà', FALSE, TRUE, FALSE, '2025-01-01', '2025-12-03', '0912345701', 'Quận Tây Hồ, Hà Nội', 'user'),
('pham.trang', 'password123', 'pham.trang@gmail.com', 'Phạm', 'Trang', FALSE, TRUE, FALSE, '2025-12-05', '2025-12-05', '0912345702', 'Quận Gò Vấp, Hồ Chí Minh', 'user'),
('doan.hieu', 'password123', 'doan.hieu@gmail.com', 'Đoàn', 'Hiếu', FALSE, TRUE, FALSE, '2025-12-09', '2025-12-07', '0912345703', 'Quận Liên Chiểu, Đà Nẵng', 'user'),
('vu.tu', 'password123', 'vu.tu@gmail.com', 'Vũ', 'Tú', FALSE, TRUE, FALSE, '2025-12-15', '2025-12-09', '0912345704', 'Quận Kiến An, Hải Phòng', 'user'),
('hoang.thanh', 'password123', 'hoang.thanh@gmail.com', 'Hoàng', 'Thanh', FALSE, TRUE, FALSE, '2025-12-13', '2025-12-11', '0912345705', 'Quận Thốt Nốt, Cần Thơ', 'user'),
('nguyen.phat', 'password123', 'nguyen.phat@gmail.com', 'Nguyễn', 'Phát', FALSE, TRUE, FALSE, '2025-12-15', '2025-12-13', '0912345706', 'Quận Cầu Giấy, Hà Nội', 'user'),
('tran.linh', 'password123', 'tran.linh@gmail.com', 'Trần', 'Linh', FALSE, TRUE, FALSE, '2025-12-25', '2025-12-15', '0912345707', 'Quận Tân Bình, Hồ Chí Minh', 'user'),
('le.tuan', 'password123', 'le.tuan@gmail.com', 'Lê', 'Tuấn', FALSE, TRUE, FALSE, '2025-12-18', '2025-12-17', '0912345708', 'Quận Thanh Khê, Đà Nẵng', 'user'),
('pham.hien', 'password123', 'pham.hien@gmail.com', 'Phạm', 'Hiền', FALSE, TRUE, FALSE, '2025-12-26', '2025-12-19', '0912345709', 'Quận Lê Chân, Hải Phòng', 'user'),
('doan.mai', 'password123', 'doan.mai@gmail.com', 'Đoàn', 'Mai', FALSE, TRUE, FALSE, '2025-12-30', '2025-12-21', '0912345710', 'Quận Ninh Kiều, Cần Thơ', 'user');

------------- 40 profile cho 40 user------------------
INSERT INTO profile (user_id, avatar, date_of_birth, gender)
VALUES
(1, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg/', '1995-03-12', 'Nam'),
(2, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1992-07-25', 'Nữ'),
(3, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1988-11-05', 'Nam'),
(4, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2000-06-18', 'Nữ'),
(5, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2002-01-20','Nam'),
(6, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1993-01-20', 'Nữ'),
(7, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1990-12-30', 'Nam'),
(8, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2002-04-14', 'Khác'),
(9, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1996-08-22', 'Nữ'),
(10, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1994-05-11', 'Nam'),
(11, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1989-02-28', 'Nam'),
(12, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2001-07-07', 'Nữ'),
(13, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1997-10-16', 'Nam'),
(14, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1995-12-05', 'Nữ'),
(15, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1991-03-21', 'Nam'),
(16, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2000-08-19', 'Nữ'),
(17, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1993-11-29', 'Nam'),
(18, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1999-06-02', 'Nữ'),
(19, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1992-09-17', 'Nam'),
(20, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2003-01-12', 'Nữ'),
(21, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1990-05-08', 'Nam'),
(22, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1996-03-23', 'Nữ'),
(23, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1987-12-11', 'Nam'),
(24, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2001-09-14', 'Khác'),
(25, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1994-06-30', 'Nam'),
(26, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1998-11-02', 'Nữ'),
(27, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1995-02-26', 'Nam'),
(28, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2002-05-19', 'Nữ'),
(29, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1997-08-23', 'Nam'),
(30, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1993-12-15', 'Nữ'),
(31, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1991-07-04', 'Nam'),
(32, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2000-03-09', 'Nữ'),
(33, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1989-10-28', 'Nam'),
(34, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1996-01-17', 'Nữ'),
(35, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1992-04-21', 'Nam'),
(36, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2001-08-05', 'Nữ'),
(37, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1994-09-12', 'Nam'),
(38, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1999-11-22', 'Nữ'),
(39, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '1995-06-30', 'Nam'),
(40, 'https://i.pinimg.com/736x/bc/43/98/bc439871417621836a0eeea768d60944.jpg', '2002-02-14', 'Khác');


--------------- Thêm dữ liệu cho Category (15 loại)----------------
INSERT INTO category (name, slug) VALUES
('Văn học Việt Nam', 'van-hoc-viet-nam'),
('Văn học nước ngoài', 'van-hoc-nuoc-ngoai'),
('Sách thiếu nhi', 'sach-thieu-nhi'),
('Kinh tế - Quản trị', 'kinh-te-quan-tri'),
('Khoa học - Công nghệ', 'khoa-hoc-cong-nghe'),
('Tâm lý - Kỹ năng sống', 'tam-ly-ky-nang-song'),
('Tiểu thuyết', 'tieu-thuyet'),
('Giáo dục - Học tập', 'giao-duc-hoc-tap'),
('Sách tham khảo', 'sach-tham-khao'),
('Sách kỹ năng sống', 'sach-ky-nang-song'),
('Lịch sử - Địa lý', 'lich-su-dia-ly'),
('Nghệ thuật - Hội họa', 'nghe-thuat-hoi-hoa'),
('Sách ngoại ngữ', 'sach-ngoai-ngu'),
('Sách y học - Sức khỏe', 'sach-y-hoc-suc-khoe'),
('Truyện tranh', 'truyen-tranh');


------------- 75 tác giả-----------
INSERT INTO author (name, bio) VALUES
-- Văn học Việt Nam
('Nguyễn Nhật Ánh', 'Chuyên viết văn học Việt Nam và truyện thiếu nhi'),
('Tô Hoài', 'Nhà văn nổi tiếng văn học Việt Nam'),
('Nam Cao', 'Chuyên văn học hiện thực Việt Nam'),
('Nguyễn Huy Thiệp', 'Nhà văn văn học đương đại'),
('Bảo Ninh', 'Tác giả văn học chiến tranh'),
-- Văn học nước ngoài
('Haruki Murakami', 'Tiểu thuyết gia Nhật Bản'),
('Paulo Coelho', 'Nhà văn Brazil'),
('George Orwell', 'Nhà văn Anh'),
('J.K. Rowling', 'Tác giả Harry Potter'),
('Ernest Hemingway', 'Nhà văn Mỹ'),
-- Sách thiếu nhi
('Roald Dahl', 'Chuyên sách thiếu nhi'),
('Enid Blyton', 'Tác giả truyện thiếu nhi'),
('Astrid Lindgren', 'Nhà văn thiếu nhi Thụy Điển'),
('Dr. Seuss', 'Sách thiếu nhi sáng tạo'),
('Julia Donaldson', 'Tác giả thiếu nhi'),
-- Kinh tế - Quản trị
('Peter Drucker', 'Chuyên gia quản trị'),
('Philip Kotler', 'Marketing hiện đại'),
('Michael Porter', 'Chiến lược kinh doanh'),
('Jim Collins', 'Quản trị doanh nghiệp'),
('Stephen Covey', 'Lãnh đạo và quản lý'),
-- Khoa học - Công nghệ
('Stephen Hawking', 'Vật lý học'),
('Elon Musk', 'Công nghệ và đổi mới'),
('Andrew Ng', 'Trí tuệ nhân tạo'),
('Tim Berners-Lee', 'Cha đẻ WWW'),
('Dennis Ritchie', 'Người tạo ra C'),
-- Tâm lý - Kỹ năng sống
('Dale Carnegie', 'Kỹ năng giao tiếp'),
('Tony Robbins', 'Phát triển bản thân'),
('Daniel Goleman', 'Trí tuệ cảm xúc'),
('Jordan Peterson', 'Tâm lý học'),
('Carol Dweck', 'Tư duy phát triển'),
-- Tiểu thuyết
('Dan Brown', 'Tiểu thuyết trinh thám'),
('Agatha Christie', 'Trinh thám cổ điển'),
('Arthur Conan Doyle', 'Sherlock Holmes'),
('Suzanne Collins', 'Tiểu thuyết giả tưởng'),
('George R.R. Martin', 'Fantasy'),
-- Giáo dục - Học tập
('Ken Robinson', 'Giáo dục sáng tạo'),
('Salman Khan', 'Giáo dục trực tuyến'),
('Howard Gardner', 'Đa trí tuệ'),
('Sugata Mitra', 'Giáo dục mở'),
('John Dewey', 'Triết lý giáo dục'),
-- Sách tham khảo
('Nguyễn Văn A', 'Biên soạn sách tham khảo'),
('Trần Văn B', 'Tác giả sách luyện thi'),
('Lê Văn C', 'Sách ôn tập học sinh'),
('Phạm Văn D', 'Sách tham khảo đại học'),
('Hoàng Văn E', 'Tài liệu học thuật'),
-- Sách kỹ năng sống
('Brian Tracy', 'Quản lý thời gian'),
('Robin Sharma', 'Lãnh đạo bản thân'),
('James Clear', 'Thói quen tích cực'),
('Cal Newport', 'Tập trung sâu'),
('Mark Manson', 'Tư duy thực tế'),
-- Lịch sử - Địa lý
('Yuval Noah Harari', 'Lịch sử nhân loại'),
('Will Durant', 'Lịch sử thế giới'),
('Nguyễn Phan Quang', 'Lịch sử Việt Nam'),
('Trần Quốc Vượng', 'Địa lý và lịch sử'),
('Jared Diamond', 'Lịch sử môi trường'),
-- Nghệ thuật - Hội họa
('Leonardo da Vinci', 'Nghệ thuật Phục Hưng'),
('Pablo Picasso', 'Hội họa hiện đại'),
('Vincent van Gogh', 'Hội họa hậu ấn tượng'),
('Claude Monet', 'Trường phái ấn tượng'),
('Frida Kahlo', 'Nghệ thuật cá nhân'),
-- Sách ngoại ngữ
('Raymond Murphy', 'Ngữ pháp tiếng Anh'),
('Michael Swan', 'Ngôn ngữ học'),
('Paul Nation', 'Từ vựng'),
('Jack Richards', 'Giảng dạy ngoại ngữ'),
('David Nunan', 'Ngôn ngữ học ứng dụng'),
-- Sách y học - Sức khỏe
('Deepak Chopra', 'Sức khỏe tinh thần'),
('Atul Gawande', 'Y học hiện đại'),
('Andrew Weil', 'Y học tích hợp'),
('Michael Greger', 'Dinh dưỡng'),
('David Sinclair', 'Chống lão hóa'),
-- Truyện tranh
('Eiichiro Oda', 'One Piece'),
('Akira Toriyama', 'Dragon Ball'),
('Masashi Kishimoto', 'Naruto'),
('Isayama Hajime', 'Attack on Titan'),
('Osamu Tezuka', 'Cha đẻ manga');

--------------- thêm dữ liệu cho sách 151 quyển ----------------------
INSERT INTO book (title, slug, description, price, sale_price, stock, category_id, author_id, created_at, updated_at, average_rating)
VALUES
-- Văn học Việt Nam 
('Cho tôi xin một vé đi tuổi thơ','cho-toi-xin-mot-ve-di-tuoi-tho',
'Tác phẩm nổi tiếng của Nguyễn Nhật Ánh, tái hiện lại thế giới tuổi thơ hồn nhiên, trong sáng với những trò chơi, suy nghĩ ngây ngô nhưng đầy triết lý. Cuốn sách mang đến cảm xúc hoài niệm sâu sắc cho người lớn và sự gần gũi cho thiếu nhi.',
120000,95000,50,1,1,'2025-12-02','2025-12-05',4.8),
('Tôi thấy hoa vàng trên cỏ xanh','toi-thay-hoa-vang-tren-co-xanh',
'Một câu chuyện nhẹ nhàng về làng quê Việt Nam, tình anh em, tình bạn và những rung động đầu đời. Tác phẩm khắc họa tuổi thơ nghèo khó nhưng đầy ắp yêu thương, được viết bằng giọng văn trong trẻo và giàu cảm xúc.',
130000,110000,40,1,1,'2025-12-08','2025-12-12',4.7),
('Dế mèn phiêu lưu ký','de-men-phieu-luu-ky',
'Tác phẩm kinh điển của nhà văn Tô Hoài, kể về hành trình phiêu lưu của Dế Mèn qua nhiều vùng đất khác nhau. Cuốn sách truyền tải bài học sâu sắc về lòng dũng cảm, sự trưởng thành và trách nhiệm đối với cộng đồng.',
90000,80000,60,1,2,'2025-12-01','2025-12-04',4.6),
('Chí Phèo','chi-pheo',
'Tác phẩm tiêu biểu của Nam Cao phản ánh hiện thực xã hội Việt Nam trước Cách mạng tháng Tám. Qua bi kịch cuộc đời Chí Phèo, tác giả lên án xã hội phong kiến bất công và bày tỏ niềm xót thương sâu sắc đối với người nông dân.',
85000,78000,35,1,3,'2025-12-06','2025-12-09',4.5),
('Tướng về hưu','tuong-ve-huu',
'Tác phẩm của Nguyễn Huy Thiệp phản ánh những mâu thuẫn trong đời sống hiện đại khi các giá trị truyền thống va chạm với thực tế xã hội mới. Câu chuyện giàu tính triết lý và mang đậm hơi thở thời cuộc.',
100000,90000,30,1,4,'2025-12-10','2025-12-14',4.4),
('Nỗi buồn chiến tranh','noi-buon-chien-tranh',
'Một trong những tiểu thuyết xuất sắc nhất viết về chiến tranh Việt Nam. Tác phẩm khắc họa nỗi đau, mất mát và ám ảnh tinh thần của người lính sau chiến tranh, với lối viết giàu chiều sâu tâm lý.',
140000,125000,28,1,5,'2025-12-03','2025-12-07',4.6),
('Số đỏ','so-do',
'Tác phẩm trào phúng nổi tiếng của Vũ Trọng Phụng, phản ánh xã hội Việt Nam thời kỳ nửa thực dân nửa phong kiến. Qua nhân vật Xuân Tóc Đỏ, tác giả phê phán sâu cay lối sống lố lăng và giả tạo.',
90000,80000,30,1,3,'2025-12-11','2025-12-15',4.5),
('Tuổi thơ dữ dội','tuoi-tho-du-doi',
'Câu chuyện cảm động về những thiếu niên tham gia kháng chiến trong thời kỳ chiến tranh. Tác phẩm ca ngợi tinh thần yêu nước, sự dũng cảm và hy sinh của thế hệ trẻ Việt Nam.',
120000,110000,35,1,2,'2025-12-05','2025-12-08',4.6),
('Bến không chồng','ben-khong-chong',
'Tác phẩm phản ánh số phận bi thương của những người phụ nữ trong và sau chiến tranh. Cuốn tiểu thuyết mang đậm chất hiện thực, thể hiện nỗi cô đơn, mất mát và khát vọng hạnh phúc.',
95000,88000,28,1,3,'2025-12-04','2025-12-06',4.4),
('Mảnh đất màu mỡ','manh-dat-mau-mo',
'Một tác phẩm viết về chiến tranh và hậu chiến, phản ánh sự thay đổi của con người và xã hội trong thời kỳ khó khăn. Câu chuyện mang nhiều tầng ý nghĩa và giá trị nhân văn sâu sắc.',
100000,90000,25,1,5,'2025-12-09','2025-12-13',4.5),
('Vợ chồng A Phủ','vo-chong-a-phu',
'Tác phẩm của Tô Hoài viết về cuộc sống và số phận của đồng bào dân tộc miền núi Tây Bắc trước Cách mạng. Câu chuyện ca ngợi khát vọng tự do và sức sống mãnh liệt của con người.',
85000,78000,30,1,4,'2025-12-12','2025-12-16',4.6),

-- Văn học nước ngoài
('Rừng Na Uy','rung-na-uy',
'Tiểu thuyết nổi tiếng của Haruki Murakami, xoay quanh những rung động tình yêu, nỗi cô đơn và sự mất mát của tuổi trẻ. Tác phẩm mang không khí trầm lắng, giàu chất tự sự, phản ánh những khủng hoảng tinh thần và hành trình tìm kiếm ý nghĩa sống của con người.',
150000,135000,40,2,6,'2025-12-02','2025-12-06',4.5),
('Nhà giả kim','nha-gia-kim',
'Một câu chuyện mang đậm màu sắc triết lý về hành trình theo đuổi ước mơ và khám phá bản thân. Tác phẩm truyền cảm hứng mạnh mẽ, khuyến khích con người tin vào định mệnh, lắng nghe trái tim và dũng cảm bước ra khỏi vùng an toàn.',
120000,105000,45,2,7,'2025-12-03','2025-12-07',4.6),
('1984','1984',
'Tác phẩm kinh điển của George Orwell, mô tả một xã hội toàn trị nơi con người bị kiểm soát tuyệt đối về tư tưởng và hành vi. Cuốn sách là lời cảnh tỉnh sâu sắc về quyền lực, tự do cá nhân và sự thao túng thông tin.',
150000,135000,50,2,8,'2025-12-04','2025-12-09',4.7),
('Harry Potter và Hòn đá Phù thủy','harry-potter-1',
'Tập đầu tiên trong loạt truyện huyền thoại Harry Potter, đưa người đọc bước vào thế giới phép thuật đầy màu sắc. Câu chuyện xoay quanh tình bạn, lòng dũng cảm và cuộc chiến giữa thiện và ác, phù hợp cho cả thiếu nhi và người lớn.',
180000,165000,60,2,9,'2025-12-06','2025-12-10',4.9),
('Ông già và biển cả','ong-gia-va-bien-ca',
'Tác phẩm nổi tiếng của Ernest Hemingway kể về cuộc chiến bền bỉ giữa con người và thiên nhiên. Qua hình ảnh ông lão đánh cá, cuốn sách ca ngợi ý chí kiên cường, lòng quả cảm và phẩm giá của con người.',
110000,98000,38,2,10,'2025-12-08','2025-12-12',4.6),
('Bí mật của Naoko','bi-mat-cua-naoko',
'Một tiểu thuyết trinh thám tâm lý của Keigo Higashino, kết hợp giữa yếu tố phá án và những mâu thuẫn nội tâm phức tạp. Câu chuyện lôi cuốn người đọc bằng các tình tiết bất ngờ và chiều sâu cảm xúc.',
150000,135000,40,2,6,'2025-12-11','2025-12-15',4.5),
('Alchemist','alchemist',
'Phiên bản tiếng Anh của tác phẩm nổi tiếng "Nhà giả kim", mang thông điệp mạnh mẽ về ước mơ, định mệnh và hành trình tự khám phá. Cuốn sách được yêu thích trên toàn thế giới nhờ lối viết giản dị nhưng đầy ý nghĩa.',
120000,105000,45,2,7,'2025-12-13','2025-12-17',4.6),
('Animal Farm','animal-farm',
'Một tác phẩm châm biếm chính trị sâu sắc của George Orwell, sử dụng hình ảnh các loài vật để phản ánh xã hội loài người. Cuốn sách phê phán sự tha hóa của quyền lực và sự phản bội các lý tưởng ban đầu.',
140000,130000,50,2,8,'2025-12-14','2025-12-18',4.7),
('Harry Potter và Phòng chứa bí mật','harry-potter-2',
'Tập thứ hai trong loạt truyện Harry Potter, tiếp tục mở rộng thế giới phép thuật và những bí ẩn tại trường Hogwarts. Tác phẩm nhấn mạnh giá trị của tình bạn, lòng trung thực và sự lựa chọn giữa đúng và sai.',
185000,170000,55,2,9,'2025-12-16','2025-12-20',4.9),
('The Old Man and the Sea','old-man-sea',
'Phiên bản tiếng Anh của tác phẩm kinh điển "Ông già và biển cả". Cuốn sách mang phong cách giản dị, súc tích, thể hiện triết lý sống sâu sắc về sự bền bỉ, niềm tin và tinh thần không khuất phục.',
110000,98000,38,2,10,'2025-12-18','2025-12-22',4.6),
-- Sách thiếu nhi 
('James và quả đào khổng lồ','james-qua-dao',
'Câu chuyện phiêu lưu kỳ ảo kể về cậu bé James mồ côi sống cùng hai người dì độc ác. Cuộc đời cậu thay đổi hoàn toàn khi một quả đào khổng lồ xuất hiện, đưa James bước vào chuyến hành trình đầy phép màu cùng những người bạn côn trùng đặc biệt, vượt qua sợ hãi và tìm thấy mái ấm thật sự.',
90000,82000,50,3,11,'2025-12-01','2025-12-04',4.5),
('Enid Blyton: The Magic Faraway Tree','magic-faraway-tree',
'Tác phẩm thiếu nhi nổi tiếng của Enid Blyton kể về chiếc cây thần kỳ nơi mỗi tầng mây là một thế giới khác nhau. Những chuyến phiêu lưu trên cây mang đến trí tưởng tượng phong phú, khuyến khích trẻ em khám phá, sáng tạo và nuôi dưỡng tình bạn.',
95000,87000,45,3,12,'2025-12-03','2025-12-07',4.6),
('Heidi','heidi',
'Câu chuyện cảm động về cô bé Heidi sống giữa thiên nhiên núi Alps trong lành. Cuốn sách ca ngợi tình yêu gia đình, sự giản dị của cuộc sống và sức mạnh chữa lành của thiên nhiên, mang đến bài học nhân văn sâu sắc cho cả trẻ em lẫn người lớn.',
90000,82000,40,3,13,'2025-12-05','2025-12-08',4.5),
('Dr. Seuss’s ABC','dr-seuss-abc',
'Cuốn sách học chữ cái đầy màu sắc và sáng tạo, giúp trẻ em làm quen với bảng chữ cái thông qua vần điệu vui nhộn và hình ảnh sinh động. Tác phẩm kích thích khả năng ngôn ngữ, trí tưởng tượng và niềm yêu thích đọc sách từ sớm.',
85000,78000,55,3,14,'2025-12-06','2025-12-10',4.7),
('Gruffalo','gruffalo',
'Một câu chuyện thông minh và hài hước về chú chuột nhỏ dùng trí khôn để vượt qua những kẻ săn mồi nguy hiểm. Cuốn sách truyền tải thông điệp về sự tự tin, trí tuệ và lòng dũng cảm thông qua lối kể chuyện sáng tạo.',
90000,83000,50,3,15,'2025-12-08','2025-12-12',4.6),
('Charlie và nhà máy sô-cô-la','charlie-chocolate',
'Tác phẩm kinh điển kể về cậu bé Charlie nghèo khó nhưng lương thiện, may mắn bước vào nhà máy sô-cô-la kỳ diệu của Willy Wonka. Câu chuyện vừa hài hước vừa giàu tính giáo dục, đề cao sự trung thực và lòng nhân ái.',
100000,90000,50,3,11,'2025-12-10','2025-12-14',4.7),
('Matilda','matilda',
'Câu chuyện về cô bé thiên tài Matilda với trí thông minh vượt trội và tình yêu sách mãnh liệt. Tác phẩm khuyến khích trẻ em tin vào bản thân, yêu tri thức và dũng cảm đứng lên chống lại bất công.',
95000,85000,45,3,11,'2025-12-12','2025-12-16',4.6),
('Ngũ hiệp nổi tiếng','ngu-hiep-noi-tieng',
'Bộ truyện phiêu lưu hấp dẫn xoay quanh nhóm bạn nhỏ cùng nhau khám phá những bí ẩn ly kỳ. Những chuyến đi đầy thử thách giúp các em học được tinh thần đồng đội, lòng dũng cảm và khả năng suy luận.',
90000,80000,55,3,12,'2025-12-14','2025-12-18',4.5),
('Pippi tất dài','pippi-tat-dai',
'Câu chuyện vui nhộn về cô bé Pippi mạnh mẽ, độc lập và đầy cá tính. Nhân vật Pippi phá vỡ những khuôn mẫu thông thường, truyền cảm hứng cho trẻ em sống tự do, sáng tạo và dám khác biệt.',
95000,87000,40,3,13,'2025-12-16','2025-12-20',4.4),
('The Cat in the Hat','the-cat-in-the-hat',
'Câu chuyện kinh điển của Dr. Seuss với lối kể vần điệu độc đáo, xoay quanh chú mèo tinh nghịch mang đến một ngày đầy hỗn loạn nhưng thú vị. Cuốn sách giúp trẻ phát triển kỹ năng đọc và trí tưởng tượng.',
85000,78000,45,3,14,'2025-12-18','2025-12-22',4.5),

-- Kinh tế – Quản trị 
('Quản trị hiệu quả','quan-tri-hieu-qua',
'Cuốn sách cung cấp nền tảng toàn diện về quản trị doanh nghiệp hiện đại, tập trung vào cách tổ chức nguồn lực, tối ưu quy trình và nâng cao hiệu suất làm việc. Nội dung phù hợp cho nhà quản lý, sinh viên kinh tế và những người muốn xây dựng hệ thống vận hành bền vững.',
180000,165000,30,4,16,'2025-12-02','2025-12-06',4.4),
('Marketing căn bản','marketing-can-ban',
'Tác phẩm giới thiệu những khái niệm cốt lõi của marketing từ nghiên cứu thị trường, hành vi khách hàng đến xây dựng thương hiệu và chiến lược truyền thông. Sách giúp người đọc nắm vững nền tảng để áp dụng marketing hiệu quả trong môi trường kinh doanh thực tế.',
190000,175000,35,4,17,'2025-12-04','2025-12-08',4.5),
('Chiến lược cạnh tranh','chien-luoc-canh-tranh',
'Cuốn sách kinh điển về chiến lược kinh doanh, phân tích cách doanh nghiệp tạo lợi thế cạnh tranh bền vững thông qua chi phí, khác biệt hóa và tập trung thị trường. Nội dung giàu tính học thuật nhưng gắn liền với các ví dụ thực tiễn.',
200000,185000,25,4,18,'2025-12-06','2025-12-10',4.6),
('Từ tốt đến vĩ đại','tu-tot-den-vi-dai',
'Tác phẩm nghiên cứu sâu về những doanh nghiệp có bước chuyển mình ngoạn mục từ tốt sang vĩ đại. Cuốn sách chỉ ra các yếu tố cốt lõi như lãnh đạo cấp độ cao, kỷ luật tổ chức và tư duy chiến lược dài hạn.',
180000,165000,40,4,19,'2025-12-08','2025-12-12',4.7),
('7 thói quen hiệu quả','7-thoi-quen',
'Cuốn sách nổi tiếng về phát triển bản thân và lãnh đạo, trình bày bảy thói quen giúp cá nhân và tổ chức đạt hiệu quả lâu dài. Nội dung nhấn mạnh tư duy chủ động, quản lý thời gian và xây dựng mối quan hệ bền vững.',
170000,155000,45,4,20,'2025-12-10','2025-12-14',4.8),
('Lean In','lean-in',
'Tác phẩm truyền cảm hứng về vai trò lãnh đạo và sự tự tin trong công việc, đặc biệt dành cho phụ nữ trong môi trường doanh nghiệp. Cuốn sách khuyến khích người đọc mạnh dạn nắm bắt cơ hội, phát triển năng lực và cân bằng cuộc sống.',
180000,165000,40,4,16,'2025-12-12','2025-12-16',4.5),
('Principles','principles',
'Cuốn sách chia sẻ những nguyên tắc quản trị và ra quyết định được đúc kết từ kinh nghiệm thực tiễn trong kinh doanh và đầu tư. Nội dung giúp người đọc xây dựng tư duy hệ thống, minh bạch và hiệu quả trong quản lý.',
200000,185000,35,4,17,'2025-12-14','2025-12-18',4.6),
('Good to Great','good-to-great',
'Phiên bản tiếng Anh của tác phẩm kinh điển về quản trị doanh nghiệp, tập trung phân tích các yếu tố tạo nên sự vĩ đại bền vững. Cuốn sách là tài liệu tham khảo giá trị cho nhà lãnh đạo và quản lý cấp cao.',
180000,165000,30,4,19,'2025-12-16','2025-12-20',4.7),
('Competitive Strategy','competitive-strategy',
'Tác phẩm chuyên sâu về chiến lược kinh doanh, cung cấp các mô hình phân tích ngành và đối thủ cạnh tranh. Nội dung giúp doanh nghiệp hiểu rõ vị thế của mình và xây dựng chiến lược phù hợp trong môi trường cạnh tranh khốc liệt.',
190000,175000,28,4,18,'2025-12-18','2025-12-22',4.6),
('The 5 Levels of Leadership','5-levels-leadership',
'Cuốn sách trình bày năm cấp độ lãnh đạo từ cơ bản đến xuất sắc, giúp người đọc hiểu rõ con đường phát triển năng lực lãnh đạo. Nội dung phù hợp cho cả nhà quản lý mới và những người muốn nâng cao tầm ảnh hưởng.',
170000,155000,25,4,20,'2025-12-20','2025-12-24',4.7),
('Lược sử thời gian','luoc-su-thoi-gian',
'Tác phẩm nổi tiếng về vũ trụ học, giải thích những khái niệm phức tạp như nguồn gốc vũ trụ, hố đen và bản chất của thời gian bằng ngôn ngữ dễ tiếp cận. Cuốn sách giúp người đọc phổ thông hiểu sâu hơn về khoa học hiện đại và những câu hỏi lớn của nhân loại.',
170000,155000,40,5,21,'2025-12-01','2025-12-05',4.7),

('AI căn bản','ai-can-ban',
'Cuốn sách nhập môn về trí tuệ nhân tạo, trình bày các khái niệm nền tảng, lịch sử phát triển và những ứng dụng phổ biến của AI trong đời sống. Nội dung phù hợp cho người mới bắt đầu, sinh viên công nghệ và những ai muốn hiểu tổng quan về lĩnh vực này.',
250000,230000,30,5,23,'2025-12-03','2025-12-07',4.6),

('Machine Learning','machine-learning',
'Tác phẩm cung cấp kiến thức cơ bản và nâng cao về học máy, từ các thuật toán học có giám sát, không giám sát đến đánh giá mô hình. Cuốn sách giúp người đọc xây dựng nền tảng vững chắc để ứng dụng machine learning trong các bài toán thực tế.',
260000,240000,25,5,23,'2025-12-05','2025-12-09',4.6),

('The Web Weaving','web-weaving',
'Cuốn sách kể lại quá trình hình thành và phát triển của Internet, đặc biệt là sự ra đời của World Wide Web. Nội dung mang tính lịch sử và công nghệ, giúp người đọc hiểu rõ cách Internet thay đổi cách con người kết nối và chia sẻ thông tin.',
200000,185000,20,5,24,'2025-12-07','2025-12-11',4.5),

('Ngôn ngữ C','ngon-ngu-c',
'Tác phẩm giới thiệu ngôn ngữ lập trình C từ những khái niệm cơ bản đến kỹ thuật lập trình hiệu quả. Cuốn sách giúp người học nắm vững tư duy lập trình nền tảng, phù hợp cho sinh viên CNTT và người mới tiếp cận lập trình hệ thống.',
180000,165000,35,5,25,'2025-12-09','2025-12-13',4.4),

('Python Crash Course','python-crash-course',
'Cuốn sách hướng dẫn lập trình Python theo cách thực hành, kết hợp lý thuyết ngắn gọn với các dự án nhỏ. Nội dung giúp người đọc nhanh chóng làm quen với Python và áp dụng vào phát triển ứng dụng, phân tích dữ liệu hoặc tự động hóa.',
250000,230000,40,5,25,'2025-12-11','2025-12-15',4.8),

('Deep Learning','deep-learning',
'Tác phẩm chuyên sâu về học sâu, trình bày các mô hình mạng nơ-ron, mạng tích chập và mạng hồi quy. Cuốn sách phù hợp cho người đã có nền tảng machine learning và muốn nghiên cứu sâu hơn về trí tuệ nhân tạo hiện đại.',
300000,280000,35,5,23,'2025-12-13','2025-12-17',4.7),

('Artificial Intelligence: A Modern Approach','ai-modern',
'Cuốn sách kinh điển về trí tuệ nhân tạo, cung cấp cái nhìn toàn diện từ lý thuyết đến ứng dụng thực tiễn. Nội dung được sử dụng rộng rãi trong giảng dạy đại học và là tài liệu tham khảo quan trọng cho người nghiên cứu AI.',
280000,260000,30,5,24,'2025-12-15','2025-12-19',4.6),

('The Pragmatic Programmer','pragmatic-programmer',
'Tác phẩm nổi tiếng về lập trình thực hành, chia sẻ tư duy và kinh nghiệm giúp lập trình viên viết mã hiệu quả, dễ bảo trì. Cuốn sách tập trung vào kỹ năng nghề nghiệp và tư duy giải quyết vấn đề trong phát triển phần mềm.',
270000,250000,25,5,23,'2025-12-17','2025-12-21',4.7),

('Computer Networks','computer-networks',
'Cuốn sách cung cấp kiến thức nền tảng về mạng máy tính, từ mô hình OSI, TCP/IP đến các giao thức truyền thông. Nội dung phù hợp cho sinh viên CNTT và những người muốn hiểu cách các hệ thống máy tính kết nối với nhau.',
240000,220000,30,5,24,'2025-12-19','2025-12-23',4.5),

-- Tâm lý – Kỹ năng sống
('Đắc nhân tâm','dac-nhan-tam',
'Cuốn sách kinh điển về nghệ thuật giao tiếp và ứng xử, giúp người đọc hiểu tâm lý con người, xây dựng các mối quan hệ tích cực và tạo ảnh hưởng lâu dài. Nội dung tập trung vào cách lắng nghe, thấu hiểu và tôn trọng người khác trong cả công việc lẫn cuộc sống.',
150000,135000,60,6,26,'2025-12-02','2025-12-06',4.8),

('Đánh thức con người phi thường','danh-thuc-phi-thuong',
'Tác phẩm truyền cảm hứng mạnh mẽ, giúp người đọc khám phá tiềm năng bên trong và thay đổi tư duy để đạt được thành công. Cuốn sách kết hợp tâm lý học, động lực và các ví dụ thực tế nhằm khuyến khích hành động tích cực.',
170000,155000,45,6,27,'2025-12-04','2025-12-08',4.6),

('Trí tuệ cảm xúc','tri-tue-cam-xuc',
'Cuốn sách phân tích vai trò của trí tuệ cảm xúc trong công việc và đời sống cá nhân. Nội dung giúp người đọc hiểu, kiểm soát cảm xúc, nâng cao khả năng đồng cảm và xây dựng các mối quan hệ bền vững.',
160000,145000,40,6,28,'2025-12-06','2025-12-10',4.5),

('12 quy luật cuộc đời','12-quy-luat',
'Tác phẩm bàn về các nguyên tắc tâm lý và triết lý sống giúp con người định hướng cuộc đời một cách có trách nhiệm. Cuốn sách kết hợp giữa khoa học, triết học và kinh nghiệm thực tế để giúp người đọc trưởng thành hơn trong suy nghĩ và hành động.',
180000,165000,35,6,29,'2025-12-08','2025-12-12',4.6),

('Tư duy phát triển','tu-duy-phat-trien',
'Cuốn sách giải thích sự khác biệt giữa tư duy cố định và tư duy phát triển, từ đó giúp người đọc thay đổi cách nhìn nhận về học tập, công việc và thất bại. Nội dung khuyến khích việc học hỏi liên tục và không ngừng cải thiện bản thân.',
160000,145000,45,6,30,'2025-12-10','2025-12-14',4.7),

('How to Win Friends & Influence People','win-friends',
'Phiên bản tiếng Anh của tác phẩm kinh điển về giao tiếp và tạo ảnh hưởng. Cuốn sách cung cấp các nguyên tắc đơn giản nhưng hiệu quả để xây dựng mối quan hệ, thuyết phục người khác và trở thành người được tin tưởng.',
150000,135000,50,6,26,'2025-12-12','2025-12-16',4.8),

('Emotional Intelligence 2.0','eq-2',
'Cuốn sách tập trung vào việc phát triển trí tuệ cảm xúc thông qua các kỹ năng cụ thể như tự nhận thức, tự quản lý và quản lý mối quan hệ. Nội dung mang tính ứng dụng cao, phù hợp cho cả môi trường làm việc và cuộc sống cá nhân.',
150000,140000,40,6,28,'2025-12-14','2025-12-18',4.6),

('Mindset: The New Psychology','mindset-new',
'Tác phẩm phân tích sâu về tư duy phát triển và ảnh hưởng của nó đến thành công cá nhân. Cuốn sách giúp người đọc hiểu cách thay đổi suy nghĩ để cải thiện hiệu suất học tập, sự nghiệp và các mối quan hệ.',
160000,145000,35,6,30,'2025-12-16','2025-12-20',4.7),

('The Power of Habit','power-of-habit',
'Cuốn sách khám phá cách hình thành và thay đổi thói quen trong cuộc sống cá nhân cũng như tổ chức. Nội dung giúp người đọc hiểu cơ chế của thói quen và áp dụng để xây dựng những thói quen tích cực, bền vững.',
150000,140000,50,6,46,'2025-12-18','2025-12-22',4.8),

--Tiểu thuyết 
('Mật mã Da Vinci','mat-ma-da-vinci',
'Tiểu thuyết trinh thám nổi tiếng xoay quanh những bí ẩn lịch sử, tôn giáo và nghệ thuật. Câu chuyện theo chân giáo sư Robert Langdon trong hành trình giải mã các biểu tượng cổ, mang đến nhịp truyện nhanh, hồi hộp và nhiều cú twist bất ngờ.',
160000,145000,50,7,31,'2025-12-01','2025-12-05',4.6),
('Án mạng trên chuyến tàu','an-mang-tau-toc-hanh',
'Tác phẩm trinh thám kinh điển của Agatha Christie với bối cảnh một vụ án xảy ra trên chuyến tàu sang trọng. Cuốn sách hấp dẫn bởi cách xây dựng nhân vật tinh tế và màn phá án đầy logic của thám tử Hercule Poirot.',
150000,135000,40,7,32,'2025-12-03','2025-12-07',4.7),
('Sherlock Holmes','sherlock-holmes',
'Tuyển tập những vụ án nổi tiếng của thám tử Sherlock Holmes – biểu tượng của thể loại trinh thám cổ điển. Câu chuyện gây ấn tượng bởi khả năng suy luận sắc bén, bầu không khí bí ẩn và phong cách kể chuyện đặc trưng.',
170000,155000,45,7,33,'2025-12-05','2025-12-09',4.8),

('Đấu trường sinh tử','dau-truong-sinh-tu',
'Tiểu thuyết giả tưởng – hành động lấy bối cảnh xã hội tương lai đầy khắc nghiệt. Câu chuyện theo chân nhân vật chính trong cuộc chiến sinh tồn, phản ánh sự đấu tranh, lòng dũng cảm và khát vọng tự do.',
160000,145000,35,7,34,'2025-12-07','2025-12-11',4.6),

('Trò chơi vương quyền','tro-choi-vuong-quyen',
'Tác phẩm fantasy hoành tráng với thế giới rộng lớn, nhiều tuyến nhân vật và những âm mưu chính trị phức tạp. Cuốn sách cuốn hút bởi các trận chiến quyền lực, tình tiết bất ngờ và chiều sâu tâm lý nhân vật.',
220000,199000,30,7,35,'2025-12-09','2025-12-13',4.9),

('Angels & Demons','angels-demons',
'Tiểu thuyết trinh thám – khoa học tiếp nối Mật mã Da Vinci, xoay quanh cuộc đối đầu giữa khoa học hiện đại và tôn giáo cổ xưa. Câu chuyện diễn ra với nhịp độ nhanh, nhiều pha hành động và bí ẩn ly kỳ.',
160000,145000,40,7,31,'2025-12-11','2025-12-15',4.6),

('Murder on the Orient Express','orient-express',
'Phiên bản tiếng Anh của Án mạng trên chuyến tàu tốc hành, kể về một vụ giết người bí ẩn giữa chuyến tàu bị kẹt trong tuyết. Cuốn sách nổi bật với cái kết bất ngờ và cách phá án độc đáo.',
150000,135000,35,7,32,'2025-12-13','2025-12-17',4.7),

('The Adventures of Sherlock Holmes','sherlock-adventures',
'Tuyển tập các cuộc phiêu lưu nổi tiếng của Sherlock Holmes bằng tiếng Anh. Cuốn sách mang đậm phong cách trinh thám cổ điển, tập trung vào suy luận logic và những vụ án đầy thách thức.',
170000,155000,30,7,33,'2025-12-15','2025-12-19',4.8),

('Catching Fire','catching-fire',
'Phần tiếp theo của Đấu trường sinh tử, tiếp tục hành trình sinh tồn và đấu tranh của nhân vật chính. Câu chuyện được đẩy lên cao trào với những âm mưu chính trị, phản kháng và những lựa chọn đầy khó khăn.',
160000,145000,45,7,34,'2025-12-17','2025-12-21',4.7),

('A Game of Thrones','game-of-thrones',
'Phiên bản tiếng Anh của Trò chơi vương quyền, mở đầu cho loạt tiểu thuyết fantasy nổi tiếng. Tác phẩm xây dựng một thế giới giả tưởng rộng lớn với những cuộc chiến quyền lực, phản bội và số phận đan xen.',
220000,199000,50,7,35,'2025-12-19','2025-12-23',4.9),
-- Giáo dục – Học tập
('Trường học sáng tạo','truong-hoc-sang-tao',
'Cuốn sách trình bày những tư duy giáo dục hiện đại, khuyến khích sự sáng tạo và phát triển cá nhân của học sinh. Tác phẩm phân tích những hạn chế của mô hình giáo dục truyền thống và đề xuất cách xây dựng môi trường học tập linh hoạt, nhân văn.',
170000,155000,30,8,36,'2025-12-02','2025-12-05',4.5),

('Học mọi lúc mọi nơi','hoc-moi-luc',
'Tác phẩm tập trung vào mô hình học tập linh hoạt trong thời đại số, nơi người học có thể tiếp cận tri thức mọi lúc, mọi nơi. Cuốn sách phân tích vai trò của công nghệ trong giáo dục và xu hướng e-learning hiện đại.',
160000,145000,28,8,37,'2025-12-03','2025-12-06',4.4),

('Đa trí tuệ','da-tri-tue',
'Cuốn sách giới thiệu thuyết đa trí tuệ, nhấn mạnh rằng mỗi cá nhân có những thế mạnh khác nhau. Tác phẩm giúp giáo viên và phụ huynh hiểu rõ hơn về tiềm năng của trẻ, từ đó áp dụng phương pháp giáo dục phù hợp.',
180000,165000,25,8,38,'2025-12-04','2025-12-07',4.6),

('Giáo dục mở','giao-duc-mo',
'Tác phẩm bàn về triết lý giáo dục mở, đề cao sự tự do học tập và khả năng tiếp cận tri thức cho mọi người. Cuốn sách phân tích vai trò của công nghệ, cộng đồng và sự đổi mới trong giáo dục hiện đại.',
170000,155000,30,8,39,'2025-12-05','2025-12-08',4.5),

('Dân chủ và giáo dục','dan-chu-giao-duc',
'Tác phẩm kinh điển về triết lý giáo dục, nhấn mạnh mối quan hệ giữa giáo dục và xã hội dân chủ. Cuốn sách giúp người đọc hiểu rõ vai trò của giáo dục trong việc hình thành công dân có tư duy độc lập và trách nhiệm.',
160000,145000,20,8,40,'2025-12-06','2025-12-09',4.4),

('Creative Schools','creative-schools',
'Phiên bản tiếng Anh của Trường học sáng tạo, tập trung vào việc đổi mới giáo dục thông qua việc nuôi dưỡng sự sáng tạo. Tác phẩm cung cấp nhiều ví dụ thực tế và giải pháp nhằm cải thiện hệ thống giáo dục hiện nay.',
170000,155000,25,8,36,'2025-12-07','2025-12-10',4.5),

('Khan Academy Basics','khan-basics',
'Cuốn sách giới thiệu nền tảng học trực tuyến Khan Academy và triết lý giáo dục mở. Nội dung tập trung vào việc học tập tự do, cá nhân hóa và khả năng tiếp cận tri thức cho mọi đối tượng.',
160000,145000,28,8,37,'2025-12-08','2025-12-11',4.4),

('Multiple Intelligences','multiple-intelligences',
'Phiên bản tiếng Anh của Đa trí tuệ, trình bày chi tiết lý thuyết về nhiều loại hình trí thông minh. Cuốn sách là tài liệu tham khảo quan trọng cho giáo viên, nhà nghiên cứu và những ai quan tâm đến giáo dục cá nhân hóa.',
180000,165000,20,8,38,'2025-12-09','2025-12-12',4.6),

('The Hole in the Wall','hole-in-wall',
'Tác phẩm nghiên cứu nổi tiếng về giáo dục mở và học tập tự khám phá. Cuốn sách kể lại những thí nghiệm giáo dục độc đáo, cho thấy trẻ em có thể tự học hiệu quả khi được tạo điều kiện phù hợp.',
170000,155000,25,8,39,'2025-12-10','2025-12-13',4.5),

('Democracy and Education','democracy-education',
'Phiên bản tiếng Anh của Dân chủ và giáo dục, phân tích sâu mối liên hệ giữa giáo dục và xã hội. Tác phẩm được xem là nền tảng lý luận quan trọng trong lĩnh vực triết lý giáo dục hiện đại.',
160000,145000,22,8,40,'2025-12-11','2025-12-14',4.4),

-- Sách tham khảo
('Sách Toán lớp 10','toan-lop-10',
'Cuốn sách tổng hợp đầy đủ kiến thức Toán lớp 10 theo chương trình phổ thông mới. Nội dung được trình bày rõ ràng, có ví dụ minh họa chi tiết và hệ thống bài tập đa dạng giúp học sinh củng cố nền tảng và rèn luyện tư duy logic.',
95000,88000,40,9,41,'2025-12-02','2025-12-05',4.6),

('Sách Lý lớp 10','ly-lop-10',
'Tài liệu tham khảo môn Vật lý lớp 10, tập trung vào việc giải thích bản chất các hiện tượng vật lý. Cuốn sách cung cấp nhiều bài tập từ cơ bản đến nâng cao, hỗ trợ học sinh ôn tập và chuẩn bị tốt cho các kỳ kiểm tra.',
95000,88000,35,9,42,'2025-12-03','2025-12-06',4.5),

('Sách Hóa lớp 10','hoa-lop-10',
'Cuốn sách giúp học sinh hệ thống lại kiến thức Hóa học lớp 10 một cách khoa học. Nội dung bao gồm lý thuyết trọng tâm, ví dụ minh họa dễ hiểu và bài tập thực hành giúp nâng cao khả năng vận dụng.',
95000,88000,30,9,43,'2025-12-04','2025-12-07',4.6),

('Sách Sinh lớp 10','sinh-lop-10',
'Tài liệu ôn tập môn Sinh học lớp 10, trình bày rõ ràng các khái niệm sinh học cơ bản. Cuốn sách giúp học sinh nắm vững kiến thức nền tảng, phát triển tư duy khoa học và khả năng phân tích.',
95000,88000,28,9,44,'2025-12-05','2025-12-08',4.5),

('Sách Văn lớp 10','van-lop-10',
'Cuốn sách tham khảo môn Ngữ văn lớp 10, cung cấp hệ thống tác phẩm trọng tâm và hướng dẫn phân tích chi tiết. Nội dung hỗ trợ học sinh rèn luyện kỹ năng đọc hiểu, cảm thụ văn học và viết bài nghị luận.',
95000,88000,25,9,45,'2025-12-06','2025-12-09',4.6),

('Sách Toán lớp 11','toan-lop-11',
'Tài liệu tổng hợp kiến thức Toán lớp 11 với các chuyên đề quan trọng. Cuốn sách giúp học sinh nâng cao khả năng tư duy toán học thông qua hệ thống bài tập đa dạng và lời giải chi tiết.',
98000,90000,40,9,41,'2025-12-07','2025-12-10',4.7),

('Sách Lý lớp 11','ly-lop-11',
'Cuốn sách ôn tập Vật lý lớp 11, tập trung vào các nội dung trọng tâm và chuyên đề thường gặp trong kiểm tra. Nội dung được trình bày logic, giúp học sinh hiểu sâu và vận dụng hiệu quả.',
98000,90000,35,9,42,'2025-12-08','2025-12-11',4.6),

('Sách Hóa lớp 11','hoa-lop-11',
'Tài liệu tham khảo Hóa học lớp 11, cung cấp kiến thức từ cơ bản đến nâng cao. Cuốn sách hỗ trợ học sinh rèn luyện kỹ năng giải bài tập và chuẩn bị tốt cho các kỳ thi quan trọng.',
98000,90000,30,9,43,'2025-12-09','2025-12-12',4.7),

('Sách Sinh lớp 11','sinh-lop-11',
'Cuốn sách hệ thống hóa kiến thức Sinh học lớp 11, giúp học sinh hiểu rõ các quá trình sinh học quan trọng. Nội dung phù hợp cho việc ôn tập và nâng cao kết quả học tập.',
98000,90000,28,9,44,'2025-12-10','2025-12-13',4.6),

('Sách Văn lớp 11','van-lop-11',
'Tài liệu tham khảo môn Ngữ văn lớp 11, tập trung vào các tác phẩm trọng tâm và kỹ năng làm văn. Cuốn sách giúp học sinh nâng cao khả năng phân tích, cảm thụ và trình bày ý tưởng mạch lạc.',
98000,90000,25,9,45,'2025-12-11','2025-12-14',4.7),

-- Sách kỹ năng sống
('The 7 Habits of Highly Effective People','7-habits',
'Cuốn sách kinh điển về phát triển bản thân và kỹ năng sống, trình bày 7 thói quen cốt lõi giúp con người làm việc hiệu quả hơn trong cuộc sống cá nhân và sự nghiệp. Nội dung nhấn mạnh tư duy chủ động, quản lý thời gian và xây dựng các mối quan hệ bền vững.',
170000,155000,35,10,46,'2025-12-02','2025-12-05',4.7),

('Deep Work','deep-work',
'Cuốn sách tập trung vào tầm quan trọng của khả năng làm việc sâu trong thời đại nhiều xao nhãng. Tác phẩm hướng dẫn cách rèn luyện sự tập trung cao độ, nâng cao hiệu suất làm việc và tạo ra giá trị thực sự trong học tập và sự nghiệp.',
160000,145000,30,10,47,'2025-12-03','2025-12-06',4.6),

('Atomic Habits','atomic-habits',
'Cuốn sách nổi tiếng về việc xây dựng thói quen tích cực thông qua những thay đổi nhỏ mỗi ngày. Nội dung giúp người đọc hiểu cách hình thành, duy trì và loại bỏ thói quen xấu để đạt được sự tiến bộ bền vững trong cuộc sống.',
150000,140000,40,10,48,'2025-12-04','2025-12-07',4.8),

('The Subtle Art of Not Giving a F*ck','subtle-art',
'Tác phẩm mang góc nhìn thực tế và thẳng thắn về cách sống tích cực bằng việc tập trung vào những điều thực sự quan trọng. Cuốn sách giúp người đọc học cách chấp nhận giới hạn, đối diện khó khăn và xây dựng tư duy lành mạnh.',
160000,145000,38,10,49,'2025-12-05','2025-12-08',4.7),

('Essentialism','essentialism',
'Cuốn sách hướng dẫn lối sống và làm việc tối giản, tập trung vào những điều cốt lõi mang lại giá trị cao nhất. Nội dung giúp người đọc loại bỏ sự dư thừa, quản lý thời gian hiệu quả và nâng cao chất lượng cuộc sống.',
150000,140000,35,10,50,'2025-12-06','2025-12-09',4.6),

('Mindset: Tư duy phát triển','mindset',
'Tác phẩm nổi tiếng về tư duy phát triển, giải thích sự khác biệt giữa tư duy cố định và tư duy mở. Cuốn sách giúp người đọc thay đổi cách nhìn nhận thất bại, học hỏi từ thử thách và phát triển bản thân bền vững.',
160000,145000,30,10,50,'2025-12-07','2025-12-10',4.8),

('Grit','grit',
'Cuốn sách nhấn mạnh vai trò của sự kiên trì và đam mê trong việc đạt được thành công dài hạn. Nội dung dựa trên nghiên cứu khoa học và câu chuyện thực tế, truyền cảm hứng cho người đọc không bỏ cuộc trước khó khăn.',
160000,145000,32,10,47,'2025-12-08','2025-12-11',4.6),

('Emotional Intelligence 2.0','emotional-intelligence',
'Tác phẩm giúp người đọc hiểu và rèn luyện trí tuệ cảm xúc, bao gồm khả năng tự nhận thức, kiểm soát cảm xúc và xây dựng mối quan hệ. Cuốn sách phù hợp cho cả phát triển cá nhân và môi trường làm việc.',
170000,155000,28,10,28,'2025-12-09','2025-12-12',4.8),

('Awaken the Giant Within','awaken-giant',
'Cuốn sách truyền cảm hứng mạnh mẽ về việc làm chủ bản thân và khai phá tiềm năng cá nhân. Nội dung hướng dẫn cách thay đổi tư duy, thói quen và cảm xúc để tạo ra những bước ngoặt tích cực trong cuộc sống.',
180000,165000,25,10,27,'2025-12-10','2025-12-13',4.7),

-- Lịch sử – Địa lý 
('Guns, Germs, and Steel','guns-germs-steel',
'Tác phẩm phân tích lịch sử phát triển của các nền văn minh nhân loại dưới góc nhìn môi trường, địa lý và sinh học. Cuốn sách lý giải vì sao một số xã hội phát triển vượt trội hơn những xã hội khác, không dựa trên chủng tộc mà dựa vào điều kiện tự nhiên, tài nguyên và sự lan truyền của công nghệ.',
200000,185000,30,11,51,'2025-12-02','2025-12-05',4.8),

('The Silk Roads','silk-roads',
'Cuốn sách tái hiện lịch sử thế giới thông qua Con đường Tơ lụa – tuyến giao thương quan trọng kết nối Đông và Tây. Tác phẩm mang đến một góc nhìn mới mẻ về sự hình thành, giao thoa văn hóa, kinh tế và chính trị của các nền văn minh lớn.',
180000,165000,28,11,52,'2025-12-03','2025-12-06',4.7),

('The History of Vietnam','history-vietnam',
'Sách trình bày tiến trình lịch sử Việt Nam từ thời kỳ dựng nước đến hiện đại. Nội dung bao quát các giai đoạn quan trọng, các cuộc kháng chiến, biến động chính trị và văn hóa, giúp người đọc hiểu sâu sắc hơn về bản sắc dân tộc Việt.',
150000,140000,25,11,53,'2025-12-04','2025-12-07',4.6),

('A Short History of Nearly Everything','short-history',
'Tác phẩm khoa học – lịch sử nổi tiếng giúp người đọc tiếp cận những kiến thức phức tạp về vũ trụ, Trái Đất và sự sống một cách dễ hiểu. Sách kết hợp hài hòa giữa khoa học, lịch sử khám phá và những câu chuyện hấp dẫn.',
190000,175000,20,11,54,'2025-12-05','2025-12-08',4.5),

('The Geography of Thought','geography-thought',
'Cuốn sách nghiên cứu sự khác biệt trong tư duy và nhận thức giữa các nền văn hóa Đông – Tây. Thông qua địa lý, lịch sử và xã hội, tác giả lý giải cách môi trường sống ảnh hưởng đến cách con người suy nghĩ và hành xử.',
170000,155000,22,11,55,'2025-12-06','2025-12-09',4.6),

('1491: Before Columbus','1491-before-columbus',
'Tác phẩm khám phá lịch sử châu Mỹ trước khi Christopher Columbus đặt chân tới. Cuốn sách làm sáng tỏ các nền văn minh bản địa phát triển rực rỡ, phá vỡ nhiều quan niệm sai lầm về xã hội tiền Colombo.',
180000,165000,20,11,52,'2025-12-07','2025-12-10',4.6),

('Collapse','collapse',
'Cuốn sách phân tích nguyên nhân khiến các nền văn minh từng hưng thịnh rơi vào suy tàn. Tác giả xem xét các yếu tố như môi trường, biến đổi khí hậu, chiến tranh và quản lý tài nguyên, từ đó rút ra bài học cho xã hội hiện đại.',
200000,185000,18,11,51,'2025-12-08','2025-12-11',4.7),

('Vietnam: A History','vietnam-history',
'Tác phẩm tổng hợp lịch sử Việt Nam qua nhiều thời kỳ với cách tiếp cận khách quan và học thuật. Sách cung cấp cái nhìn toàn diện về chính trị, văn hóa, xã hội và những biến chuyển quan trọng của đất nước.',
150000,140000,25,11,53,'2025-12-09','2025-12-12',4.6),

('The Rise and Fall of the Third Reich','third-reich',
'Cuốn sách kinh điển ghi lại quá trình hình thành, phát triển và sụp đổ của Đệ tam Đế chế Đức. Tác phẩm cung cấp tư liệu lịch sử chi tiết, giúp người đọc hiểu rõ bối cảnh chính trị và xã hội châu Âu thế kỷ XX.',
220000,200000,15,11,52,'2025-12-10','2025-12-13',4.8),

('Prisoners of Geography','prisoners-geography',
'Tác phẩm phân tích vai trò của địa lý trong việc định hình chính trị và chiến lược toàn cầu. Cuốn sách cho thấy cách núi non, sông ngòi, khí hậu và vị trí địa lý ảnh hưởng sâu sắc đến vận mệnh các quốc gia.',
170000,155000,22,11,55,'2025-12-11','2025-12-14',4.7),

-- Nghệ thuật – Hội họa 
('Leonardo da Vinci: Huyền thoại Phục Hưng','leonardo-da-vinci',
'Cuốn sách khắc họa chân dung toàn diện của Leonardo da Vinci – thiên tài vĩ đại thời Phục Hưng. Tác phẩm không chỉ phân tích các kiệt tác hội họa nổi tiếng mà còn khám phá tư duy khoa học, sáng tạo và ảnh hưởng sâu rộng của ông đối với nghệ thuật và nhân loại.',
300000,280000,20,12,56,'2025-12-02','2025-12-05',4.8),

('Picasso: Người tạo trào lưu hiện đại','picasso',
'Tác phẩm giới thiệu cuộc đời và sự nghiệp của Pablo Picasso, người đã thay đổi hoàn toàn diện mạo hội họa thế kỷ XX. Cuốn sách phân tích các giai đoạn sáng tác, phong cách nghệ thuật và tư duy cách mạng đã đưa ông trở thành biểu tượng của nghệ thuật hiện đại.',
280000,260000,18,12,57,'2025-12-03','2025-12-06',4.7),

('Van Gogh: Chân dung cuộc đời','van-gogh',
'Cuốn sách tái hiện cuộc đời đầy bi kịch nhưng cũng vô cùng rực rỡ của Vincent van Gogh. Thông qua các tác phẩm và thư từ, sách giúp người đọc hiểu rõ hơn về tâm hồn, cảm xúc và giá trị nghệ thuật bất hủ của một thiên tài hậu ấn tượng.',
270000,250000,22,12,58,'2025-12-04','2025-12-07',4.7),

('Claude Monet: Ánh sáng và màu sắc','claude-monet',
'Tác phẩm phân tích phong cách nghệ thuật của Claude Monet – người tiên phong của trường phái Ấn tượng. Cuốn sách làm nổi bật cách ông sử dụng ánh sáng, màu sắc và thiên nhiên để tạo nên những bức tranh đầy cảm xúc và sức sống.',
260000,240000,20,12,59,'2025-12-05','2025-12-08',4.6),

('Frida Kahlo: Cuộc sống và nghệ thuật','frida-kahlo',
'Cuốn sách kể về cuộc đời đầy đau đớn nhưng mãnh liệt của Frida Kahlo, nơi nghệ thuật trở thành tiếng nói cá nhân mạnh mẽ. Tác phẩm giúp người đọc hiểu rõ mối liên hệ giữa trải nghiệm cá nhân, văn hóa Mexico và phong cách hội họa độc đáo của bà.',
250000,230000,18,12,60,'2025-12-06','2025-12-09',4.8),

('Rembrandt: Bậc thầy ánh sáng','rembrandt',
'Tác phẩm khám phá nghệ thuật của Rembrandt – bậc thầy hội họa Hà Lan thế kỷ XVII. Cuốn sách tập trung phân tích kỹ thuật xử lý ánh sáng, bố cục và chiều sâu cảm xúc trong các bức chân dung và tranh tôn giáo nổi tiếng.',
280000,260000,15,12,61,'2025-12-07','2025-12-10',4.7),

('Michelangelo: Nghệ thuật và điêu khắc','michelangelo',
'Cuốn sách giới thiệu cuộc đời và sự nghiệp của Michelangelo – nghệ sĩ vĩ đại của thời Phục Hưng. Tác phẩm làm nổi bật những kiệt tác điêu khắc và hội họa, đồng thời phân tích tư duy nghệ thuật và sức ảnh hưởng lâu dài của ông.',
300000,280000,12,12,62,'2025-12-08','2025-12-11',4.8),

('Georgia O’Keeffe: Hoa và sa mạc','georgia-okeeffe',
'Tác phẩm phân tích phong cách nghệ thuật độc đáo của Georgia O’Keeffe, nổi bật với hình ảnh hoa, sa mạc và thiên nhiên Mỹ. Cuốn sách giúp người đọc hiểu rõ cách bà thể hiện cảm xúc và bản sắc cá nhân thông qua hội họa hiện đại.',
240000,220000,18,12,63,'2025-12-09','2025-12-12',4.6),

('Jackson Pollock: Nghệ thuật trừu tượng','jackson-pollock',
'Cuốn sách khám phá phong cách trừu tượng hành động của Jackson Pollock – người phá vỡ mọi quy chuẩn truyền thống. Tác phẩm phân tích kỹ thuật, triết lý sáng tác và ảnh hưởng của ông đối với nghệ thuật đương đại.',
250000,230000,16,12,64,'2025-12-10','2025-12-13',4.7),

('Andy Warhol: Pop Art','andy-warhol',
'Tác phẩm giới thiệu Andy Warhol – biểu tượng của nghệ thuật Pop Art. Cuốn sách phân tích cách ông biến văn hóa đại chúng thành nghệ thuật, phản ánh xã hội tiêu dùng và tạo nên ảnh hưởng sâu rộng trong nghệ thuật hiện đại.',
260000,240000,15,12,65,'2025-12-11','2025-12-14',4.7),

-- Sách ngoại ngữ 
('English Grammar in Use','english-grammar-in-use',
'Cuốn sách ngữ pháp tiếng Anh kinh điển dành cho người học ở mọi trình độ. Nội dung được trình bày rõ ràng, dễ hiểu với ví dụ thực tế và bài tập kèm theo, giúp người học nắm vững cấu trúc ngữ pháp và áp dụng hiệu quả trong giao tiếp hàng ngày.',
220000,200000,40,13,58,'2025-12-02','2025-12-05',4.8),

('Word Power Made Easy','word-power',
'Tác phẩm nổi tiếng giúp người học mở rộng vốn từ vựng một cách hệ thống và khoa học. Cuốn sách kết hợp giữa nguồn gốc từ, cách ghi nhớ và bài tập thực hành, giúp cải thiện kỹ năng sử dụng từ ngữ trong cả nói và viết.',
200000,185000,35,13,59,'2025-12-03','2025-12-06',4.7),

('English Vocabulary in Use','english-vocab-use',
'Cuốn sách cung cấp kho từ vựng phong phú được phân chia theo chủ đề cụ thể. Nội dung dễ tiếp cận, có ví dụ minh họa rõ ràng và bài luyện tập, giúp người học nâng cao vốn từ và khả năng sử dụng tiếng Anh một cách tự nhiên.',
210000,195000,38,13,60,'2025-12-04','2025-12-07',4.7),

('English Idioms in Use','english-idioms',
'Tác phẩm tập trung vào các thành ngữ tiếng Anh thông dụng trong giao tiếp và văn viết. Cuốn sách giúp người học hiểu đúng ngữ cảnh sử dụng idioms, từ đó nâng cao khả năng diễn đạt và tiếp cận tiếng Anh như người bản ngữ.',
200000,185000,35,13,61,'2025-12-05','2025-12-08',4.6),

('Cambridge English Grammar','cambridge-grammar',
'Cuốn sách ngữ pháp nâng cao do Cambridge biên soạn, phù hợp cho người học ở trình độ trung cấp và cao cấp. Nội dung đi sâu vào cấu trúc phức tạp, cách sử dụng chuẩn xác và các lỗi thường gặp trong tiếng Anh học thuật.',
220000,200000,40,13,62,'2025-12-06','2025-12-09',4.8),

('English Phrasal Verbs','english-phrasal',
'Tác phẩm chuyên sâu về động từ cụm – một phần quan trọng nhưng khó của tiếng Anh. Cuốn sách giải thích ý nghĩa, cách dùng và ngữ cảnh phổ biến, giúp người học tự tin hơn khi giao tiếp và đọc hiểu tài liệu tiếng Anh.',
210000,195000,30,13,63,'2025-12-07','2025-12-10',4.7),

('Practical English Usage','practical-english',
'Cuốn sách tham khảo toàn diện về cách sử dụng tiếng Anh trong thực tế. Nội dung giải đáp chi tiết các vấn đề ngữ pháp, từ vựng và cách diễn đạt thường gây nhầm lẫn, phù hợp cho cả người học và giáo viên tiếng Anh.',
230000,210000,25,13,64,'2025-12-08','2025-12-11',4.8),

('English for Academic Purposes','english-academic',
'Tác phẩm dành cho người học cần sử dụng tiếng Anh trong môi trường học thuật. Cuốn sách tập trung phát triển kỹ năng đọc, viết, trình bày và tư duy học thuật, hỗ trợ hiệu quả cho sinh viên và nghiên cứu sinh.',
240000,220000,28,13,65,'2025-12-09','2025-12-12',4.6),

('Teach Yourself English','teach-yourself',
'Cuốn sách tự học tiếng Anh dành cho người mới bắt đầu và người học độc lập. Nội dung được thiết kế theo lộ trình rõ ràng, kết hợp giữa lý thuyết và thực hành, giúp người học xây dựng nền tảng tiếng Anh vững chắc.',
200000,185000,32,13,66,'2025-12-10','2025-12-13',4.7),

('Oxford Word Skills','oxford-word-skills',
'Tác phẩm phát triển từ vựng tiếng Anh theo chuẩn Oxford, phù hợp với nhiều trình độ khác nhau. Cuốn sách cung cấp từ vựng theo chủ đề, ví dụ sinh động và bài luyện tập thực tế, giúp người học ghi nhớ và vận dụng hiệu quả.',
220000,200000,30,13,67,'2025-12-11','2025-12-14',4.7),

-- Sách y học 
('Why We Sleep','why-we-sleep',
'Cuốn sách khoa học nổi tiếng khám phá vai trò thiết yếu của giấc ngủ đối với sức khỏe thể chất và tinh thần. Tác phẩm giải thích cách giấc ngủ ảnh hưởng đến trí nhớ, cảm xúc, hệ miễn dịch và tuổi thọ, giúp người đọc hiểu rõ vì sao ngủ đủ và đúng cách là nền tảng của một cuộc sống khỏe mạnh.',
190000,175000,30,14,60,'2025-12-02','2025-12-05',4.6),

('How Not to Die','how-not-to-die',
'Tác phẩm tập trung vào mối liên hệ giữa dinh dưỡng và phòng ngừa bệnh tật. Cuốn sách trình bày các nghiên cứu khoa học về chế độ ăn uống lành mạnh, nhấn mạnh vai trò của thực phẩm trong việc hỗ trợ sức khỏe tim mạch và nâng cao chất lượng cuộc sống.',
220000,200000,28,14,61,'2025-12-03','2025-12-06',4.7),

('The Body Keeps the Score','body-keeps-score',
'Cuốn sách đi sâu vào mối liên hệ giữa tâm lý, sang chấn và sức khỏe cơ thể. Tác phẩm giúp người đọc hiểu cách trải nghiệm tinh thần có thể ảnh hưởng lâu dài đến não bộ và cơ thể, từ đó mở ra góc nhìn toàn diện hơn về chăm sóc sức khỏe tinh thần.',
210000,195000,28,14,62,'2025-12-04','2025-12-07',4.7),

('How to Eat','how-to-eat',
'Cuốn sách cung cấp kiến thức nền tảng về dinh dưỡng hàng ngày, giúp người đọc hiểu cách lựa chọn thực phẩm phù hợp với nhu cầu cơ thể. Nội dung được trình bày dễ tiếp cận, phù hợp cho những ai muốn xây dựng thói quen ăn uống khoa học.',
200000,185000,25,14,63,'2025-12-05','2025-12-08',4.6),

('Nutrition and Health','nutrition-health',
'Tác phẩm tổng hợp kiến thức về dinh dưỡng và sức khỏe dựa trên nghiên cứu khoa học. Cuốn sách phân tích vai trò của các nhóm chất dinh dưỡng và mối liên hệ giữa chế độ ăn uống với sức khỏe tổng thể.',
220000,200000,30,14,64,'2025-12-06','2025-12-09',4.7),

('Sleep Smarter','sleep-smarter',
'Cuốn sách hướng đến việc cải thiện chất lượng giấc ngủ thông qua các thói quen sinh hoạt khoa học. Tác phẩm giúp người đọc hiểu rõ hơn về nhịp sinh học và tầm quan trọng của giấc ngủ đối với hiệu suất làm việc và sức khỏe hàng ngày.',
190000,175000,35,14,65,'2025-12-07','2025-12-10',4.6),

('The Blue Zones','blue-zones',
'Tác phẩm nghiên cứu những cộng đồng sống thọ trên thế giới và các yếu tố lối sống góp phần tạo nên tuổi thọ cao. Cuốn sách mang đến góc nhìn thực tiễn về dinh dưỡng, vận động, tinh thần và mối quan hệ xã hội.',
210000,195000,20,14,66,'2025-12-08','2025-12-11',4.8),

('The Plant Paradox','plant-paradox',
'Cuốn sách thảo luận về mối quan hệ giữa chế độ ăn uống và sức khỏe tiêu hóa. Tác phẩm đưa ra góc nhìn mới về việc lựa chọn thực phẩm một cách thông minh để hỗ trợ sức khỏe lâu dài.',
200000,185000,22,14,67,'2025-12-09','2025-12-12',4.7),

('Eat to Live','eat-to-live',
'Tác phẩm tập trung vào vai trò của dinh dưỡng trong việc duy trì sức khỏe và phòng ngừa bệnh tật. Cuốn sách khuyến khích xây dựng lối sống ăn uống lành mạnh dựa trên nền tảng khoa học.',
220000,200000,25,14,68,'2025-12-10','2025-12-13',4.7),

('Mindful Eating','mindful-eating',
'Cuốn sách giới thiệu khái niệm ăn uống chánh niệm, giúp người đọc nhận thức rõ hơn về thói quen ăn uống và mối liên hệ giữa tâm trí và cơ thể. Tác phẩm hướng đến việc xây dựng mối quan hệ tích cực với thực phẩm.',
210000,195000,20,14,69,'2025-12-11','2025-12-14',4.6),

-- Truyện tranh 
('One Piece Tập 1','one-piece-1',
'Tập mở đầu của bộ manga nổi tiếng kể về hành trình phiêu lưu trên biển của Luffy và ước mơ trở thành Vua Hải Tặc. Câu chuyện thu hút người đọc bởi thế giới rộng lớn, nhân vật cá tính và tinh thần tự do, tình bạn đầy cảm hứng.',
45000,40000,120,15,62,'2025-12-02','2025-12-05',4.9),

('Naruto Tập 1','naruto-1',
'Tập đầu tiên giới thiệu Naruto – cậu bé ninja mang trong mình khát vọng được công nhận. Truyện kết hợp giữa hành động, tình bạn và sự trưởng thành, mở ra thế giới ninja đầy thử thách và cảm xúc.',
45000,40000,110,15,63,'2025-12-03','2025-12-06',4.8),

('Dragon Ball Tập 1','dragon-ball-1',
'Tập mở màn của Dragon Ball đưa người đọc bước vào hành trình phiêu lưu đầy màu sắc của Son Goku. Truyện mang phong cách vui nhộn, kết hợp giữa phiêu lưu và chiến đấu, phù hợp với nhiều thế hệ độc giả.',
45000,40000,100,15,64,'2025-12-04','2025-12-07',4.8),

('Attack on Titan Tập 1','attack-on-titan-1',
'Tập đầu tiên xây dựng một thế giới giả tưởng nơi con người phải sinh tồn trước những mối đe dọa khổng lồ. Truyện gây ấn tượng mạnh bởi cốt truyện kịch tính, không khí căng thẳng và những câu hỏi về tự do và số phận.',
50000,45000,90,15,65,'2025-12-05','2025-12-08',4.9),

('One Piece Tập 2','one-piece-2',
'Tập tiếp theo tiếp tục hành trình của Luffy trên con đường chinh phục biển cả. Câu chuyện mở rộng thế giới hải tặc, giới thiệu thêm nhân vật mới và làm nổi bật tinh thần đồng đội.',
45000,40000,110,15,62,'2025-12-06','2025-12-09',4.9),

('Naruto Tập 2','naruto-2',
'Tập 2 phát triển sâu hơn về quá trình rèn luyện và những thử thách đầu tiên của Naruto. Truyện nhấn mạnh sự nỗ lực, ý chí và tình bạn trong thế giới ninja.',
45000,40000,100,15,63,'2025-12-07','2025-12-10',4.8),

('Dragon Ball Tập 2','dragon-ball-2',
'Tập này tiếp tục những cuộc phiêu lưu thú vị của Goku và bạn bè. Truyện giữ phong cách hài hước đặc trưng, đồng thời mở rộng thế giới và các nhân vật.',
45000,40000,90,15,64,'2025-12-08','2025-12-11',4.8),

('Attack on Titan Tập 2','attack-on-titan-2',
'Tập 2 đẩy cao nhịp truyện với những tình tiết căng thẳng và bí ẩn hơn. Câu chuyện tiếp tục khai thác tâm lý nhân vật và bối cảnh thế giới đầy thử thách.',
50000,45000,80,15,65,'2025-12-09','2025-12-12',4.9),

('Bleach Tập 1','bleach-1',
'Tập đầu tiên giới thiệu thế giới linh hồn và nhân vật chính Ichigo. Truyện kết hợp yếu tố hành động, siêu nhiên và cảm xúc gia đình, tạo nên phong cách riêng biệt.',
45000,40000,75,15,66,'2025-12-10','2025-12-13',4.7),

('My Hero Academia Tập 1','my-hero-1',
'Tập mở đầu kể về một thế giới nơi siêu năng lực trở nên phổ biến và ước mơ trở thành anh hùng của cậu bé Midoriya. Truyện truyền tải thông điệp tích cực về nỗ lực và lòng dũng cảm.',
45000,40000,70,15,67,'2025-12-11','2025-12-14',4.8),

('Doraemon Tập 2','doraemon-2',
'Tập truyện mang đậm ký ức tuổi thơ với những câu chuyện hài hước, nhẹ nhàng xoay quanh Doraemon và Nobita. Nội dung gần gũi, giàu tính giáo dục và giải trí.',
40000,36000,140,15,68,'2025-12-12','2025-12-15',4.8),

('Dragon Quest: Dai Tập 1','dragon-quest-1',
'Tập đầu tiên mở ra thế giới phiêu lưu kỳ ảo dựa trên trò chơi nổi tiếng Dragon Quest. Truyện mang phong cách anh hùng, tình bạn và hành trình trưởng thành đầy cảm hứng.',
45000,40000,60,15,69,'2025-12-13','2025-12-16',4.7);

----------------------- thêm bìa cho sách --------------------------
INSERT INTO book_image (book_id, image) VALUES
(1, 'https://upload.wikimedia.org/wikipedia/vi/c/c9/Cho_t%C3%B4i_xin_m%E1%BB%99t_v%C3%A9_%C4%91i_tu%E1%BB%95i_th%C6%A1.jpg'),
(2, 'https://upload.wikimedia.org/wikipedia/vi/3/3d/T%C3%B4i_th%E1%BA%A5y_hoa_v%C3%A0ng_tr%C3%AAn_c%E1%BB%8F_xanh.jpg'),
(3, 'https://bavi.edu.vn/upload/21768/fck/files/150800018_3868030666550251_8375198552020103317_n.jpg'),
(4, 'https://book.sachgiai.com/uploads/book/truyen-ngan-chi-pheo/truyen-ngan-chi-pheo-nam-cao.jpg'),
(5, 'https://isach.info/images/story/cover/tuong_ve_huu__nguyen_huy_thiep.jpg'),
(6, 'https://upload.wikimedia.org/wikipedia/vi/1/11/Noi_buon_chien_tranh.jpg'),
(7, 'https://cdn1.fahasa.com/media/catalog/product/s/_/s_-b1.jpg'),
(8, 'https://product.hstatic.net/200000343865/product/tuoi-tho-du-doi_tap-1---tb-2023_37610d8b4cd0453aa96ab4f7873defee.png'),
(9, 'https://upload.wikimedia.org/wikipedia/vi/6/6a/B%E1%BA%BFn_kh%C3%B4ng_ch%E1%BB%93ng_%28phim%29.jpg'),
(10, 'https://static.oreka.vn/500-500_6a388038-78fd-45c8-a58e-20af300abb8e.webp'),
(11, 'https://thiquocgia.vn/wp-content/uploads/tom-tat-vo-chong-a-phu-3.jpg'),

(12, 'https://upload.wikimedia.org/wikipedia/vi/2/28/Norwegian-wood_poster.jpg'),
(13, 'https://tgu.edu.vn/upload/images/1_nha%20gia%20kim.jpg'),
(14, 'https://m.media-amazon.com/images/I/71wANojhEKL._AC_UF894,1000_QL80_.jpg'),
(15, 'https://www.nxbtre.com.vn/Images/Book/nxbtre_full_21542017_035423.jpg'),
(16, 'https://product.hstatic.net/200000845405/product/b_a_1_-_ng_gi_v_bi_n_c__d48977e1bcd442e09b8d437dfabad90f_master.png'),
(17, 'https://sachnhanam.s3.ap-southeast-1.amazonaws.com/wp-content/uploads/20231116115648/Bi-Mat-Cua-Naoko-Tobey-Nguyen-Tobey-Nguyen-scaled.jpg'),
(18, 'https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1483412266i/865.jpg'),
(19, 'https://upload.wikimedia.org/wikipedia/en/thumb/8/85/Tt0204824.jpeg/250px-Tt0204824.jpeg'),
(20, 'https://www.nxbtre.com.vn/Images/Book/nxbtre_full_21472017_034753.jpg'),
(21, 'https://m.media-amazon.com/images/I/71RXc0OoEwL._AC_UF894,1000_QL80_.jpg'),
(22, 'https://salt.tikicdn.com/cache/750x750/media/catalog/product/f/u/full_a197ed2434f3c2d9450d744b7a411bdc.jpg'),

(23, 'https://m.media-amazon.com/images/I/71cBeTUYFEL._AC_UF894,1000_QL80_.jpg'),
(24, 'https://nxbphunu.com.vn/wp-content/uploads/2023/10/heidi-bia-1.jpg'),
(25, 'https://salt.tikicdn.com/cache/w300/ts/product/ff/f3/5b/8cb66bc3c92ba793dcbde1cc6e3a9de1.jpg'),
(26, 'https://upload.wikimedia.org/wikipedia/en/3/34/Fairuse_Gruffalo.jpg'),
(27, 'https://upload.wikimedia.org/wikipedia/vi/f/fc/Charlie_v%C3%A0_Nh%C3%A0_M%C3%A1y_S%C3%B4c%C3%B4la_Kim_%C4%90%E1%BB%93ng_60.jpg'),
(28, 'https://m.media-amazon.com/images/I/81EVlFfo4tL._AC_UF894,1000_QL80_.jpg'),
(29, 'https://khosachcu.com/image/cache/data/Tre/vo-hiep-ngu-dai-gia-390x525.jpg'),
(30, 'https://salt.tikicdn.com/cache/w300/media/catalog/product/p/i/pippi_tat_dai-pp_4.jpg'),
(31, 'https://upload.wikimedia.org/wikipedia/en/thumb/1/10/The_Cat_in_the_Hat.png/250px-The_Cat_in_the_Hat.png'),
(32, 'https://pacebooks.pace.edu.vn/Uploads/PACE_BOOKS/2024/8/13/nhaquantrihieuquathumbnailwebp.webp'),
(33, 'https://cdn1.fahasa.com/media/flashmagazine/images/page_images/marketing_can_ban___marketing_101/2022_06_17_16_06_19_7-390x510.jpg'),

(34, 'https://cdn1.fahasa.com/media/catalog/product/1/1/1104060003915.jpg'),
(35, 'https://hbr.edu.vn/storage/news/2018/04/14/tom-tat-cuon-sach-kinh-dien-tu-tot-den-vi-dai-jim-collins-18.webp'),
(36, 'https://www.pace.edu.vn/uploads/news/2023/05/gioi-thieu-7-thoi-quen-hieu-qua.jpg'),
(37, 'https://www.elle.vn/wp-content/uploads/2022/06/05/481496/how-we-learn-review-sach-hay-ve-cach-hoc-scaled.jpg'),
(38, 'https://cdn.hstatic.net/200000692705/file/ipals-life-work-by-ray-dalio-1024x576_80dd55f10ab247239430d3f260b31a72_grande.png'),
(39, 'https://upload.wikimedia.org/wikipedia/en/thumb/0/03/Cover_Good_2_Gr8.jpg/250px-Cover_Good_2_Gr8.jpg'),
(40, 'https://product.hstatic.net/200000481913/product/b6a2c4f8-5b9e-4fae-9310-50673afd76a0_e278cc68457546f69cc748b984cea662.jpg'),
(41, 'https://salt.tikicdn.com/cache/w1200/media/catalog/product/4/1/41dgzsutbnl._sx322_bo1,204,203,200_.u2654.d20160912.t151303.153783.jpg'),
(42, 'https://www.nxbtre.com.vn/Images/Book/copy_27_nxbtre_full_21022016_100217.jpg'),
(43, 'https://www.netabooks.vn/Data/Sites/1/Product/43118/ai-tri-tue-nhan-tao-101-dieu-can-biet-ve-tuong-lai.jpg'),
(44, 'https://nguyenvanhieu.vn/wp-content/uploads/2023/09/2-14-1.jpg.webp'),

(45, 'https://m.media-amazon.com/images/I/51N6MWZFP7L._AC_UF1000,1000_QL80_.jpg'),
(46, 'https://salt.tikicdn.com/cache/w300/ts/product/ba/d4/99/1209b20bd2da72f70146c6216ddea452.jpg'),
(47, 'https://salt.tikicdn.com/cache/w1200/ts/product/44/3c/a3/bfbcd2602c85f2445fabe2399606540b.jpg'),
(48, 'https://newshop.vn/public/uploads/content/cu%E1%BB%99c%20c%C3%A1ch%20m%E1%BA%A1ng%20s%C3%A2u.png'),
(49, 'https://upload.wikimedia.org/wikipedia/en/e/e5/Artificial_Intelligence-_A_Modern_Approach.jpg'),
(50, 'https://pawelgrzybek.com/book-review-the-pragmatic-programmer-by-david-thomas-and-andrew-hunt/2021-07-04-1.jpg'),
(51, 'https://secure-ecsd.elsevier.com/covers/80/Tango2/largest/9780128182000.jpg'),
(52, 'https://cungdocsach.vn/wp-content/uploads/2020/10/%C4%90%E1%BA%AFc-nh%C3%A2n-t%C3%A2m-3.jpg'),
(53, 'https://sachnoivietnam.com/wp-content/uploads/2021/09/2.-Danh-thuc-con-nguoi-phi-thuong-trong-ban-Tony-Robbins.jpeg'),
(54, 'https://bizbooks.vn/uploads/images/2023/thang-8/tri-tue-cam-xuc-cao-nen-trang.jpg'),
(55, 'https://www.netabooks.vn/Data/Sites/1/media/sach/12-quy-luat-cuoc-doi-than-duoc-cho-cuoc-song-hien-dai/12-quy-luat-cuoc-doi-than-duoc-cho-cuoc-song-hien-dai-870x550.jpg'),

(56, 'https://www.nxbctqg.org.vn/img_data/images/347858793260_m.jpg'),
(57, 'https://m.media-amazon.com/images/I/61dFZ1RHBsL._AC_UF1000,1000_QL80_.jpg'),
(58, 'https://i.ebayimg.com/images/g/utQAAOSwPdljxaaC/s-l1200.jpg'),
(59, 'https://m.media-amazon.com/images/I/71h937MExWL._AC_UF894,1000_QL80_.jpg'),
(60, 'https://cruciallearning.com/wp-content/uploads/2023/12/TPOH-book-cover-440.png'),
(61, 'https://static.tuoitre.vn/tto/i/s626/2006/05/27/FLErXnLD.jpg'),
(62, 'https://upload.wikimedia.org/wikipedia/vi/thumb/b/bd/Murder_on_the_Orient_Express_teaser_poster.jpg/250px-Murder_on_the_Orient_Express_teaser_poster.jpg'),
(63, 'https://m.media-amazon.com/images/M/MV5BMTg0NjEwNjUxM15BMl5BanBnXkFtZTcwMzk0MjQ5Mg@@._V1_.jpg'),
(64, 'https://upload.wikimedia.org/wikipedia/vi/a/ab/Hunger_games.jpg'),
(65, 'https://cdn1.fahasa.com/media/catalog/product/i/m/image_195509_1_20170.jpg'),
(66, 'https://m.media-amazon.com/images/I/71Dwg8WlApL._AC_UF1000,1000_QL80_.jpg'),

(67, 'https://m.media-amazon.com/images/M/MV5BNTlkYjBlZTctZjg2YS00NDMzLTlkMTMtNWExMGYyOTliMmEzXkEyXkFqcGc@._V1_.jpg'),
(68, 'https://salt.tikicdn.com/cache/w1200/ts/product/fa/ca/b7/baedb1fb96d1c3f9926f931e9f7365be.jpg'),
(69, 'https://upload.wikimedia.org/wikipedia/en/a/a2/Catching_Fire_%28Suzanne_Collins_novel_-_cover_art%29.jpg'),
(70, 'https://prodimage.images-bn.com/pimages/9780553381689_p0_v3_s600x595.jpg'),
(71, 'https://www.netabooks.vn/Data/Sites/1/media/sach-2021/truong-hoc-sang-tao/truong-hoc-sang-tao.jpg'),
(72, 'https://product.hstatic.net/200000845405/product/2024_03_09_11_36_36_1-390x510_da722307258343a7884f19e7095984a6_master.jpg'),
(73, 'https://minhkhai.com.vn/hinhlon/8934994081719.jpg'),
(74, 'https://researchcoach.edu.vn/wp-content/uploads/2024/07/Screenshot-2025-04-08-235908.png'),
(75, 'https://www.netabooks.vn/Data/Sites/1/Product/49731/dan-chu-va-giao-duc-bia-cung-4.jpg'),
(76, 'https://images.blinkist.io/images/books/57c1769b4a1a18000344dd05/1_1/470.jpg'),
(77, 'https://shopngoaingu.com/wp-content/uploads/Khan-Academy-Math-College-Board.png'),

(78, 'https://m.media-amazon.com/images/I/71002bwrVmL.jpg_BO30,255,255,255_UF900,850_SR1910,1000,0,C_QL100_.jpg'),
(79, 'https://m.media-amazon.com/images/I/810hMz78bzS._UF1000,1000_QL80_.jpg'),
(80, 'https://m.media-amazon.com/images/I/51HOyN8qkxL._AC_UF1000,1000_QL80_.jpg'),
(81, 'https://giaokhoaonline.com/wp-content/uploads/2024/06/Toan-10-Tap-1-Bo-Chan-Troi.jpg'),
(82, 'https://sachgiaokhoa.vn/pub/media/catalog/product/cache/3bd4b739bad1f096e12e3a82b40e551a/s/g/sgk-l10-gd-997.jpg'),
(83, 'https://sachgiaokhoa.vn/pub/media/catalog/product/cache/3bd4b739bad1f096e12e3a82b40e551a/s/g/sgk-l10-gd-971.jpg'),
(84, 'https://img.loigiaihay.com/picture/2024/0123/img-5598.png'),
(85, 'https://giaokhoaonline.com/wp-content/uploads/2024/06/Ngu-Van-10-Tap-1-Bo-Chan-Troi.jpg'),
(86, 'https://toanmath.com/wp-content/uploads/2022/12/sach-giao-khoa-toan-11-tap-1-ket-noi-tri-thuc-voi-cuoc-song.png'),
(87, 'https://vietjack.com/sach-moi/images/sach-vat-li-lop-11-ket-noi-tri-thuc-sua2024-1.PNG'),
(88, 'https://online.pubhtml5.com/yemmo/lfgb/files/large/1.jpg'),

(89, 'https://cdn1.fahasa.com/media/catalog/product/9/7/9786040350466.jpg'),
(90, 'https://sobee.vn/site/wp-content/uploads/2023/07/Ngu-van-11-tap-mot-Chan-troi-sang-tao-1.png'),
(91, 'https://pos.nvncdn.com/fd5775-40602/ps/20240329_LRErpdCwzC.jpeg'),
(92, 'https://librireading.com/wp-content/uploads/2021/05/Deep-work.jpg'),
(93, 'https://www.oskareggert.com/content/images/size/w2000/2024/02/image_67203329.JPG'),
(94, 'https://accidentallyretired.com/wp-content/uploads/2024/04/The-Subtle-Art-of-Not-Giving-A-Fck.jpg'),
(95, 'https://gregmckeown.com/wp-content/uploads/2011/08/book-1225x1600.jpg'),
(96, 'https://images.spiderum.com/sp-images/ea98b95055f511ee8b4f03a873823375.jpeg'),
(97, 'https://m.media-amazon.com/images/I/91fmmjCP6FL._UF1000,1000_QL80_.jpg'),
(98, 'https://images.blinkist.io/images/books/55ae019b3366610007000000/1_1/470.jpg'),
(99, 'https://miro.medium.com/1*mbvSfi8iCskar-FV2HQNTQ.jpeg'),

(100, 'https://m.media-amazon.com/images/I/61V8g4GgqdL._AC_UF894,1000_QL80_.jpg'),
(101, 'https://salt.tikicdn.com/cache/w300/media/catalog/product/4/3/43-the-silk-roads.u5387.d20170707.t143820.418412.jpg'),
(102, 'https://cdn1.fahasa.com/media/catalog/product/i/m/image_195509_1_34822.jpg'),
(103, 'https://cdn1.fahasa.com/media/catalog/product/i/m/image_105944.jpg'),
(104, 'https://static-ppimages.freetls.fastly.net/nielsens/9781529309416.jpg?canvas=600,600&fit=bounds&height=600&mode=max&width=600&404=default.jpg'),
(105, 'https://od.nhungvisao.com/Content/Upload/OldWebImage/1491---Nhung-kham-pha-moi-ve-Chau-My-thoi-ky-tien-Columbus-2024123164123.jpg'),
(106, 'https://salt.tikicdn.com/cache/w300/ts/product/68/96/a8/236df1ef03fe7c33b9a8afb140f34fd8.jpg'),
(107, 'https://thuviennguyenvanhuong.vn/wp-content/uploads/2019/11/IMG20191112103218-scaled.jpg'),
(108, 'https://thefirstedition-prod.s3.us-east-2.amazonaws.com/wp-content/uploads/2025/05/09214049/Shirer-William-L_The-Rise-and-Fall-of-the-Third-Reich_17100-7.jpg'),
(109, 'https://www.stanfords.co.uk/media/catalog/product/265x265/8/1/814moxqfppl._sl1500_.jpg'),
(110, 'https://nxbhcm.com.vn/Image/Biasach/1462B7D6-9968-4F0E-B3C1-F856BE898B9D.jpeg'),

(111, 'https://photo.znews.vn/w660/Uploaded/mdf_fedrei/2022_06_19/286195130_2853583004937123_9177634685073712867_n.jpg'),
(112, 'https://image.sggp.org.vn/w1000/Uploaded/2025/naeyut/2021_06_09/b2d5d9c8-1801-4099-b9ca-cf912d27bbee_knux.jpg.webp'),
(113, 'https://product.hstatic.net/200000122283/product/claude_monet_35539d5c33c64954abfbc3ef69dbe65e_master.jpg'),
(114, 'https://www.netabooks.vn/Data/Sites/1/Product/69669/bat-mi-doi-hoa-si-frida-kahlo-nghe-thuat-cua-cuoc-song-2.jpg'),
(115, 'https://image.ngaynay.vn/w890/Uploaded/2025/xqeiodvsxr/2022_08_29/z3648077475241-527f77a62b95368f9c4a2b17499779bd-2588.jpg'),
(116, 'https://congdankhuyenhoc.qltns.mediacdn.vn/449484899827462144/2022/7/15/z3561014545450e6b6ca8ecd9b29648182958b1b39e86e-16578574416941917640416.jpg'),
(117, 'https://thebookland.vn/contents/1656496439731_z3529167149992_1cf35f8dec6189613bba827769312431.jpg'),
(118, 'https://abook.vn/img-abook.vn/hoi-hoa-truu-tuong-chang-duong-nam-muoi-nam-hoan-thien-tu-kadinsky-toi-jackson-pollock.webp'),
(119, 'https://images-na.ssl-images-amazon.com/images/I/71NttxFWLmL.jpg'),
(120, 'https://m.media-amazon.com/images/I/91q7YInXiaL._AC_UF894,1000_QL80_.jpg'),

(121, 'https://m.media-amazon.com/images/I/71DortY2MXL._AC_UF350,350_QL50_.jpg'),
(122, 'https://nhasachdaruma.com/wp-content/uploads/2021/07/english-vocabulary-in-use-elementary.jpg'),
(123, 'https://cdn1.fahasa.com/media/catalog/product/i/m/image_195509_1_28786.jpg'),
(124, 'https://m.media-amazon.com/images/I/81G2jGK6XlL._AC_UF1000,1000_QL80_.jpg'),
(125, 'https://ieltscaptoc.com.vn/wp-content/uploads/2022/05/English-Phrasal-Verbs-in-Use.jpg'),
(126, 'https://cdn.hstatic.net/products/200000481913/81c6e408-2cf1-4ba4-bebf-cda8d09fc3d2_16dd59a258c948b39656e45e89e63cad_master.jpg'),
(127, 'https://images.routledge.com/common/jackets/crclarge/978041571/9780415716345.jpg'),
(128, 'https://i.dr.com.tr/cache/600x600-0/originals/0000000454222-1.jpg'),
(129, 'https://www.aland.edu.vn/uploads/images/userfiles/2019/07/oxford-word-skills-intermidiate-aland-ielts.jpg'),
(130, 'https://images.gatesnotes.com/12514eb8-7b51-008e-41a9-512542cf683b/a1460f50-80d4-456c-b032-9414312b540a/Holida_Books_2019-Image_02-1200px_by_630px-001.jpg'),

(131, 'https://nutritionfacts.org/app/themes/sage/dist/images/books/how-not-to-die-anniversary-large_f184e0f7.jpg'),
(132, 'https://www.cairnsmoirconnections.org/uploads/4/1/4/7/41470649/s549503630596007947_p69_i2_w1523.jpeg'),
(133, 'https://www.parallax.org/wp-content/uploads/2021/01/9781937006723-fullsize-rgb-400x600.jpg'),
(134, 'https://m.media-amazon.com/images/I/71wRJyJ59lL.jpg_BO30,255,255,255_UF900,850_SR1910,1000,0,C_QL100_.jpg'),
(135, 'https://salt.tikicdn.com/cache/750x750/ts/product/66/54/c7/27446f04f96c4e6dd3f329956a11b3df.jpg'),
(136, 'https://cdn1.fahasa.com/media/catalog/product/9/7/9781426221941.jpg'),
(137, 'https://images-na.ssl-images-amazon.com/images/I/81l3xKTTzNL._AC_UL210_SR210,210_.jpg'),
(138, 'https://m.media-amazon.com/images/I/71JlAKmLoHL._AC_UF894,1000_QL80_.jpg'),
(139, 'https://m.media-amazon.com/images/I/617+AOhLcSL._AC_UF894,1000_QL80_.jpg'),
(140, 'https://cdn1.fahasa.com/media/catalog/product/8/9/8935244865097.jpg'),
(141, 'https://bookbuy.vn/Res/Images/Product/naruto-tap-1_95101_1.jpg'),

(142, 'https://salt.tikicdn.com/cache/w300/ts/product/be/14/92/793ea545be33e1b78fa187cb6b4e6cd6.jpg'),
(143, 'https://cdn1.fahasa.com/media/catalog/product/z/5/z5117266272397_fc78a82725916be4f1f3275af4c3df9b.jpg'),
(144, 'https://nhasachtohana.com/public/upload/O2_1.png'),
(145, 'https://vi.wikipedia.org/wiki/T%E1%BA%ADp_tin:Naruto_the_Movie_2_Cover.jpg'),
(146, 'https://cdn1.fahasa.com/media/catalog/product/d/r/dragon-ball-full-color-tap-2.jpg'),
(147, 'https://www.nxbtre.com.vn/Images/Book/nxbtre_full_27522024_045217.jpg'),
(148, 'https://bookbuy.vn/Res/Images/Product/su-mang-than-chet-tap-1-(tai-ban-2014)_35360_1.jpg'),
(149, 'https://cdn1.fahasa.com/media/flashmagazine/images/page_images/my_hero_academia___hoc_vien_sieu_anh_hung_tap_1_midoriya_izuku_khoi_dau_tai_ban_2019/2021_06_22_13_41_40_1-390x510.jpg'),
(150, 'https://salt.tikicdn.com/cache/w300/ts/product/ed/9f/47/7259bd245d88fbd97ddc686705eec385.jpg'),
(151, 'https://salt.tikicdn.com/cache/200x280/ts/product/4d/c7/00/66fa0dbb5dbe1944958635bc3b927ae0.jpg');

----------------------- reviews--------------------
-- ít nhất 4 reviews cho 1 quyển
-- còn lại radom 
CREATE OR REPLACE FUNCTION generate_reviews(total_reviews INT DEFAULT 650)
RETURNS VOID AS
$$
DECLARE b RECORD;
		u_id INT;
	    review_count INT := 0;
	    sentences TEXT[];
	    sentence_count INT;
	    review_text TEXT;
BEGIN
    sentences := ARRAY[
        'Màu sách nhìn ngoài rất đẹp, không bị lệch màu.',
        'Bìa sách cứng cáp, cầm chắc tay.',
        'Nội dung trình bày rõ ràng, dễ hiểu.',
        'Đọc khá cuốn, không bị chán.',
        'Giấy in ổn, chữ rõ, không mờ.',
        'Giao hàng nhanh, đóng gói cẩn thận.',
        'Nhận sách không bị móp méo.',
        'Mua đúng đợt giảm giá nên rất hài lòng.',
        'So với giá tiền thì chất lượng khá tốt.',
        'Phù hợp để đọc lâu dài.',
        'Nội dung đúng như mô tả.',
        'Sách mới 100%, không có dấu hiệu bị dùng.',
		'Màu bìa nhìn ngoài rất đẹp. Nội dung trình bày rõ ràng.',
        'Sách mới, không trầy xước. Giao nhanh.',
        'Giấy in tốt, chữ rõ. Đáng tiền.',
        'Mua được lúc khuyến mãi nên rất thích.',
        'Đọc giải trí ổn, phù hợp nhiều đối tượng.',
		'Màu sách đẹp, giấy in rõ ràng. Nội dung dễ theo dõi.',
        'Bìa sách cứng cáp, thiết kế nhìn rất thích. Giao hàng nhanh.',
        'Nội dung sách hữu ích, đọc không bị nhàm chán.',
        'Sách đúng mô tả, đóng gói cẩn thận.',
        'Giá tốt, mua được lúc giảm nên rất hài lòng.'
    ];

    -- Đảm bảo mỗi sách có ít nhất 4 review
    FOR b IN
        SELECT id, created_at FROM book WHERE id BETWEEN 1 AND 151
    LOOP
        FOR i IN 1..4 LOOP
            u_id := (1 + FLOOR(RANDOM() * 40))::INT;

            sentence_count := 1 + FLOOR(RANDOM() * 5);
            review_text := '';

            FOR j IN 1..sentence_count LOOP
                review_text := review_text || ' ' ||
                    sentences[1 + FLOOR(RANDOM() * array_length(sentences, 1))];
            END LOOP;

            INSERT INTO review (book_id, user_id, rating, comment, created_at)
            VALUES (b.id, u_id,(RANDOM() * 4 + 1)::INT, 
			TRIM(review_text), b.created_at + (RANDOM() * INTERVAL '90 days') + INTERVAL '1 day' )
            ON CONFLICT (book_id, user_id) DO NOTHING;

            IF FOUND THEN
                review_count := review_count + 1;
            END IF;
            EXIT WHEN review_count >= total_reviews;
        END LOOP;
    END LOOP;

    -- Sinh thêm review cho đủ total_reviews (650 reviews)
    WHILE review_count < total_reviews LOOP
        SELECT id, created_at
        INTO b
        FROM book
        WHERE id BETWEEN 1 AND 151
        ORDER BY RANDOM()
        LIMIT 1;

        u_id := (1 + FLOOR(RANDOM() * 40))::INT;

        sentence_count := 1 + FLOOR(RANDOM() * 5);
        review_text := '';

        FOR j IN 1..sentence_count LOOP
            review_text := review_text || ' ' ||
                sentences[1 + FLOOR(RANDOM() * array_length(sentences, 1))];
        END LOOP;

        INSERT INTO review (book_id, user_id, rating, comment, created_at)
        VALUES (b.id, u_id,(RANDOM() * 4 + 1)::INT, TRIM(review_text),
           	 b.created_at + (RANDOM() * INTERVAL '120 days') + INTERVAL '2 days')
        ON CONFLICT (book_id, user_id) DO NOTHING;

        IF FOUND THEN
            review_count := review_count + 1;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-------------- favarite book---------------
-- 5-20 sách/user
DO $$
DECLARE
    u RECORD;
    num_books INT;
    chosen_books INT[];
    b_id INT;
    b_created TIMESTAMP;
    book_ids INT[];
BEGIN
    -- Lấy tất cả book id
    SELECT array_agg(id) INTO book_ids FROM book;

    FOR u IN SELECT id FROM "user" LOOP
        num_books := 5 + FLOOR(RANDOM() * 16)::INT;  -- 5–20 sách
        chosen_books := ARRAY[]::INT[];

        WHILE array_length(chosen_books,1) IS NULL OR array_length(chosen_books,1) < num_books LOOP
            b_id := book_ids[1 + FLOOR(RANDOM() * array_length(book_ids,1))::INT];
            SELECT created_at INTO b_created FROM book WHERE id = b_id;

            -- Bỏ qua nếu trùng
            IF NOT b_id = ANY(chosen_books) THEN
                chosen_books := array_append(chosen_books, b_id);

                INSERT INTO favorite_book(user_id, book_id, created_at)
                VALUES (u.id, b_id, b_created + (RANDOM() * INTERVAL '60 days') + INTERVAL '1 day')
                ON CONFLICT (user_id, book_id) DO NOTHING;
            END IF;
        END LOOP;
    END LOOP;
END
$$;


------------------------- book view history ---------------------
-- mỗi user 10-20 sách
DO $$
DECLARE
    u RECORD;
    b_id INT;
    b_created TIMESTAMP;
    viewed_books INT[];
    num_views INT;
    book_ids INT[];
BEGIN
    -- Lấy tất cả book id
    SELECT array_agg(id) INTO book_ids FROM book;

    FOR u IN SELECT id FROM "user" LOOP
        viewed_books := ARRAY[]::INT[];
        num_views := 10 + FLOOR(RANDOM() * 11)::INT;  -- mỗi user xem 10–20 sách

        WHILE array_length(viewed_books,1) IS NULL OR array_length(viewed_books,1) < num_views LOOP
            b_id := book_ids[1 + FLOOR(RANDOM() * array_length(book_ids,1))::INT];

            -- Lấy ngày tạo sách
            SELECT created_at INTO b_created FROM book WHERE id = b_id;

            IF NOT b_id = ANY(viewed_books) THEN
                viewed_books := array_append(viewed_books, b_id);

                INSERT INTO book_view_history(user_id, book_id, viewed_at)
                VALUES (u.id, b_id, b_created + (RANDOM() * INTERVAL '60 days') + INTERVAL '1 day');
            END IF;
        END LOOP;
    END LOOP;
END
$$;


------------------- cart---------------------
--- created_at: giả lập trong 30 ngày gần đây
--- updated_at: luôn sau created_at 0–10 ngày
INSERT INTO cart(user_id, created_at, updated_at) VALUES
(1, NOW() - INTERVAL '10 days', NOW() - INTERVAL '5 days'),
(2, NOW() - INTERVAL '15 days', NOW() - INTERVAL '12 days'),
(3, NOW() - INTERVAL '7 days', NOW() - INTERVAL '3 days'),
(4, NOW() - INTERVAL '20 days', NOW() - INTERVAL '18 days'),
(5, NOW() - INTERVAL '5 days', NOW() - INTERVAL '2 days'),
(6, NOW() - INTERVAL '12 days', NOW() - INTERVAL '7 days'),
(7, NOW() - INTERVAL '8 days', NOW() - INTERVAL '6 days'),
(8, NOW() - INTERVAL '18 days', NOW() - INTERVAL '15 days'),
(9, NOW() - INTERVAL '9 days', NOW() - INTERVAL '4 days'),
(10, NOW() - INTERVAL '25 days', NOW() - INTERVAL '20 days'),
(11, NOW() - INTERVAL '14 days', NOW() - INTERVAL '10 days'),
(12, NOW() - INTERVAL '11 days', NOW() - INTERVAL '7 days'),
(13, NOW() - INTERVAL '6 days', NOW() - INTERVAL '3 days'),
(14, NOW() - INTERVAL '16 days', NOW() - INTERVAL '12 days'),
(15, NOW() - INTERVAL '13 days', NOW() - INTERVAL '8 days'),
(16, NOW() - INTERVAL '19 days', NOW() - INTERVAL '14 days'),
(17, NOW() - INTERVAL '4 days', NOW() - INTERVAL '2 days'),
(18, NOW() - INTERVAL '21 days', NOW() - INTERVAL '17 days'),
(19, NOW() - INTERVAL '3 days', NOW() - INTERVAL '1 day'),
(20, NOW() - INTERVAL '23 days', NOW() - INTERVAL '18 days'),
(21, NOW() - INTERVAL '7 days', NOW() - INTERVAL '5 days'),
(22, NOW() - INTERVAL '10 days', NOW() - INTERVAL '6 days'),
(23, NOW() - INTERVAL '15 days', NOW() - INTERVAL '12 days'),
(24, NOW() - INTERVAL '2 days', NOW() - INTERVAL '1 day'),
(25, NOW() - INTERVAL '8 days', NOW() - INTERVAL '5 days'),
(26, NOW() - INTERVAL '14 days', NOW() - INTERVAL '10 days'),
(27, NOW() - INTERVAL '6 days', NOW() - INTERVAL '3 days'),
(28, NOW() - INTERVAL '9 days', NOW() - INTERVAL '4 days'),
(29, NOW() - INTERVAL '12 days', NOW() - INTERVAL '8 days'),
(30, NOW() - INTERVAL '11 days', NOW() - INTERVAL '7 days'),
(31, NOW() - INTERVAL '5 days', NOW() - INTERVAL '2 days'),
(32, NOW() - INTERVAL '18 days', NOW() - INTERVAL '14 days'),
(33, NOW() - INTERVAL '20 days', NOW() - INTERVAL '17 days'),
(34, NOW() - INTERVAL '13 days', NOW() - INTERVAL '9 days'),
(35, NOW() - INTERVAL '16 days', NOW() - INTERVAL '12 days'),
(36, NOW() - INTERVAL '7 days', NOW() - INTERVAL '3 days'),
(37, NOW() - INTERVAL '10 days', NOW() - INTERVAL '6 days'),
(38, NOW() - INTERVAL '5 days', NOW() - INTERVAL '2 days'),
(39, NOW() - INTERVAL '12 days', NOW() - INTERVAL '8 days'),
(40, NOW() - INTERVAL '9 days', NOW() - INTERVAL '5 days');


-- ------------------cart item-----------------
-- cart_id = 1–40 (theo cart đã tạo cho 40 user)
-- book_id = 1–151
-- quantity = 1–5 (random giả lập)
-- price = sale_price của sách
DO $$
DECLARE
    c RECORD;
    b_id INT;
    b_price NUMERIC(10,2);
    cart_books INT[];
    num_items INT;
    book_ids INT[];
BEGIN
    -- Lấy tất cả book id
    SELECT array_agg(id) INTO book_ids FROM book;

    FOR c IN SELECT id FROM cart LOOP
        cart_books := ARRAY[]::INT[];
        num_items := 1 + FLOOR(RANDOM() * 10)::INT;  -- 1–10 sách cho mỗi cart

        WHILE array_length(cart_books,1) IS NULL OR array_length(cart_books,1) < num_items LOOP
            b_id := book_ids[1 + FLOOR(RANDOM() * array_length(book_ids,1))::INT];

            IF NOT b_id = ANY(cart_books) THEN
                cart_books := array_append(cart_books, b_id);

                -- Lấy giá sale_price
                SELECT sale_price INTO b_price FROM book WHERE id = b_id;

                INSERT INTO cart_item(cart_id, book_id, quantity, price)
                VALUES (
                    c.id,
                    b_id,
                    1 + FLOOR(RANDOM() * 5)::INT,  -- quantity 1–5
                    b_price
                )
                ON CONFLICT (cart_id, book_id) DO NOTHING;
            END IF;
        END LOOP;
    END LOOP;
END
$$;

-------------------voucher------------------
-- FREESHIP: 4 voucher đầu, discount_value = 0, voucher_type = 'freeship'.
-- Percent: giảm 10–15%, tên dạng VOUCHER{giá trị}%
-- Fixed: giảm 10k–50k, tên dạng VOUCHER{giá trị}K
-- min_order_amount: random trong khoảng 0–200k
-- start_date / end_date: giả lập ±30–60 ngày từ hiện tại
-- quantity: 50–100 (cố định để demo)
-- is_active = TRUE
INSERT INTO voucher(name, voucher_type, discount_value, min_order_amount, start_date, end_date, quantity, is_active) VALUES
-- 4 Voucher FREESHIP
('FREESHIP1', 'freeship', 0, 15000, NOW() - INTERVAL '10 days', NOW() + INTERVAL '40 days', 75, TRUE),
('FREESHIP2', 'freeship', 0, 5000, NOW() - INTERVAL '5 days', NOW() + INTERVAL '50 days', 80, TRUE),
('FREESHIP3', 'freeship', 0, 20000, NOW() - INTERVAL '12 days', NOW() + INTERVAL '45 days', 60, TRUE),
('FREESHIP4', 'freeship', 0, 10000, NOW() - INTERVAL '8 days', NOW() + INTERVAL '55 days', 90, TRUE),
-- 16 Voucher giảm tiền hoặc %
('VOUCHER10P', 'percent', 10, 50000, NOW() - INTERVAL '15 days', NOW() + INTERVAL '40 days', 70, TRUE),
('VOUCHER12P', 'percent', 12, 80000, NOW() - INTERVAL '20 days', NOW() + INTERVAL '45 days', 65, TRUE),
('VOUCHER15P', 'percent', 15, 60000, NOW() - INTERVAL '10 days', NOW() + INTERVAL '35 days', 75, TRUE),
('VOUCHER25K', 'fixed', 25000, 40000, NOW() - INTERVAL '18 days', NOW() + INTERVAL '50 days', 80, TRUE),
('VOUCHER40K', 'fixed', 40000, 100000, NOW() - INTERVAL '12 days', NOW() + INTERVAL '38 days', 60, TRUE),
('VOUCHER30K', 'fixed', 30000, 70000, NOW() - INTERVAL '7 days', NOW() + INTERVAL '45 days', 70, TRUE),
('VOUCHER20K', 'fixed', 20000, 50000, NOW() - INTERVAL '14 days', NOW() + INTERVAL '50 days', 75, TRUE),
('VOUCHER10K', 'fixed', 10000, 20000, NOW() - INTERVAL '9 days', NOW() + INTERVAL '40 days', 90, TRUE),
('VOUCHER11P', 'percent', 11, 30000, NOW() - INTERVAL '16 days', NOW() + INTERVAL '42 days', 65, TRUE),
('VOUCHER13P', 'percent', 13, 60000, NOW() - INTERVAL '13 days', NOW() + INTERVAL '47 days', 70, TRUE),
('VOUCHER14P', 'percent', 14, 50000, NOW() - INTERVAL '11 days', NOW() + INTERVAL '43 days', 80, TRUE),
('VOUCHER18K', 'fixed', 18000, 40000, NOW() - INTERVAL '10 days', NOW() + INTERVAL '48 days', 60, TRUE),
('VOUCHER22K', 'fixed', 22000, 70000, NOW() - INTERVAL '8 days', NOW() + INTERVAL '50 days', 75, TRUE),
('VOUCHER15K', 'fixed', 15000, 30000, NOW() - INTERVAL '5 days', NOW() + INTERVAL '45 days', 85, TRUE),
('VOUCHER50K', 'fixed', 50000, 100000, NOW() - INTERVAL '12 days', NOW() + INTERVAL '55 days', 70, TRUE),
('VOUCHER10P', 'percent', 10, 20000, NOW() - INTERVAL '9 days', NOW() + INTERVAL '40 days', 80, TRUE);

-------------------------- user voucher-------------------
-- 40 user × 3 voucher = 120 dòng
-- Mỗi user: 1 freeship + 2 voucher giảm tiền/percent
-- claimed_at trong khoảng ngày hiện tại – 12–15 ngày trước (giả lập)
-- used = FALSE
INSERT INTO user_voucher(user_id, voucher_id, used, claimed_at) VALUES
-- User 1
(1, 1, FALSE, NOW() - INTERVAL '10 days'),
(1, 5, FALSE, NOW() - INTERVAL '9 days'),
(1, 7, FALSE, NOW() - INTERVAL '8 days'),
-- User 2
(2, 2, FALSE, NOW() - INTERVAL '12 days'),
(2, 6, FALSE, NOW() - INTERVAL '11 days'),
(2, 8, FALSE, NOW() - INTERVAL '10 days'),
-- User 3
(3, 3, FALSE, NOW() - INTERVAL '15 days'),
(3, 5, FALSE, NOW() - INTERVAL '13 days'),
(3, 9, FALSE, NOW() - INTERVAL '12 days'),
-- User 4
(4, 4, FALSE, NOW() - INTERVAL '14 days'),
(4, 6, FALSE, NOW() - INTERVAL '12 days'),
(4, 10, FALSE, NOW() - INTERVAL '11 days'),
-- User 5
(5, 1, FALSE, NOW() - INTERVAL '10 days'),
(5, 11, FALSE, NOW() - INTERVAL '9 days'),
(5, 12, FALSE, NOW() - INTERVAL '8 days'),
-- User 6
(6, 2, FALSE, NOW() - INTERVAL '13 days'),
(6, 7, FALSE, NOW() - INTERVAL '11 days'),
(6, 13, FALSE, NOW() - INTERVAL '10 days'),
-- User 7
(7, 3, FALSE, NOW() - INTERVAL '12 days'),
(7, 8, FALSE, NOW() - INTERVAL '11 days'),
(7, 14, FALSE, NOW() - INTERVAL '9 days'),
-- User 8
(8, 4, FALSE, NOW() - INTERVAL '11 days'),
(8, 9, FALSE, NOW() - INTERVAL '10 days'),
(8, 15, FALSE, NOW() - INTERVAL '8 days'),
-- User 9
(9, 1, FALSE, NOW() - INTERVAL '10 days'),
(9, 5, FALSE, NOW() - INTERVAL '9 days'),
(9, 16, FALSE, NOW() - INTERVAL '7 days'),
-- User 10
(10, 2, FALSE, NOW() - INTERVAL '9 days'),
(10, 6, FALSE, NOW() - INTERVAL '8 days'),
(10, 17, FALSE, NOW() - INTERVAL '6 days'),
-- User 11
(11, 3, FALSE, NOW() - INTERVAL '14 days'),
(11, 7, FALSE, NOW() - INTERVAL '13 days'),
(11, 12, FALSE, NOW() - INTERVAL '11 days'),
-- User 12
(12, 4, FALSE, NOW() - INTERVAL '13 days'),
(12, 8, FALSE, NOW() - INTERVAL '12 days'),
(12, 14, FALSE, NOW() - INTERVAL '10 days'),
-- User 13
(13, 1, FALSE, NOW() - INTERVAL '12 days'),
(13, 9, FALSE, NOW() - INTERVAL '11 days'),
(13, 15, FALSE, NOW() - INTERVAL '9 days'),
-- User 14
(14, 2, FALSE, NOW() - INTERVAL '11 days'),
(14, 5, FALSE, NOW() - INTERVAL '10 days'),
(14, 16, FALSE, NOW() - INTERVAL '8 days'),
-- User 15
(15, 3, FALSE, NOW() - INTERVAL '10 days'),
(15, 6, FALSE, NOW() - INTERVAL '9 days'),
(15, 17, FALSE, NOW() - INTERVAL '7 days'),
-- User 16
(16, 4, FALSE, NOW() - INTERVAL '12 days'),
(16, 7, FALSE, NOW() - INTERVAL '11 days'),
(16, 10, FALSE, NOW() - INTERVAL '9 days'),
-- User 17
(17, 1, FALSE, NOW() - INTERVAL '11 days'),
(17, 8, FALSE, NOW() - INTERVAL '10 days'),
(17, 12, FALSE, NOW() - INTERVAL '8 days'),
-- User 18
(18, 2, FALSE, NOW() - INTERVAL '10 days'),
(18, 9, FALSE, NOW() - INTERVAL '9 days'),
(18, 14, FALSE, NOW() - INTERVAL '7 days'),
-- User 19
(19, 3, FALSE, NOW() - INTERVAL '12 days'),
(19, 5, FALSE, NOW() - INTERVAL '11 days'),
(19, 15, FALSE, NOW() - INTERVAL '9 days'),
-- User 20
(20, 4, FALSE, NOW() - INTERVAL '11 days'),
(20, 6, FALSE, NOW() - INTERVAL '10 days'),
(20, 16, FALSE, NOW() - INTERVAL '8 days'),
-- User 21
(21, 1, FALSE, NOW() - INTERVAL '10 days'),
(21, 7, FALSE, NOW() - INTERVAL '9 days'),
(21, 17, FALSE, NOW() - INTERVAL '7 days'),
-- User 22
(22, 2, FALSE, NOW() - INTERVAL '12 days'),
(22, 8, FALSE, NOW() - INTERVAL '11 days'),
(22, 13, FALSE, NOW() - INTERVAL '9 days'),
-- User 23
(23, 3, FALSE, NOW() - INTERVAL '11 days'),
(23, 5, FALSE, NOW() - INTERVAL '10 days'),
(23, 15, FALSE, NOW() - INTERVAL '8 days'),
-- User 24
(24, 4, FALSE, NOW() - INTERVAL '10 days'),
(24, 6, FALSE, NOW() - INTERVAL '9 days'),
(24, 12, FALSE, NOW() - INTERVAL '7 days'),
-- User 25
(25, 1, FALSE, NOW() - INTERVAL '11 days'),
(25, 7, FALSE, NOW() - INTERVAL '10 days'),
(25, 14, FALSE, NOW() - INTERVAL '8 days'),
-- User 26
(26, 2, FALSE, NOW() - INTERVAL '12 days'),
(26, 8, FALSE, NOW() - INTERVAL '11 days'),
(26, 16, FALSE, NOW() - INTERVAL '9 days'),
-- User 27
(27, 3, FALSE, NOW() - INTERVAL '10 days'),
(27, 5, FALSE, NOW() - INTERVAL '9 days'),
(27, 17, FALSE, NOW() - INTERVAL '7 days'),
-- User 28
(28, 4, FALSE, NOW() - INTERVAL '11 days'),
(28, 6, FALSE, NOW() - INTERVAL '10 days'),
(28, 10, FALSE, NOW() - INTERVAL '8 days'),
-- User 29
(29, 1, FALSE, NOW() - INTERVAL '12 days'),
(29, 7, FALSE, NOW() - INTERVAL '11 days'),
(29, 12, FALSE, NOW() - INTERVAL '9 days'),
-- User 30
(30, 2, FALSE, NOW() - INTERVAL '10 days'),
(30, 8, FALSE, NOW() - INTERVAL '9 days'),
(30, 13, FALSE, NOW() - INTERVAL '7 days'),
-- User 31
(31, 3, FALSE, NOW() - INTERVAL '11 days'),
(31, 5, FALSE, NOW() - INTERVAL '10 days'),
(31, 14, FALSE, NOW() - INTERVAL '8 days'),
-- User 32
(32, 4, FALSE, NOW() - INTERVAL '10 days'),
(32, 6, FALSE, NOW() - INTERVAL '9 days'),
(32, 16, FALSE, NOW() - INTERVAL '7 days'),
-- User 33
(33, 1, FALSE, NOW() - INTERVAL '11 days'),
(33, 7, FALSE, NOW() - INTERVAL '10 days'),
(33, 17, FALSE, NOW() - INTERVAL '8 days'),
-- User 34
(34, 2, FALSE, NOW() - INTERVAL '12 days'),
(34, 8, FALSE, NOW() - INTERVAL '11 days'),
(34, 10, FALSE, NOW() - INTERVAL '9 days'),
-- User 35
(35, 3, FALSE, NOW() - INTERVAL '10 days'),
(35, 5, FALSE, NOW() - INTERVAL '9 days'),
(35, 12, FALSE, NOW() - INTERVAL '7 days'),
-- User 36
(36, 4, FALSE, NOW() - INTERVAL '11 days'),
(36, 6, FALSE, NOW() - INTERVAL '10 days'),
(36, 14, FALSE, NOW() - INTERVAL '8 days'),
-- User 37
(37, 1, FALSE, NOW() - INTERVAL '12 days'),
(37, 7, FALSE, NOW() - INTERVAL '11 days'),
(37, 16, FALSE, NOW() - INTERVAL '9 days'),
-- User 38
(38, 2, FALSE, NOW() - INTERVAL '10 days'),
(38, 8, FALSE, NOW() - INTERVAL '9 days'),
(38, 17, FALSE, NOW() - INTERVAL '7 days'),
-- User 39
(39, 3, FALSE, NOW() - INTERVAL '11 days'),
(39, 5, FALSE, NOW() - INTERVAL '10 days'),
(39, 14, FALSE, NOW() - INTERVAL '8 days'),
-- User 40
(40, 4, FALSE, NOW() - INTERVAL '10 days'),
(40, 6, FALSE, NOW() - INTERVAL '9 days'),
(40, 12, FALSE, NOW() - INTERVAL '7 days');

------------------------order---------------------
DO $$
DECLARE
    u RECORD;
    o_count INT;
    i INT;
    pay_method VARCHAR(10);
    status_arr TEXT[] := ARRAY['Đang xử lý','Đang giao', 'Hoàn thành', 'Đã huỷ'];
    ord_status VARCHAR(20);
    uv RECORD;
    pc RECORD;
    total_price NUMERIC(12,2);
    total_amount NUMERIC(12,2);
BEGIN
    FOR u IN 
        SELECT id, address 
        FROM "user"
        WHERE address IS NOT NULL
    LOOP
        o_count := 1 + FLOOR(RANDOM() * 5)::INT; -- 1–5 order mỗi user

        FOR i IN 1..o_count LOOP
            -- Payment method
            IF RANDOM() < 0.7 THEN
                pay_method := 'COD';
            ELSE
                pay_method := 'Card';
            END IF;

            -- Status ngẫu nhiên
            ord_status := status_arr[
                1 + FLOOR(RANDOM() * array_length(status_arr, 1))::INT
            ];

            -- Chọn voucher (user_voucher) nếu có
            SELECT id INTO uv
            FROM user_voucher
            WHERE user_id = u.id
            ORDER BY RANDOM()
            LIMIT 1;

            -- Chọn promo code ngẫu nhiên
            SELECT id, discount_percent, discount_amount INTO pc
            FROM promo_code
            WHERE is_active = TRUE
            ORDER BY RANDOM()
            LIMIT 1;

            -- Tổng tiền giả lập
            total_price := 50000 + FLOOR(RANDOM() * 450001); -- 50k–500k
            total_amount := total_price;

            -- Giảm voucher
            IF uv.id IS NOT NULL THEN
                total_amount := total_amount - FLOOR(RANDOM() * 50000);
            END IF;

            -- Giảm promo
            IF pc.id IS NOT NULL THEN
                IF pc.discount_percent > 0 THEN
                    total_amount := total_amount * (1 - pc.discount_percent / 100.0);
                ELSE
                    total_amount := total_amount - pc.discount_amount;
                END IF;
            END IF;

            -- Không cho âm
            IF total_amount < 0 THEN
                total_amount := 0;
            END IF;

            -- Insert order
            INSERT INTO "order" (
                user_id,
                payment_method,
                created_at,
                status,
                shipping_address,
                user_voucher_id,
                promo_code_id,
                total_price,
                total_amount
            )
            VALUES (
                u.id,
                pay_method,
                NOW() - (RANDOM() * INTERVAL '60 days'),
                ord_status,
                u.address,      
                uv.id,
                pc.id,
                total_price,
                total_amount
            );
        END LOOP;
    END LOOP;
END
$$;

--------------------------- order item ----------------------
DO $$
DECLARE
    o RECORD;
    num_books INT;
    b_id INT;
    b_price NUMERIC(12,2);
    chosen_books INT[];
    book_ids INT[];
BEGIN
    -- Lấy tất cả book id
    SELECT array_agg(id) INTO book_ids FROM book;

    FOR o IN SELECT id FROM "order" LOOP
        chosen_books := ARRAY[]::INT[];
        num_books := 1 + FLOOR(RANDOM() * 5)::INT; -- 1–5 sách mỗi order

        WHILE array_length(chosen_books,1) IS NULL OR array_length(chosen_books,1) < num_books LOOP
            b_id := book_ids[1 + FLOOR(RANDOM() * array_length(book_ids,1))::INT];

            IF NOT b_id = ANY(chosen_books) THEN
                chosen_books := array_append(chosen_books, b_id);

                -- Lấy giá sale_price
                SELECT sale_price INTO b_price FROM book WHERE id = b_id;

                INSERT INTO order_item(order_id, book_id, quantity, price)
                VALUES (
                    o.id,
                    b_id,
                    1 + FLOOR(RANDOM() * 5)::INT,  -- quantity 1–5
                    b_price
                );
            END IF;
        END LOOP;
    END LOOP;
END
$$;

----------------------- recommendation_engine ---------------------
DO $$
DECLARE
    u RECORD;
    rec_count INT;
    i INT;
BEGIN
    FOR u IN SELECT id FROM "user" LOOP
        rec_count := 1 + FLOOR(RANDOM() * 3)::INT; -- 1–3 record mỗi user
        FOR i IN 1..rec_count LOOP
            INSERT INTO recommendation_engine(user_id, created_at)
            VALUES (u.id, NOW() - (RANDOM() * INTERVAL '30 days'));
        END LOOP;
    END LOOP;
END
$$;
SELECT COUNT(*) FROM recommendation_engine;
SELECT * FROM recommendation_engine;

-----------------------recommendation_engine_order_history-------------------------
DO $$
DECLARE
    rec RECORD;
    book_ids INT[];
    b_id INT;
    num_books INT;
    chosen_books INT[];
BEGIN
    -- Lặp qua từng record recommendation_engine
    FOR rec IN SELECT id, user_id FROM recommendation_engine LOOP

        -- Lấy tất cả sách user từng order + favorite
        SELECT array_agg(DISTINCT book_id) INTO book_ids
        FROM (
            SELECT oi.book_id
            FROM order_item oi
            JOIN "order" o ON oi.order_id = o.id
            WHERE o.user_id = rec.user_id
            UNION
            SELECT fb.book_id
            FROM favorite_book fb
            WHERE fb.user_id = rec.user_id
        ) AS user_books;

        -- Nếu user có sách
        IF book_ids IS NOT NULL THEN
            chosen_books := ARRAY[]::INT[];
            num_books := LEAST(5, array_length(book_ids,1)); -- 1–5 sách
            WHILE array_length(chosen_books,1) < num_books LOOP
                b_id := book_ids[1 + FLOOR(RANDOM() * array_length(book_ids,1))::INT];

                IF NOT b_id = ANY(chosen_books) THEN
                    chosen_books := array_append(chosen_books, b_id);

                    -- Insert vào recommendation history
                    INSERT INTO recommendation_engine_order_history(recommendation_engine_id, book_id)
                    VALUES (rec.id, b_id)
                    ON CONFLICT DO NOTHING;
                END IF;
            END LOOP;
        END IF;

    END LOOP;
END
$$;

---------------------reccomendation cache--------------------
DO $$
DECLARE
    u RECORD;
    b_id INT;
    num_books INT;
    chosen_books INT[];
    s REAL;
BEGIN
    FOR u IN SELECT id FROM "user" LOOP
        -- Mỗi user có 5–15 sách gợi ý
        num_books := 5 + FLOOR(RANDOM() * 11)::INT;
        chosen_books := ARRAY[]::INT[];

        WHILE COALESCE(array_length(chosen_books,1),0) < num_books LOOP
            b_id := 1 + FLOOR(RANDOM() * 151)::INT; -- 151 sách

            -- Không trùng sách
            IF NOT b_id = ANY(chosen_books) THEN
                chosen_books := array_append(chosen_books, b_id);

                -- Score từ 0.0–1.0
                s := ROUND(RANDOM()::NUMERIC, 2)::REAL;

                -- Insert vào bảng
                INSERT INTO recommendation_cache(user_id, book_id, score, updated_at)
                VALUES (
                    u.id,
                    b_id,
                    s,
                    NOW() - (RANDOM() * INTERVAL '60 days')
                );
            END IF;
        END LOOP;
    END LOOP;
END
$$;

---------------------------banner-------------------
INSERT INTO banner(title, subtitle, image, is_active) VALUES
('Sách ấn tượng', 'Bán sách ấn tượng, chốt đơn ầm ầm.', 'https://tudongchat.com/blog/101-stt-ban-sach-an-tuong/', TRUE),
('Vi vu hội sách', 'Khám phá top sách phát triển bản thân năm 2025', 'https://tiki.vn/khuyen-mai/bizbooks', TRUE),
('Hội sách online', 'Hội sách online, siêu sale đa vũ trụ', 'https://tiki.vn/khuyen-mai/first-news-sach-doc-quyen', TRUE),
('Truyện hè', 'Truyện mới chào hè', 'https://vietgigs.vn/service/thiet-ke-banner-poster-bia-sach-297CC78BEC7D768DBCBC', TRUE),
('Hội sách', 'Hội sách văn học 2023', 'https://vietgigs.vn/service/thiet-ke-banner-poster-bia-sach-297CC78BEC7D768DBCBC', TRUE);

-------------------------promotion--------------------------
-- code: tên mã giảm giá dạng PROMOxx
-- discount_percent: từ 5–50%, phân bổ đều
-- expire_date: từ 20–100 ngày sau ngày hiện tại (NOW())
INSERT INTO promotion(code, discount_percent, expire_date) VALUES
('PROMO10', 10, NOW()::DATE + INTERVAL '30 days'),
('PROMO15', 15, NOW()::DATE + INTERVAL '45 days'),
('PROMO20', 20, NOW()::DATE + INTERVAL '60 days'),
('PROMO25', 25, NOW()::DATE + INTERVAL '30 days'),
('PROMO30', 30, NOW()::DATE + INTERVAL '50 days'),
('PROMO5', 5, NOW()::DATE + INTERVAL '20 days'),
('PROMO12', 12, NOW()::DATE + INTERVAL '35 days'),
('PROMO18', 18, NOW()::DATE + INTERVAL '40 days'),
('PROMO22', 22, NOW()::DATE + INTERVAL '45 days'),
('PROMO28', 28, NOW()::DATE + INTERVAL '60 days'),
('PROMO8', 8, NOW()::DATE + INTERVAL '25 days'),
('PROMO14', 14, NOW()::DATE + INTERVAL '30 days'),
('PROMO17', 17, NOW()::DATE + INTERVAL '40 days'),
('PROMO21', 21, NOW()::DATE + INTERVAL '50 days'),
('PROMO35', 35, NOW()::DATE + INTERVAL '70 days'),
('PROMO40', 40, NOW()::DATE + INTERVAL '90 days'),
('PROMO45', 45, NOW()::DATE + INTERVAL '80 days'),
('PROMO50', 50, NOW()::DATE + INTERVAL '100 days'),
('PROMO7', 7, NOW()::DATE + INTERVAL '20 days'),
('PROMO13', 13, NOW()::DATE + INTERVAL '30 days');

--------------------promo code------------------
-- 50% giảm phần trăm 10–20%
-- 50% giảm tiền 10k–50k
-- Min order 0–200k
-- Ngày hiệu lực trong khoảng 30 ngày trước, kéo dài 30–90 ngày
INSERT INTO promo_code(code, discount_percent, discount_amount, min_order_amount, valid_from, valid_to, is_active) VALUES
('PROMO1', 15, 0, 120000, NOW() - INTERVAL '5 days', NOW() + INTERVAL '40 days', TRUE),
('PROMO2', 0, 35000, 50000, NOW() - INTERVAL '12 days', NOW() + INTERVAL '60 days', TRUE),
('PROMO3', 18, 0, 80000, NOW() - INTERVAL '8 days', NOW() + INTERVAL '50 days', TRUE),
('PROMO4', 0, 20000, 100000, NOW() - INTERVAL '20 days', NOW() + INTERVAL '55 days', TRUE),
('PROMO5', 12, 0, 150000, NOW() - INTERVAL '3 days', NOW() + INTERVAL '45 days', TRUE),
('PROMO6', 0, 50000, 70000, NOW() - INTERVAL '15 days', NOW() + INTERVAL '60 days', TRUE),
('PROMO7', 16, 0, 90000, NOW() - INTERVAL '10 days', NOW() + INTERVAL '35 days', TRUE),
('PROMO8', 0, 30000, 20000, NOW() - INTERVAL '7 days', NOW() + INTERVAL '50 days', TRUE),
('PROMO9', 14, 0, 60000, NOW() - INTERVAL '2 days', NOW() + INTERVAL '40 days', TRUE),
('PROMO10', 0, 15000, 110000, NOW() - INTERVAL '18 days', NOW() + INTERVAL '60 days', TRUE),
('PROMO11', 11, 0, 50000, NOW() - INTERVAL '6 days', NOW() + INTERVAL '30 days', TRUE),
('PROMO12', 0, 40000, 120000, NOW() - INTERVAL '4 days', NOW() + INTERVAL '65 days', TRUE);

------------------customer_promotion--------------------
-- Mỗi user có 1–2 promotion (mình xen kẽ 1–2 user có 2 record)
-- promo_type: ngẫu nhiên 'NEW', 'VIP', 'BIRTHDAY'
-- discount_percent: từ 5–20%
-- start_date trước end_date, ngày trong 30 ngày gần đây
-- is_active = TRUE → dùng được trực tiếp cho web demo
INSERT INTO customer_promotion(user_id, promo_type, discount_percent, start_date, end_date, is_active) VALUES
(1, 'NEW', 10, NOW() - INTERVAL '10 days', NOW() + INTERVAL '40 days', TRUE),
(1, 'VIP', 15, NOW() - INTERVAL '5 days', NOW() + INTERVAL '35 days', TRUE),
(2, 'BIRTHDAY', 12, NOW() - INTERVAL '8 days', NOW() + INTERVAL '38 days', TRUE),
(2, 'NEW', 18, NOW() - INTERVAL '12 days', NOW() + INTERVAL '45 days', TRUE),
(3, 'VIP', 7, NOW() - INTERVAL '3 days', NOW() + INTERVAL '33 days', TRUE),
(4, 'NEW', 14, NOW() - INTERVAL '6 days', NOW() + INTERVAL '36 days', TRUE),
(4, 'BIRTHDAY', 20, NOW() - INTERVAL '9 days', NOW() + INTERVAL '50 days', TRUE),
(5, 'NEW', 9, NOW() - INTERVAL '4 days', NOW() + INTERVAL '32 days', TRUE),
(5, 'VIP', 16, NOW() - INTERVAL '7 days', NOW() + INTERVAL '42 days', TRUE),
(6, 'BIRTHDAY', 11, NOW() - INTERVAL '2 days', NOW() + INTERVAL '30 days', TRUE),
(7, 'NEW', 13, NOW() - INTERVAL '5 days', NOW() + INTERVAL '37 days', TRUE),
(8, 'VIP', 19, NOW() - INTERVAL '8 days', NOW() + INTERVAL '48 days', TRUE),
(9, 'BIRTHDAY', 10, NOW() - INTERVAL '6 days', NOW() + INTERVAL '40 days', TRUE),
(10, 'NEW', 12, NOW() - INTERVAL '3 days', NOW() + INTERVAL '35 days', TRUE),
(11, 'VIP', 15, NOW() - INTERVAL '7 days', NOW() + INTERVAL '43 days', TRUE),
(12, 'BIRTHDAY', 8, NOW() - INTERVAL '4 days', NOW() + INTERVAL '33 days', TRUE),
(13, 'NEW', 14, NOW() - INTERVAL '9 days', NOW() + INTERVAL '44 days', TRUE),
(14, 'VIP', 17, NOW() - INTERVAL '6 days', NOW() + INTERVAL '41 days', TRUE),
(15, 'BIRTHDAY', 20, NOW() - INTERVAL '5 days', NOW() + INTERVAL '45 days', TRUE),
(16, 'NEW', 11, NOW() - INTERVAL '3 days', NOW() + INTERVAL '36 days', TRUE),
(17, 'VIP', 13, NOW() - INTERVAL '8 days', NOW() + INTERVAL '38 days', TRUE),
(18, 'BIRTHDAY', 15, NOW() - INTERVAL '6 days', NOW() + INTERVAL '40 days', TRUE),
(19, 'NEW', 12, NOW() - INTERVAL '4 days', NOW() + INTERVAL '37 days', TRUE),
(20, 'VIP', 10, NOW() - INTERVAL '5 days', NOW() + INTERVAL '35 days', TRUE),
(21, 'BIRTHDAY', 18, NOW() - INTERVAL '7 days', NOW() + INTERVAL '42 days', TRUE),
(22, 'NEW', 16, NOW() - INTERVAL '6 days', NOW() + INTERVAL '39 days', TRUE),
(23, 'VIP', 12, NOW() - INTERVAL '3 days', NOW() + INTERVAL '33 days', TRUE),
(24, 'BIRTHDAY', 14, NOW() - INTERVAL '5 days', NOW() + INTERVAL '36 days', TRUE),
(25, 'NEW', 9, NOW() - INTERVAL '4 days', NOW() + INTERVAL '34 days', TRUE),
(26, 'VIP', 15, NOW() - INTERVAL '7 days', NOW() + INTERVAL '41 days', TRUE),
(27, 'BIRTHDAY', 20, NOW() - INTERVAL '6 days', NOW() + INTERVAL '45 days', TRUE),
(28, 'NEW', 11, NOW() - INTERVAL '2 days', NOW() + INTERVAL '32 days', TRUE),
(29, 'VIP', 13, NOW() - INTERVAL '5 days', NOW() + INTERVAL '37 days', TRUE),
(30, 'BIRTHDAY', 10, NOW() - INTERVAL '3 days', NOW() + INTERVAL '35 days', TRUE),
(31, 'NEW', 14, NOW() - INTERVAL '6 days', NOW() + INTERVAL '40 days', TRUE),
(32, 'VIP', 12, NOW() - INTERVAL '4 days', NOW() + INTERVAL '36 days', TRUE),
(33, 'BIRTHDAY', 19, NOW() - INTERVAL '7 days', NOW() + INTERVAL '44 days', TRUE),
(34, 'NEW', 15, NOW() - INTERVAL '5 days', NOW() + INTERVAL '38 days', TRUE),
(35, 'VIP', 17, NOW() - INTERVAL '6 days', NOW() + INTERVAL '42 days', TRUE),
(36, 'BIRTHDAY', 16, NOW() - INTERVAL '4 days', NOW() + INTERVAL '40 days', TRUE),
(37, 'NEW', 12, NOW() - INTERVAL '3 days', NOW() + INTERVAL '36 days', TRUE),
(38, 'VIP', 10, NOW() - INTERVAL '5 days', NOW() + INTERVAL '35 days', TRUE),
(39, 'BIRTHDAY', 18, NOW() - INTERVAL '6 days', NOW() + INTERVAL '41 days', TRUE),
(40, 'NEW', 11, NOW() - INTERVAL '4 days', NOW() + INTERVAL '37 days', TRUE);

----------------------product discount---------------------------------
-- Giảm %: 5–20%
-- Giảm tiền: 10k–50k
-- Mỗi sách có thể có 1 record
-- is_active = TRUE
INSERT INTO product_discount(book_id, discount_percent, discount_amount, is_active) VALUES
(1, 10, 0, TRUE),
(2, 0, 20000, TRUE),
(3, 15, 0, TRUE),
(4, 0, 50000, TRUE),
(5, 12, 0, TRUE),
(6, 0, 30000, TRUE),
(7, 18, 0, TRUE),
(8, 0, 15000, TRUE),
(9, 5, 0, TRUE),
(10, 0, 25000, TRUE),
(11, 20, 0, TRUE),
(12, 0, 40000, TRUE),
(13, 10, 0, TRUE),
(14, 0, 35000, TRUE),
(15, 15, 0, TRUE),
(16, 0, 10000, TRUE),
(17, 12, 0, TRUE),
(18, 0, 45000, TRUE),
(19, 17, 0, TRUE),
(20, 0, 50000, TRUE);

