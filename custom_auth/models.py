"""Содержит описание моделей кастомной авторизации"""
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Описывает кастомного пользователя"""
    avatar = models.ImageField(
        verbose_name="Аватар пользователя",
        upload_to='avatars/',
        null=True,
        blank=True
    )

    class Meta:
        """Мета данные кастомного пользователя"""
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
