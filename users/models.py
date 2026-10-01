from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с авторизацией по email."""

    email = models.EmailField(
        verbose_name="Электронная почта",
        unique=True,
        help_text="Используется для входа в систему",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите изображение профиля",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        blank=True,
        help_text="Контактный номер телефона",
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
        blank=True,
        help_text="Страна проживания",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email
