import os
import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


def read_csv(name_file):
    """Считывает данные из csv и возвращает список строк таблицы"""
    path = os.path.join('../../data/', name_file)
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        return list(reader)


def load_data(model, name_file):
    """
    Загрузка данных по имени модели.
    Не загружает данные во вспомогательную таблицу
    со связью многие ко многим
    """
    table = read_csv(name_file)
    model.objects.bulk_create(
        model(idx, *row) for idx, row in enumerate(table)
        )

#load_data(Ingredient, 'ingredients.csv')