"""Вьюсеты приложения API."""
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Ingredient, Tag, Recipe
from .serializers import IngredientSerialiser, TagSerialiser, RecipeSerialiser


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет ингредиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialiser
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет тега."""

    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Вьюсет рецепта."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerialiser
