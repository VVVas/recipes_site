"""Сериалайзеры приложения API."""
from rest_framework import serializers

from recipes.models import Ingredient, Tag, Recipe


class IngredientSerialiser(serializers.ModelSerializer):
    """Сериалайзер ингредиента."""

    class Meta:
        """Метаданные сериалайзера ингредиента."""

        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )


class TagSerialiser(serializers.ModelSerializer):
    """Сериалайзер тега."""

    class Meta:
        """Метаданные сериалайзера тега."""

        model = Tag
        fields = (
            'id', 'name', 'slug',
        )


class RecipeSerialiser(serializers.ModelSerializer):
    """Сериалайзер тега."""

    class Meta:
        """Метаданные сериалайзера тега."""

        model = Recipe
        fields = (
            'id', 'tags', 'author', 'name', 'text', 'cooking_time',
        )
