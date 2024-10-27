"""Содержит endpoints проекта"""
import random
import string

from django.http import HttpResponseNotFound
from django.urls import reverse
from django.shortcuts import render, redirect
from core.models import ShortedUrl
from linkshortener.settings import SHORT_URL_LENGTH

def index(request):
    """Отображение view главной страницы"""
    return render(request, "index.html", {'url': ""})

def generate_url(request):
    """Генерирует ссылку для текущего пользователя или анонимно"""
    if request.method == "POST":
        url = request.POST['url']
        is_exists = True

        while is_exists:
            short_url = ""
            for _ in range(SHORT_URL_LENGTH):
                short_url += random.choice(string.ascii_letters)

            is_exists = ShortedUrl.objects.filter(short_url=short_url).exists()

        user = request.user

        shorted_url = ShortedUrl(
            author = user if user.is_authenticated else None,
            original_url = url,
            short_url = short_url
        )

        shorted_url.save()

        short_url = f"{request.get_host()}/{short_url}" 

        return render(request, "index.html", {'url': short_url})

    url = request.GET['url']
    return redirect(reverse(url))

def qr_generator(request):
    """Отображение страницы QR-генератора"""
    return render(request, "qr_generator.html")

def history(request):
    """Отображение страницы Мои ссылки и QR-коды"""
    user = request.user

    if not user.is_authenticated:
        urls = []
    else:
        urls = ShortedUrl.objects.filter(author__id = user.id)

    return render(request, "history.html", {'urls': urls})

def price(request):
    """Отображение страницы Тарифы"""
    return HttpResponseNotFound()

def account(request):
    """Отображение страницы аккаунта пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    return render(request, "account.html", {'user': user})

def privacy(request):
    """Отображение страницы правил сервиса"""
    return render(request, "privacy.html")

def redirect_to_url(request, url = ""):
    """Базовая функция переадресует пользователя на созданную заранее ссылку"""
    if url == "":
        return HttpResponseNotFound()

    shorted_urls = ShortedUrl.objects.filter(short_url = url)
    if not shorted_urls.exists():
        return HttpResponseNotFound()

    url_redirect_to = shorted_urls.first().original_url
    return redirect(url_redirect_to)
