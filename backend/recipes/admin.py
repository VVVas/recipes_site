"""Настройка отображения моделей приложения Рецепты в админке."""
from django.contrib import admin

from . import models


class TagAdmin(admin.ModelAdmin):
    """Отображение тега в админке."""

    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    """Отображение ингредиента в админке."""

    list_display = ('pk', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    """Отображение тега в админке."""

    list_display = ('pk', 'name', 'text', 'cooking_time', 'author',)
    readonly_fields = ('in_favorite',)
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name', 'author', 'text', 'tags',)
    empty_value_display = '-пусто-'

    @admin.display(description='В избранном')
    def in_favorite(self, recipe):
        return recipe.favoriterecipe.count()


class IngredientAmountAdmin(admin.ModelAdmin):
    """Отображение количества ингредиента в админке."""

    list_display = ('pk', 'recipe', 'ingredient', 'amount',)
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'


class FavoriteShoppingCartRecipeAdmin(admin.ModelAdmin):
    """Отображение избранных рецептов и рецептов в списке покупок."""

    list_display = ('pk', 'user', 'recipe',)
    search_fields = ('recipe',)
    empty_value_display = '-пусто-'


admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.IngredientAmount, IngredientAmountAdmin)
admin.site.register(models.FavoriteRecipe, FavoriteShoppingCartRecipeAdmin)
admin.site.register(models.ShoppingCartRecipe, FavoriteShoppingCartRecipeAdmin)
