"""Модели приложения Рецепты."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        blank=True,
        verbose_name='Цвет',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введите код цвета в шестнадцатеричной системе.'
            ),
        ],
    )
    slug = models.SlugField(
        max_length=200,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Слаг',
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message='Только латинские буквы, цифры, подчёркивание и дефис.'
            ),
        ],
    )

    def __str__(self):
        """Строковое представление модели тега."""
        return self.name

    class Meta:
        """Метаданные модели тега."""

        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        """Строковое представление модели ингредиента."""
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        """Метаданные модели ингредиента."""

        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='%(app_label)s_%(class)s_name_measurement_pair_unique'
            )
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']


class Recipe(models.Model):
    """Модель рецепта."""

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipe',
        verbose_name='Ингредиенты',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=settings.RECIPES_UPLOAD_TO,
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(1, 'Минимальное время 1 минута'),
            MaxValueValidator(900, 'Максимальное время 900 минут'),
        ],
    )

    def __str__(self):
        """Строковое представление модели рецепта."""
        return f'{self.name} от {self.author}'

    class Meta:
        """Метаданные модели Рецепта."""

        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']


class IngredientAmount(models.Model):
    """Модель количества ингредиента в рецепте."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientamount',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientamount',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Минимум 1'),
            MaxValueValidator(2500, 'Максимум 2500'),
        ],
    )

    def __str__(self):
        """Строковое представление модели количества ингредиента в рецепте."""
        return (f'{self.ingredient.name}, '
                f'{self.amount} {self.ingredient.measurement_unit}, '
                f'в {self.recipe.name}')

    class Meta:
        """Метаданные модели количества ингредиента в рецепте."""

        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='%(app_label)s_%(class)s_ingredient_recipe_pair_unique'
            )
        ]
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количества ингредиентов в рецепте'
        ordering = ['ingredient']


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favoriterecipe',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favoriterecipe',
        verbose_name='Рецепт'
    )

    def __str__(self):
        """Строковое представление модели избранных рецептов пользователя."""
        return f'{self.user}, {self.recipe}'

    class Meta:
        """Метаданные модели избранных рецептов пользователя."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='%(app_label)s_%(class)s_user_recipe_pair_unique'
            )
        ]
        verbose_name = 'Избранные рецепты пользователя'
        verbose_name_plural = 'Избранные рецепты пользователей'
        ordering = ['user']


class ShoppingCartRecipe(models.Model):
    """Модель списка покупок пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcartrecipe',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcartrecipe',
        verbose_name='Рецепт'
    )

    def __str__(self):
        """Строковое представление модели списка покупок пользователя."""
        return f'{self.user}, {self.recipe}'

    class Meta:
        """Метаданные модели списка покупок пользователя."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='%(app_label)s_%(class)s_user_recipe_pair_unique'
            )
        ]
        verbose_name = 'Список покупок пользователя'
        verbose_name_plural = 'Списки покупок пользователей'
        ordering = ['user']
