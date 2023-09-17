"""Вьюсеты приложения API."""
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Ingredient
from api.serializers import IngredientSerialiser


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет ингредиента."""

    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerialiser
