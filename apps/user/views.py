
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.user.forms import RegisterForm
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash

from apps.user.models import Profile



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công! Mời bạn đăng nhập.")
            return redirect("user:login")
        else:
            messages.error(request, "Đăng ký không thành công. Vui lòng kiểm tra lại thông tin.")
    else:
        form = RegisterForm()

    return render(request, "user/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home:home")
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu")

    return render(request, "user/login.html")



@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect("home:home")



@login_required
def profile_view(request):
    user = request.user


    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Lưu User
        user.phone = request.POST.get("phone")
        user.address = request.POST.get("address")
        user.save()

        # Lưu Profile
        profile.date_of_birth = request.POST.get("date_of_birth") or None
        profile.gender = request.POST.get("gender")
        profile.save()

        messages.success(request, "Cập nhật thông tin thành công")
        return redirect("user:profile")

    return render(request, "user/profile.html")



@login_required
def change_password_view(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Mật khẩu hiện tại không đúng")
            return redirect("user:change_password")

        if new_password != confirm_password:
            messages.error(request, "Mật khẩu mới không khớp")
            return redirect("user:change_password")

        if len(new_password) < 6:
            messages.error(request, "Mật khẩu mới phải có ít nhất 6 ký tự")
            return redirect("user:change_password")

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Đổi mật khẩu thành công")
        return redirect("home:home")

    return render(request, "user/change_password.html")
