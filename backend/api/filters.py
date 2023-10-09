"""Фильтры приложения API."""
from django.contrib.auth import get_user_model
from django_filters import (CharFilter, ChoiceFilter, FilterSet,
                            ModelChoiceFilter, ModelMultipleChoiceFilter)

from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class IngredientFilter(FilterSet):
    """Фильтр ингредиента."""

    name = CharFilter(lookup_expr='istartswith')

    class Meta:
        """Метаданные фильтра ингредиента."""

        model = Ingredient
        fields = (
            'name',
        )


class RecipeFilter(FilterSet):
    """Фильтр рецепта."""

    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = ChoiceFilter(
        label='Избранные рецепты',
        choices=(('0', '0'), ('1', '1')),
        method='is_favorited_filter'
    )
    is_in_shopping_cart = ChoiceFilter(
        label='Рецепты в списке покупок',
        choices=(('0', '0'), ('1', '1')),
        method='is_in_shopping_cart_filter'
    )

    class Meta:
        """Метаданные фильтра рецепта."""

        model = Recipe
        fields = (
            'author', 'tags',
        )

    def is_favorited_filter(self, queryset, name, value):
        """Фильтрует избранные рецепты для пользователя."""
        user = self.request.user
        if value == '1' and not user.is_anonymous:
            return queryset.filter(favoriterecipe__user=user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        """Фильтрует рецепты в списке покупок для пользователя."""
        user = self.request.user
        if value == '1' and not user.is_anonymous:
            return queryset.filter(shoppingcartrecipe__user=user)
        return queryset
