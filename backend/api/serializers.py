"""Сериалайзеры приложения API."""
from base64 import b64decode

from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag

User = get_user_model()

#
# Вспомогательные сериалайзеры.
#


class Base64ImageField(serializers.ImageField):
    """Поле изображения, которое пребразует base64-картинку в файл."""

    def to_internal_value(self, data):
        """Преобразование входных данных."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(b64decode(imgstr), name='temp.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)

#
# Пользователь — основной сериалайзер.
#


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """Статус подписки на пользователя."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.subscriber.filter(author=obj).exists()

    class Meta:
        """Метаданные пользователя."""

        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

#
# Рецепт — вспомогательные сериалайзеры.
#


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер тега."""

    class Meta:
        """Метаданные тега."""

        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер ингредиента."""

    class Meta:
        """Метаданные ингредиента."""

        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )


class RecipeSimpleSerializer(serializers.ModelSerializer):
    """Упрощённый сериалайзер рецепта при просмотре."""

    class Meta:
        """Метаданные упрощённого рецепта при просмотре."""

        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time',
        )

#
# Рецепт — сериалайзеры просмотра.
#


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериалайзер количества ингредиента в рецепте при просмотре."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        """Метаданные количества ингредиента в рецепте при просмотре."""

        model = IngredientAmount
        fields = (
            'id', 'name', 'measurement_unit', 'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер рецепта при просмотре."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True, read_only=True,
        source='ingredientamount'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        """Статус наличие рецепта в избранном пользователя."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favoriterecipe.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Статус наличие рецепта в списке покупок пользователя."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shoppingcartrecipe.filter(recipe=obj).exists()

    class Meta:
        """Метаданные рецепта при просмотре."""

        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        )

#
# Рецепт — сериалайзеры создания и редактирования.
#


class IngredientAmountCUSerializer(serializers.ModelSerializer):
    """Сериалайзер количества ингредиента в рецепте при редактировании."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        """Метаданные количества ингредиента в рецепте при редактировании."""

        model = IngredientAmount
        fields = (
            'id', 'amount',
        )


class RecipeCUSerializer(serializers.ModelSerializer):
    """Сериалайзер рецепта при редактировании."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        allow_empty=False,
    )
    ingredients = IngredientAmountCUSerializer(
        many=True,
        source='ingredientamount',
        allow_empty=False,
    )
    image = Base64ImageField()

    class Meta:
        """Метаданные рецепта при редактировании."""

        model = Recipe
        fields = (
            'tags', 'ingredients', 'image', 'name', 'text', 'cooking_time',
        )

    def validate_tags(self, tags):
        """Проверка поля тегов."""
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError('Не дублируйте теги')
        return tags

    def validate_ingredients(self, ingredients):
        """Проверка поля ингредиентов."""
        ingredients_ids = [item['id'] for item in ingredients]
        if len(ingredients_ids) != len(set(ingredients_ids)):
            raise serializers.ValidationError('Не дублируйте ингредиенты')
        return ingredients

    def validate(self, data):
        """Проверка полей."""
        if not data.get('tags'):
            raise serializers.ValidationError({'tags': 'Обязательное поле'})
        if not data.get('ingredientamount'):
            raise serializers.ValidationError(
                {'ingredients': 'Обязательное поле'}
            )
        return data

    def _create_ingredientamount(self, ingredients, recipe):
        """Создание количества ингредиентов в рецепте."""
        ingredientamounts = []
        for ingredientamount in ingredients:
            ingredient = ingredientamount.get('id')
            amount = ingredientamount.get('amount')
            ingredientamounts.append(
                IngredientAmount(
                    ingredient=ingredient,
                    recipe=recipe,
                    amount=amount
                )
            )
        IngredientAmount.objects.bulk_create(ingredientamounts)

    @transaction.atomic
    def create(self, validated_data):
        """Переопределение создания рецепта."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientamount')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self._create_ingredientamount(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        """Переопределение обновления рецепта."""
        tags = validated_data.get('tags', recipe.tags)
        recipe.tags.set(tags, clear=True)

        ingredients = validated_data.get(
            'ingredientamount', recipe.ingredients)
        IngredientAmount.objects.filter(recipe=recipe).delete()
        self._create_ingredientamount(ingredients, recipe)

        recipe.image = validated_data.get(
            'image', recipe.image)
        recipe.name = validated_data.get(
            'name', recipe.name)
        recipe.text = validated_data.get(
            'text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)

        return recipe

    def to_representation(self, recipe):
        """Преобразование выходных данных."""
        return RecipeSerializer(recipe, context=self.context).data

#
# Подписки — основной сериалайзер просмотра.
#


class SubscriptionSerializer(UserSerializer):
    """Сериалайзер для вывода подписки."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        """Метаданные пользователя."""

        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )

    def get_recipes(self, author):
        """Получение рецептов автора."""
        request = self.context.get('request')
        if request.GET.get('recipes_limit'):
            recipes_limit = int(request.GET.get('recipes_limit'))
            queryset = author.recipe.all()[:recipes_limit]
        else:
            queryset = author.recipe.all()
        serializer = RecipeSimpleSerializer(
            queryset, read_only=True, many=True, context=self.context
        )
        return serializer.data

    def get_recipes_count(self, author):
        """Вычисление количества рецептов автора."""
        return author.recipe.count()
