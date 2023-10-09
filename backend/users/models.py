"""Модели приложения Пользователи."""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(
        unique=True,
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Только латинские буквы, цифры, подчёркивание и дефис.'
            ),
        ],
    )

    first_name = models.CharField(
        max_length=150,
        blank=False,
    )

    last_name = models.CharField(
        max_length=150,
        blank=False,
    )

    def __str__(self):
        """Строковое представление модели пользователя."""
        return self.email

    class Meta:
        """Метаданные модели пользователя."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']


User = get_user_model()


class Subscription(models.Model):
    """Модель подписки на пользователей."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
    )

    def __str__(self):
        """Строковое представление модели подписки на пользователей."""
        return f'{self.user} подписан на {self.author}'

    class Meta:
        """Метаданные модели подписки на пользователей."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='%(app_label)s_%(class)s_user_author_pair_unique'
            )
        ]
        verbose_name = 'Подписка на пользователей'
        verbose_name_plural = 'Подписки на пользователей'
        ordering = ['user']
