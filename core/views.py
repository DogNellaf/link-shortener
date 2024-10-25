"""Содержит endpoints проекта"""
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from core.models import ShortedUrl

def index(request):
    """Отображение view главной страницы"""
    return render(request, "index")

def qr_generator(request):
    """Отображение страницы QR-генератора"""
    return render(request, "qr_generator")

def history(request):
    """Отображение страницы Мои ссылки и QR-коды"""
    user = request.user

    if not user.is_authenticated:
        urls = []
    else:
        urls = ShortedUrl.objects.filter(author__id = user.id)

    return render(request, "history", {'urls': urls})

def price(request):
    """Отображение страницы Тарифы"""
    return HttpResponseNotFound()

def account(request):
    """Отображение страницы аккаунта пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    return render(request, "account", {'user': user})

def privacy(request):
    """Отображение страницы правил сервиса"""
    return render(request, "privacy")
