"""Класс содержит методы модуля авторизации"""
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
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
            return render(request, "auth/registration.html", {
                "error": "Пароли не совпадают",
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
            })

        same_users = CustomUser.objects.filter(email=email)
        if same_users.exists():
            return render(request, "auth/registration.html", {
                "error": "Пользователь с такой почтой уже существует",
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            })

        user = CustomUser.objects.create(
            username=email,  # Используем email в качестве username
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),  # Хэшируем пароль перед сохранением
            is_active=True
        )

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login_method(request, user)
            return redirect('account')

    return render(request, "auth/registration.html")

def login(request):
    """Функция возвращает страницу авторизации"""
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)  # Используем email как username
        if user is not None:
            login_method(request, user)
            return redirect('account')
        else:
            return render(request, "auth/login.html", {"error": "Пользователь с такими данными не найден"})

    return render(request, "auth/login.html")

def reset_password(request):
    """Функция возвращает страницу восстановления пароля"""
    return render(request, "auth/reset_password.html")

def account_update_password(request):
    """Обновляет пароль пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        current_password = request.POST['current_password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not user.check_password(current_password):
            return render(request, "auth/account_password.html", {
                'user': user, 'answer': 'Указан неверный текущий пароль'
            })

        if password1 != password2:
            return render(request, "auth/account_password.html", {
                'user': user, 'answer': 'Пароли не совпадают'
            })

        user.password = make_password(password1)
        user.save()

        return render(request, "auth/account_password.html", {
            'user': user, 'answer': 'Пароль успешно изменен', 'is_success': True
        })

    return HttpResponseNotFound()
