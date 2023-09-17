"""Настройка отображения моделей приложения Рецепты в админке."""
from django.contrib import admin

from .models import Ingredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    """Отображение ингредиента в админке."""

    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    """Отображение тега в админке."""

    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
