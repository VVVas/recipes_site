"""
Загрузка ингредиентов из csv файл.

Путь и имя файла задаётся в setings.py в INGREDIENTS_CSV
В одной строке один ингредиент и его мера измерения разделённые запятой.
"""
import csv

from django.db import transaction
from django.conf import settings
from django.core.management import BaseCommand

from ...models import Ingredient


class Command(BaseCommand):
    """Класс команды управления Джанго."""

    @transaction.atomic
    def handle(self, *args, **options):
        """Код команды управления Джанго."""
        with open(settings.INGREDIENTS_CSV, encoding='utf-8') as file:
            data_csv = csv.reader(file)
            for row in data_csv:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
