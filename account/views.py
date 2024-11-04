"""Содержит основные методы взаимодействия с аккаунтом"""
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.conf import settings

from core.models import CustomUser

def account(request):
    """Отображение страницы аккаунта пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    return render(request, "account.html", {'user': user})

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
            return render(request, "account_password.html", {
                'user': user,
                'answer': 'Указан неверный текущий пароль'
            })

        if password1 != password2:
            return render(request, "account_password.html", {
                'user': user,
                'answer': 'Пароли не совпадают'
            })

        user.password = make_password(password1)
        user.save()

        return render(request, "account_password.html", {
            'user': user,
            'answer': 'Пароль успешно изменен',
            'is_success': True
        })

    return HttpResponseNotFound()

def account_update_data(request):
    """Обновляет данные пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        email = request.POST['email']

        same_users = CustomUser.objects.filter(email=email)
        if same_users.exists():
            same_user = same_users.first()
            if same_user.pk != user.pk:
                return render(request, "auth/account.html", {
                    'user': user,
                    'answer': 'Email уже занят'
                })

        user.email = email

        user.save()
        return redirect(account)

    return HttpResponseNotFound()

def avatar_remove(request):
    """Удаляет аватар пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        user.avatar = None
        user.save()
        return redirect(account)

    return HttpResponseNotFound()

def avatar_update(request):
    """Загружает аватар пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        avatar = request.FILES['avatar']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(avatar.name, avatar)
        user.avatar = fs.url(filename)
        user.save()
        return redirect(account)

    return HttpResponseNotFound()

def account_price(request):
    """Отображение страницы тарифа аккаунта пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    return render(request, "account_price.html", {'user': user})

def account_password(request):
    """Отображение страницы пароля аккаунта пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    return render(request, "account_password.html", {'user': user})
