"""Вьюсеты приложения API."""
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Ingredient, Tag, Recipe
from .serializers import IngredientSerialiser, TagSerialiser, RecipeSerialiser


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет ингредиента."""

    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerialiser


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет тега."""

    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerialiser


class RecipeViewSet(ModelViewSet):
    """Вьюсет рецепта."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerialiser
