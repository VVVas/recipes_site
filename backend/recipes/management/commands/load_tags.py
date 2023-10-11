"""
Загрузка тегов из csv файл.

Путь и имя файла задаётся в setings.py в TAGS_CSV
В одной строке один тег, его цвет и его слаг разделённые запятой.
"""
import csv

from django.db import transaction
from django.conf import settings
from django.core.management import BaseCommand

from ...models import Tag


class Command(BaseCommand):
    """Класс команды управления Джанго."""

    @transaction.atomic
    def handle(self, *args, **options):
        """Код команды управления Джанго."""
        with open(settings.TAGS_CSV, encoding='utf-8') as file:
            data_csv = csv.reader(file)
            for row in data_csv:
                Tag.objects.get_or_create(
                    name=row[0],
                    color=row[1],
                    slug=row[2],
                )
