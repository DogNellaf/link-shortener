"""Класс содержит методы модуля авторизации"""
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login as login_method, get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404
from custom_auth.models import CustomUser, PasswordResetCode

import json

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

    return render(request, "auth/registration.html")

def login(request):
    """Функция возвращает страницу авторизации"""
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login_method(request, user)
            return redirect('account')

        return render(request, "auth/login.html", {
            "error": "Пользователь с такими данными не найден"
        })

    return render(request, "auth/login.html")

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email is None:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')

        try:
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            return render(request, 'auth/password_reset.html', {'error': "Пользователь не существует", "email": email})

        code = get_random_string(length=4, allowed_chars='0123456789')

        PasswordResetCode.objects.filter(user=user).delete()
        PasswordResetCode.objects.create(user=user, code=code)

        send_mail(
            'Восстановление пароля',
            f'Ваш код для восстановления пароля: {code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return render(request, 'auth/password_reset_verify.html', {'email': email})

    return render(request, 'auth/password_reset.html')

def password_reset_verify(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        try:
            reset_code = PasswordResetCode.objects.get(code=code)

        except PasswordResetCode.DoesNotExist:
            return HttpResponse("Неверный код.", status=400)

        if reset_code.is_expired():
            return HttpResponse("Код истек.", status=400)

        return redirect('auth/password_reset_confirm.html', user_id=reset_code.user.id)

    return render(request, 'auth/password_reset_verify.html')

def password_reset_confirm(request, code: str):
    """Обрабатывает POST запрос применения нового пароля"""
    if request.method == 'POST':
        code = get_object_or_404(PasswordResetCode, code=code)
        password = get_random_string(length=18)
        code.user.set_password(password)
        code.user.save()

        send_mail(
            'Восстановление пароля',
            f'Ваш новый пароль: {password}',
            settings.DEFAULT_FROM_EMAIL,
            [code.user.email],
            fail_silently=False,
        )

        code.delete()

        return HttpResponse("Пароль успешно изменен", status=200)

    return Http404()
