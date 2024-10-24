"""Содержит описание моделей базы данных"""

from django.contrib.auth.models import User
from django.db import models

class ShortedUrl(models.Model):
    """Представляет класс сокращенной ссылки"""
    author = models.ForeignKey(
        to = User,
        related_name = "Автор ссылки",
        on_delete = models.SET_NULL
    )

    original_url = models.URLField(
        related_name = 'Оригинальная ссылка',
        max_length = 200
    )

    short_url = models.CharField(
        related_name = 'Сокращенная ссылка',
        max_length = 15,
        unique = True
    )

    created_at = models.DateTimeField(
        related_name = 'Дата создания',
        auto_now_add=True
    )

    is_favorite = models.BooleanField(
        related_name = 'Является избранной ссылкой',
        default = False
    )

    def __str__(self):
        """Строковое представление объекта"""
        return f"{self.short_url} - {self.original_url}"
    
    class Meta:
        verbose_name = "Сокращенная ссылка"
        verbose_name_prural = "Сокращенные ссылки"
