from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.user.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from django.http import HttpResponse        #thêm để login 
# --- Đăng ký ---
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, "Đăng ký thành công!")
        return redirect("login")
    return render(request, "user/register.html")

# --- Đăng nhập ---
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect("home")
#         else:
#             messages.error(request, "Sai thông tin đăng nhập!")
#     return render(request, "user/login.html")


def login_view(request):
    # Đây là nơi bạn sẽ render form login của mình sau này
    # Tạm thời trả về một trang đơn giản không cần template
    
    return HttpResponse("<h1>Trang Đăng Nhập Tạm Thời Đã Chạy</h1>")


# --- Đăng xuất ---
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

# --- Kiểm tra quyền admin ---
def admin_required(user):
    return user.is_authenticated and user.is_admin
