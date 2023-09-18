"""Сериалайзеры приложения API."""
from rest_framework import serializers

from recipes.models import Ingredient, Tag, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер ингредиента."""

    class Meta:
        """Метаданные сериалайзера ингредиента."""

        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер тега."""

    class Meta:
        """Метаданные сериалайзера тега."""

        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер тега."""

    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        """Метаданные сериалайзера тега."""

        model = Recipe
        fields = (
            'id', 'tags', 'author', 'name', 'text', 'cooking_time',
        )
