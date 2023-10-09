"""Права доступа."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Полный доступ только для автора."""

    def has_object_permission(self, request, view, obj):
        """Определение уровня доступа."""
        return request.method in SAFE_METHODS or obj.author == request.user
