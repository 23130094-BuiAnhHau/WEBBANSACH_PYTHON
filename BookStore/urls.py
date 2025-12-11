from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


from apps.order.views import checkout, order_history, StaticOrderHistoryView # Import View mới
from apps.order.views import StaticOrderDetailView
from apps.user.views import login_view

urlpatterns = [
    path('login/', login_view, name='login'), # Thêm mới, Phải khớp với LOGIN_URL
    path('admin/', admin.site.urls),

# them de test templates tĩnh

   
    path('order-history/', StaticOrderHistoryView.as_view(), name='order_history'),
    path('order-detail/', StaticOrderDetailView.as_view(), name='order_detail'),
    path('checkout/', checkout, name='checkout'),

    # --- Home (ví dụ trang chính chỉ là template tĩnh) ---
    # path('', TemplateView.as_view(template_name="home.html"), name="home"), 
    # đóng tạm để chạy trang checkout... vì chưa có home.html

    # --- App book ---
    path('books/', include('apps.book.urls')),

    # --- App user ---
    # path('', include('apps.user.urls')),

    # --- App cart ---
    path('cart/', include('apps.cart.urls')),

    # --- App order ---
    # path('order/', include('apps.order.urls')),
]

# --- Phục vụ media trong dev ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
