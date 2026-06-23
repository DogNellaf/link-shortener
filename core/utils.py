"""Модуль содержит вспомогательные методы"""

import random
import string

from django.conf import settings
from custom_auth.models import CustomUser
from core.models import ShortedUrl


URL_CHARSET = string.ascii_letters + string.digits
SHORT_URL_LENGTH = settings.SHORT_URL_LENGTH

def generate_short_url() -> str:
    """Генерирует сокращенную ссылку по представленному оригиналу"""
    is_exists = True
    short_url = ""

    while is_exists:
        short_url = ""
        for _ in range(SHORT_URL_LENGTH):
            short_url += random.choice(URL_CHARSET)

        is_exists = ShortedUrl.objects.filter(short_url=short_url).exists()

    return short_url

def create_shorted_url(user: CustomUser, original_url: str) -> ShortedUrl:
    """Создает от лица CustomUser ShortedUrl объект по оригинальной ссылке"""
    short_url = generate_short_url()

    shorted_url = ShortedUrl(
        author = user if user.is_authenticated else None,
        original_url = original_url,
        short_url = short_url
    )

    shorted_url.save()

    return shorted_url
