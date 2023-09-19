"""Модели приложения Рецепты."""
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


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

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']


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
            )
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
            )
        ],
    )

    def __str__(self):
        """Строковое представление модели тега."""
        return self.name

    class Meta:
        """Метаданные модели тега."""

        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']


class IngredientAmount(models.Model):
    """Модель количества ингредиента."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientamount',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Минимум 1'),
        ],
    )

    def __str__(self):
        """Строковое представление модели количества ингредиента."""
        return (f'{self.ingredient.name}, '
                f'{self.amount} {self.ingredient.measurement_unit}')

    class Meta:
        """Метаданные модели количества ингредиента."""

        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количества ингредиентов'
        ordering = ['ingredient']


class Recipe(models.Model):
    """Модель рецепта."""

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        IngredientAmount,
        related_name='recipe',
        verbose_name='Ингредиенты'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(1, 'Минимальное время 1 минута'),
        ],
    )

    # image =
    # is_favorited =
    # is_in_shopping_cart =

    def __str__(self):
        """Строковое представление модели Рецепта."""
        return f'{self.name}, {self.author}'

    class Meta:
        """Метаданные модели Рецепта."""

        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']
