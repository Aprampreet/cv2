from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup")
        User.objects.create_user(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.success(request, "Account created successfully! Please login.")
        return redirect("profile")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("profile")
        messages.warning('Invalid Caridentials')
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    if request.method == "POST":
        bio = request.POST.get("bio")
        phone = request.POST.get("phone")
        profile_pic = request.FILES.get("profile_pic")
        profile = request.user.profile
        profile.bio = bio
        profile.phone = phone
        if profile_pic:  
            profile.profile_pic = profile_pic
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "accounts/profile.html", {"profile": request.user.profile})



