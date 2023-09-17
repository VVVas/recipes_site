"""Вьюсеты приложения API."""
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Ingredient, Tag
from .serializers import IngredientSerialiser, TagSerialiser


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
