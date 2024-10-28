"""Содержит endpoints проекта"""
import random
import string

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from urllib.parse import urlparse
from core.models import ShortedUrl
from linkshortener import settings
from linkshortener.settings import SHORT_URL_LENGTH

def index(request):
    """Стартовая страница, переадресующая пользователя с пустого пути / на линкер"""
    return redirect("linker")

def linker(request, url=""):
    """Отображение view главной страницы линкера"""

    original_url = ""

    if url != "":
        shorted_urls = ShortedUrl.objects.filter(short_url = url)
        if not shorted_urls.exists():
            return HttpResponseNotFound()

        shorted_url = shorted_urls.first()

        original_url = shorted_url.original_url

    return render(request, "index.html", {
        'host': request.get_host(),
        'url': url,
        'original_url': original_url,
        'is_favorite': shorted_url.is_favorite
    })

def generate_url(request):
    """Генерирует ссылку для текущего пользователя или анонимно"""
    if request.method == "POST":
        url = request.POST['url']
        is_exists = True

        url_charset = string.ascii_letters + string.digits

        while is_exists:
            short_url = ""
            for _ in range(SHORT_URL_LENGTH):
                short_url += random.choice(url_charset)

            is_exists = ShortedUrl.objects.filter(short_url=short_url).exists()

        user = request.user

        shorted_url = ShortedUrl(
            author = user if user.is_authenticated else None,
            original_url = url,
            short_url = short_url
        )

        shorted_url.save()

        return redirect(linker, url=short_url)

    return HttpResponseNotFound()

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
    return render(request, "price.html")

def account(request):
    """Отображение страницы аккаунта пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    return render(request, "auth/account.html", {'user': user})

def make_url_favorite(request):
    """Делает ссылку избранной"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        short_url = request.POST['url']
        title = request.POST['title']

        shorted_urls = ShortedUrl.objects.filter(short_url = short_url)
        if not shorted_urls.exists():
            return redirect(linker, url=short_url)

        shorted_url = shorted_urls.first()
        shorted_url.title = title
        shorted_url.is_favorite = True
        shorted_url.save()

    return redirect(linker, url=short_url)

def account_update_data(request):
    """Обновляет данные пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        email = request.POST['email']

        same_users = User.objects.filter(email=email)
        if same_users.exists():
            same_user = same_users.first()
            if same_user.pk != user.pk:
                return render(request, "auth/account.html", {
                    'user': user, 'answer': 'Email уже занят'
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

    return render(request, "auth/account_price.html", {'user': user})

def account_password(request):
    """Отображение страницы пароля аккаунта пользователя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    return render(request, "auth/account_password.html", {'user': user})

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

    parsed_url = urlparse(url_redirect_to)
    if not parsed_url.scheme:
        url_redirect_to = "http://" + url_redirect_to

    return redirect(url_redirect_to)
