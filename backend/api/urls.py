"""URL приложения API."""
from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
