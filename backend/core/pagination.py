"""Пагинации."""
from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Пагинация с указанием размера страницы."""

    page_size_query_param = 'limit'
