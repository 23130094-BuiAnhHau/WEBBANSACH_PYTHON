from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.user.views import login_view

urlpatterns = [
    # HOME
    path("", include("apps.home.urls")),

    path("user/", include("apps.user.urls")),
    path("order/", include("apps.order.urls")),


    # ADMIN
    path("admin/", admin.site.urls),

    # BOOK + CART
    path("book/", include("apps.book.urls")),
    path("cart/", include("apps.cart.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
