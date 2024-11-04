"""Содержит endpoints проекта"""

from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from qr_code.qrcode.maker import make_embedded_qr_code

from core.models import ShortedUrl
from core.utils import create_shorted_url

QR_CODE_OPTIONS = settings.QR_CODE_OPTIONS
MONTHS = settings.MONTHS

def index(request):
    """Стартовая страница, переадресующая пользователя с пустого пути / на линкер"""
    return redirect("linker")

def linker(request, url=""):
    """Отображение view главной страницы линкера"""

    original_url = ""
    is_favorite = False
    url_title = ""

    if url != "":
        shorted_urls = ShortedUrl.objects.filter(short_url = url)
        if not shorted_urls.exists():
            return HttpResponseNotFound()

        shorted_url = shorted_urls.first()
        original_url = shorted_url.original_url
        is_favorite = shorted_url.is_favorite
        url_title = shorted_url.title

    return render(request, "index.html", {
        'url': url,
        'original_url': original_url,
        'is_favorite': is_favorite,
        'url_title': url_title
    })

def generate_url(request):
    """Генерирует ссылку для текущего пользователя или анонимно"""
    if request.method == "POST":
        url = request.POST['url']
        shorted_url = create_shorted_url(
            user=request.user,
            original_url=url
        )

        return redirect(linker, url=shorted_url.short_url)

    return HttpResponseNotFound()

def qr_generator(request, url = ""):
    """Отображение страницы QR-генератора"""

    original_url = ""
    is_favorite = False
    url_title = ""
    qr = None

    if url != "":
        shorted_urls = ShortedUrl.objects.filter(short_url = url, is_only_qr=True)
        if not shorted_urls.exists():
            return HttpResponseNotFound()

        shorted_url = shorted_urls.first()
        original_url = shorted_url.original_url
        is_favorite = shorted_url.is_favorite
        url_title = shorted_url.title

        qr = make_embedded_qr_code(
            data=f"http://{request.get_host()}/{url}",
            qr_code_options=QR_CODE_OPTIONS
        )

    return render(request, "qr_generator.html", {
        'host': request.get_host(),
        'qr': qr,
        'url': url,
        'original_url': original_url,
        'is_favorite': is_favorite,
        'url_title': url_title,
    })

def generate_qr(request):
    """Создает QR код по ссылке"""
    if request.method == "POST":
        url = request.POST['url']
        shorted_url = create_shorted_url(
            user=request.user,
            original_url=url
        )

        shorted_url.is_only_qr = True
        shorted_url.save()

        return redirect(qr_generator, url=shorted_url.short_url)

    return HttpResponseNotFound()

def update_url_title(request):
    """Метод обновляет название ссылки"""
    user = request.user

    if request.method == "POST" and user.is_authenticated:
        title = request.POST['title']
        url = request.POST['url']

        urls = ShortedUrl.objects.filter(author = user, short_url = url)
        if urls.exists():
            shorted_url = urls.first()
            shorted_url.title = title
            shorted_url.save()

    return redirect(request.META['HTTP_REFERER'])

def delete_url(request):
    """Метод удаляет ссылку из избранного"""
    user = request.user

    if request.method == "POST" and user.is_authenticated:
        url = request.POST['url']

        urls = ShortedUrl.objects.filter(author = user, short_url = url)
        if urls.exists():
            url = urls.first()
            url.is_favorite = False
            url.save()

    return redirect(request.META['HTTP_REFERER'])

def favorite_urls(request):
    """Отображение страницы Мои ссылки - избранное"""
    user = request.user

    if not user.is_authenticated:
        urls = []
    else:
        urls = ShortedUrl.objects.filter(author = user, is_favorite = True, is_only_qr = False)

    return render(request, "history/favorite_urls.html", {'urls': urls})

def history_urls(request):
    """Отображение страницы Мои ссылки - история"""
    user = request.user

    if not user.is_authenticated:
        urls = []
    else:
        urls = ShortedUrl.objects.filter(author = user, is_only_qr=False)
        urls = urls.order_by('-created_at')[:100]

    urls_by_dates = {}

    for url in urls:
        created_at_date = url.created_at.date()
        month = MONTHS[created_at_date.month]
        day = created_at_date.day
        created_at_date_title = f"{day} {month}"
        dates = urls_by_dates.keys()
        if created_at_date_title in dates:
            urls_by_dates[created_at_date_title].append(url)
        else:
            urls_by_dates[created_at_date_title] = [url]

    return render(request, "history/history_urls.html", {'urls_by_dates': urls_by_dates})

def favorite_qrs(request):
    """Отображение страницы Мои QR-коды - избранное"""
    user = request.user

    if not user.is_authenticated:
        urls = []
    else:
        urls = ShortedUrl.objects.filter(author = user, is_favorite = True, is_only_qr = True)

    urls_qrs = {}
    for url in urls:
        qr = make_embedded_qr_code(
            data=f"http://{request.get_host()}/{url.short_url}",
            qr_code_options=QR_CODE_OPTIONS
        )
        urls_qrs[url] = qr

    return render(request, "history/favorite_qrs.html", {'urls': urls_qrs})

def delete_qr(request):
    """Метод удаляет QR-код из избранного"""
    user = request.user

    if request.method == "POST" and user.is_authenticated:
        url = request.POST['url']

        urls = ShortedUrl.objects.filter(author = user, short_url = url, is_only_qr = True)
        if urls.exists():
            url = urls.first()
            url.is_favorite = False
            url.save()

    return redirect(request.META['HTTP_REFERER'])

def history_qrs(request):
    """Отображение страницы Мои QR-коды - история"""
    user = request.user

    if not user.is_authenticated:
        urls = []
    else:
        urls = ShortedUrl.objects.filter(author = user, is_only_qr=True)
        urls = urls.order_by('-created_at')[:100]

    urls_by_dates = {}

    for url in urls:
        created_at_date = url.created_at.date()
        month = MONTHS[created_at_date.month]
        day = created_at_date.day
        created_at_date_title = f"{day} {month}"
        dates = urls_by_dates.keys()
        if created_at_date_title in dates:
            urls_by_dates[created_at_date_title].append(url)
        else:
            urls_by_dates[created_at_date_title] = [url]

    return render(request, "history/history_qrs.html", {'urls_by_dates': urls_by_dates})

def price(request):
    """Отображение страницы Тарифы"""
    return render(request, "price.html")

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

    if shorted_url.is_only_qr:
        return redirect(qr_generator, url=short_url)
    else:
        return redirect(linker, url=short_url)

def remove_url_favorite(request):
    """Удаляет ссылку из избранного"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        short_url = request.POST['url']

        shorted_urls = ShortedUrl.objects.filter(short_url = short_url)
        if not shorted_urls.exists():
            return redirect(linker, url=short_url)

        shorted_url = shorted_urls.first()
        shorted_url.is_favorite = False
        shorted_url.save()

    if shorted_url.is_only_qr:
        return redirect(qr_generator, url=short_url)

    return redirect(linker, url=short_url)

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

    return redirect(url_redirect_to, request=request)
