"""Содержит endpoints проекта"""
from django.http import HttpResponseNotFound
from django.shortcuts import render

def index(request):
    """Отображение view главной страницы"""
    return render(request, "index")

def qr_generator(request):
    """Отображение страницы QR-генератора"""
    return render(request, "qr_generator")

def history(request):
    """Отображение страницы Мои ссылки и QR-коды"""
    return render(request, "history")

def price(request):
    """Отображение страницы Тарифы"""
    return HttpResponseNotFound()

def account(request):
    """Отображение страницы аккаунта пользователя"""
    return render(request, "account")

def privacy(request):
    """Отображение страницы правил сервиса"""
    return render(request, "privacy")
