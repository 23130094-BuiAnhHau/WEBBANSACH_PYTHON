from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page - app home
    path('', include('apps.home.urls')), # đã thay đổi ở đây 

    # --- App book ---
    path('books/', include('apps.book.urls')),

    # --- App user ---
    path('', include('apps.user.urls')),

    # --- App cart ---
    path('cart/', include('apps.cart.urls')),

    # --- App order ---
    path('order/', include('apps.order.urls')),
]

# --- Phục vụ media trong dev ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
