"""URL приложения API."""
from django.urls import include, path
from rest_framework import routers

from .views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                    SubscriptionViewSet, TagViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register(
    'users/subscriptions',
    SubscriptionViewSet,
    basename='subscription'
)
router.register('users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
