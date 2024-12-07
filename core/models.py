"""Содержит описание моделей базы данных"""

from django.db import models
from django.conf import settings
from custom_auth.models import CustomUser

class ShortedUrl(models.Model):
    """Представляет класс сокращенной ссылки"""
    author = models.ForeignKey(
        to = CustomUser,
        verbose_name = "Автор ссылки",
        on_delete = models.SET_NULL,
        null = True
    )

    title = models.CharField(
        verbose_name="Название ссылки",
        default="",
        max_length=50
    )

    original_url = models.URLField(
        verbose_name = 'Оригинальная ссылка',
        max_length = 200
    )

    short_url = models.CharField(
        verbose_name = 'Сокращенная ссылка',
        max_length = settings.SHORT_URL_LENGTH,
        unique = True
    )

    created_at = models.DateTimeField(
        verbose_name = 'Дата создания',
        auto_now_add=True
    )

    is_favorite = models.BooleanField(
        verbose_name = 'Является избранной ссылкой',
        default = False
    )

    is_only_qr = models.BooleanField(
        verbose_name = 'Ссылка создавалась исключительно для QR кода',
        default = False
    )

    def __str__(self):
        """Строковое представление объекта"""
        return f"{self.short_url} - {self.original_url}"

    class Meta:
        """Мета данные сокращенной ссылки"""
        verbose_name = "Сокращенная ссылка"
        verbose_name_plural = "Сокращенные ссылки"


class Qr(models.Model):
    """Представляет класс QR кода - в данный момент не используется"""
    
    short_url = models.ForeignKey(
        to = ShortedUrl,
        verbose_name = "Короткая ссылка, которой соответствует QR",
        on_delete = models.CASCADE,
        null = False
    )

    qr_color = models.CharField(
        verbose_name = "Цвет QR кода",
        max_length = 6,
        default = "101010"
    )

    is_with_background = models.BooleanField(
        verbose_name = "Имеет фон",
        default = False
    )

    background_color = models.CharField(
        verbose_name = "Цвет фона",
        max_length = 6,
        default = "ffffff"
    )

    logo = models.FileField(
        verbose_name = "Логотип",
        default="operator.png"
    )


    def __str__(self):
        """Строковое представление объекта"""
        return f"{self.short_url.title} | {self.qr_color} | {self.background_color} | {self.logo}"

    class Meta:
        """Мета данные QR кода"""
        verbose_name = "QR код"
        verbose_name_plural = "QR коды"
