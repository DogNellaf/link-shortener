"""Содержит описание моделей кастомной авторизации"""
from django.contrib.auth.models import AbstractUser
from django.utils import timezone as tz
from django.db import models
from linkshortener.settings import RESET_PASSWORD_CODE_LIFETIME

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

class PasswordResetCode(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        verbose_name="Кому принадлежит",
        on_delete=models.CASCADE
    )

    code = models.CharField(
        verbose_name="Код восстановления пароля",
        max_length=4
    )

    created_at = models.DateTimeField(
        verbose_name="Создан в",
        auto_now_add=True
    )

    def is_expired(self) -> bool:
        """Возвращает результат проверки истек ли код"""
        return tz.now() > self.created_at + tz.timedelta(minutes=RESET_PASSWORD_CODE_LIFETIME)
