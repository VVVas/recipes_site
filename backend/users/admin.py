"""Настройка отображения моделей приложения Пользователи в админке."""
from django.contrib import admin

from . import models


class CustomUserAdmin(admin.ModelAdmin):
    """Отображение пользователей в админке."""

    list_display = ('pk', 'email', 'username', 'first_name', 'last_name',)
    list_filter = ('email', 'username',)
    search_fields = ('email', 'username',)
    empty_value_display = '-пусто-'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author',)
    list_filter = ('user', 'author',)
    search_fields = ('user', 'author',)
    empty_value_display = '-пусто-'


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Subscription, SubscriptionAdmin)
