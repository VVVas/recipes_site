"""Настройка отображения моделей приложения Рецепты в админке."""
from django.contrib import admin

from .models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    """Отображение ингредиента в админке."""

    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
