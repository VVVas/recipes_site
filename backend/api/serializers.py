"""Сериалайзеры приложения API."""
from rest_framework import serializers

from recipes.models import Ingredient


class IngredientSerialiser(serializers.ModelSerializer):
    """Сериалайзер ингредиента."""

    class Meta:
        """Метаданные сериалайзера ингредиента."""

        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )
