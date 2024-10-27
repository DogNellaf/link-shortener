"""Содержит описание моделей базы данных"""

from django.contrib.auth.models import User
from django.db import models
from linkshortener.settings import SHORT_URL_LENGTH

class ShortedUrl(models.Model):
    """Представляет класс сокращенной ссылки"""
    author = models.ForeignKey(
        to = User,
        verbose_name = "Автор ссылки",
        on_delete = models.SET_NULL,
        null = True
    )

    original_url = models.URLField(
        verbose_name = 'Оригинальная ссылка',
        max_length = 200
    )

    short_url = models.CharField(
        verbose_name = 'Сокращенная ссылка',
        max_length = SHORT_URL_LENGTH,
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

    def __str__(self):
        """Строковое представление объекта"""
        return f"{self.short_url} - {self.original_url}"
    
    class Meta:
        verbose_name = "Сокращенная ссылка"
        verbose_name_plural = "Сокращенные ссылки"
