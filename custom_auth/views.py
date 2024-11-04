"""Класс содержит методы модуля авторизации"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_method
from django.contrib.auth.hashers import make_password
from custom_auth.models import CustomUser

def registration(request):
    """Функция возвращает страницу регистрации"""
    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        password_another = request.POST['passwordAnother']

        if password != password_another:
            return render(request, "registration.html", {
                "error": "Пароли не совпадают",
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
            })

        same_users = CustomUser.objects.filter(email=email)
        if same_users.exists():
            return render(request, "registration.html", {
                "error": "Пользователь с такой почтой уже существует",
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            })

        user = CustomUser.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),
            is_active=True
        )

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login_method(request, user)
            return redirect('account')

    return render(request, "registration.html")

def login(request):
    """Функция возвращает страницу авторизации"""
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login_method(request, user)
            return redirect('account')

        return render(request, "login.html", {
            "error": "Пользователь с такими данными не найден"
        })

    return render(request, "login.html")

def reset_password(request):
    """Функция возвращает страницу восстановления пароля"""
    return render(request, "reset_password.html")
