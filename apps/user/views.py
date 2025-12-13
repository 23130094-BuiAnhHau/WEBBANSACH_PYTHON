from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.user.forms import RegisterForm, LoginForm
from django.http import HttpResponse

# --- Đăng ký ---
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công! Mời bạn đăng nhập.")
            return redirect("user:login")
    else:
        form = RegisterForm()

    return render(request, "user/register.html", {"form": form})

# --- Đăng nhập ---
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home:home")
            else:
                messages.error(request, "Sai tên đăng nhập hoặc mật khẩu")
    else:
        form = LoginForm()

    return render(request, "user/login.html", {"form": form})

# --- Đăng xuất ---
@login_required
def logout_view(request):
    logout(request)
    return redirect("user:login")
