import os.path
import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):

    def handle(self, *args, **options):
        file = 'ingredients.csv'
        file_path = os.path.join(DATA_ROOT, file)
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                status, created = Ingredient.objects.update_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
