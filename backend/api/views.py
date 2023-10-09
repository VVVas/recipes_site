"""Вьюсеты приложения API."""
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from recipes.models import (FavoriteRecipe, Ingredient, IngredientAmount,
                            Recipe, ShoppingCartRecipe, Tag)
from users.models import Subscription
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCUSerializer,
                          RecipeSerializer, RecipeSimpleSerializer,
                          SubscriptionSerializer, TagSerializer)

User = get_user_model()

#
# Вьюсеты по работе с пользователем.
#


class CustomUserViewSet(UserViewSet):
    """
    Вьюсет пользователя.

    Унаследован от djoser.views.UserViewSet
    """

    queryset = User.objects.all()

    @action(
        methods=['get',],
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=[IsAuthenticated,]
    )
    def me(self, request, *args, **kwargs):
        """Переопределение для ограничения доступа гостей."""
        return super().me(request, *args, **kwargs)

    @action(
        methods=['post', 'delete',],
        detail=True,
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=[IsAuthenticated,]
    )
    def get_subscribe(self, request, id):
        """Подписка на пользователей."""
        author = get_object_or_404(User, id=id)
        user = request.user

        if user == author:
            return Response(
                {'error': 'Нельзя подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            _, created = Subscription.objects.get_or_create(
                user=user, author=author
            )
            if not created:
                return Response(
                    {'error': 'Запись уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = SubscriptionSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not user.subscriber.filter(author=author).exists():
            return Response(
                {'error': 'Запись уже была удалена.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.subscriber.filter(author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(ListModelMixin, GenericViewSet):
    """Вьюсет списка подписки на авторов."""

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        """Собираем список подписки на авторов."""
        return get_list_or_404(User, author__user=self.request.user)

#
# Вьюсеты по работе с рецептом.
#


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет тега."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет ингредиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Вьюсет рецепта."""

    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        """Выбор сериалайзера для рецепта."""
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCUSerializer

    def perform_create(self, serializer):
        """При создании дополняем данные информацией об авторе."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """При обновлении сохраняем."""
        serializer.save()

    @action(
        methods=['post', 'delete',],
        detail=True,
        url_path='favorite',
        url_name='favorite',
        permission_classes=[IsAuthenticated,]
    )
    def get_favorite(self, request, pk):
        """Добавление рецептов в избранное."""
        if not Recipe.objects.filter(id=pk).exists():
            if request.method == 'POST':
                return Response(
                    {'error': 'Рецепт не найден.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': 'Рецепт не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'POST':
            _, created = FavoriteRecipe.objects.get_or_create(
                user=user, recipe=recipe
            )
            if not created:
                return Response(
                    {'error': 'Запись уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = RecipeSimpleSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not user.favoriterecipe.filter(recipe=recipe).exists():
            return Response(
                {'error': 'Запись уже была удалена.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.favoriterecipe.filter(recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete',],
        detail=True,
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=[IsAuthenticated,]
    )
    def get_shopping_cart(self, request, pk):
        """Добавление рецептов в список покупок."""
        if not Recipe.objects.filter(id=pk).exists():
            if request.method == 'POST':
                return Response(
                    {'error': 'Рецепт не найден.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': 'Рецепт не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'POST':
            _, created = ShoppingCartRecipe.objects.get_or_create(
                user=user, recipe=recipe
            )
            if not created:
                return Response(
                    {'error': 'Запись уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = RecipeSimpleSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not user.shoppingcartrecipe.filter(recipe=recipe).exists():
            return Response(
                {'error': 'Запись уже была удалена.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.shoppingcartrecipe.filter(recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get',],
        detail=False,
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=[IsAuthenticated,]
    )
    def get_download_shopping_cart(self, request):
        """Скачивание списка покупок."""
        user = request.user
        if not user.shoppingcartrecipe.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        ingredients = IngredientAmount.objects.filter(
            recipe__shoppingcartrecipe__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        cart = f'Список покупок для {user.username}\n'
        for ingredient in ingredients:
            cart += (
                f'- {ingredient["ingredient__name"]}, '
                f'{ingredient["ingredient__measurement_unit"]} - '
                f'{ingredient["amount"]}\n'
            )

        response = HttpResponse(cart, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=cart.txt'
        return response
