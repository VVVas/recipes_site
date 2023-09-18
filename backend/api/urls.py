"""URL приложения API."""
from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, TagViewSet, RecipeViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('tags', TagViewSet, basename='tag')
router.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
]
