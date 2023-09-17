"""Модели приложения Пользователи."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    class Meta:

        ordering = ['username', 'id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
