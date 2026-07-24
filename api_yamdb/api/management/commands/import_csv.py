import csv
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')

IMPORT_CONFIG = (
    ('users.csv', 'users', 'User', {}),
    ('category.csv', 'reviews', 'Category', {}),
    ('genre.csv', 'reviews', 'Genre', {}),
    ('titles.csv', 'reviews', 'Title', {'category': 'category_id'}),
    ('genre_title.csv', 'reviews', 'Title_genre', {}),
    ('review.csv', 'reviews', 'Review', {'author': 'author_id'}),
    ('comments.csv', 'reviews', 'Comment', {'author': 'author_id'}),
)


class Command(BaseCommand):
    """Команда для импорта данных из CSV файлов в базу данных."""
    help = 'Импортирует все CSV файлы из static/data/ в базу данных'

    def handle(self, *args, **options):
        for file_name, app_label, model_name, field_map in IMPORT_CONFIG:
            self.import_file(file_name, app_label, model_name, field_map)

    def get_model(self, app_label, model_name):
        if model_name == 'Title_genre':
            return apps.get_model('reviews', 'Title').genre.through
        return apps.get_model(app_label, model_name)

    def get_field_info(self, model):
        """Собирает списки nullable, auto_now_add и допустимых полей модели."""
        nullable_fields = set()
        auto_now_add_fields = set()
        for field in model._meta.fields:
            if field.null:
                nullable_fields.add(field.name)
                nullable_fields.add(field.attname)
            if getattr(field, 'auto_now_add', False):
                auto_now_add_fields.add(field.name)
        valid_fields = {field.name for field in model._meta.fields} | {
            field.attname for field in model._meta.fields
        }
        return nullable_fields, auto_now_add_fields, valid_fields

    def build_row_data(self, row, field_map,
                       nullable_fields, auto_now_add_fields,
                       valid_fields):
        """Преобразует строку CSV в данные для создания/обновления объекта."""
        data = {}
        deferred = {}

        for column, raw_value in row.items():
            field_name = field_map.get(column, column)
            if field_name != 'id' and field_name not in valid_fields:
                continue
            if raw_value == '' and field_name in nullable_fields:
                value = None
            else:
                value = raw_value
            if field_name in auto_now_add_fields:
                deferred[field_name] = value
            else:
                data[field_name] = value

        return data, deferred

    def save_row(self, model, data, deferred):
        """Создаёт или обновляет объект модели и применяет отложенные поля."""
        pk = data.pop('id', None)
        if pk is not None:
            obj, is_created = model.objects.update_or_create(
                id=pk, defaults=data
            )
        else:
            obj = model.objects.create(**data)
            is_created = True

        if deferred:
            model.objects.filter(pk=obj.pk).update(**deferred)

        return is_created

    def import_file(self, file_name, app_label, model_name, field_map):
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.WARNING(f'Файл {file_name} не найден, пропуск'))
            return

        model = self.get_model(app_label, model_name)
        nullable_fields, auto_now_add_fields, valid_fields = (
            self.get_field_info(model)
        )

        created = updated = 0

        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data, deferred = self.build_row_data(
                    row, field_map, nullable_fields,
                    auto_now_add_fields, valid_fields
                )
                is_created = self.save_row(model, data, deferred)
                if is_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{file_name} -> {model.__name__}: '
                f'создано {created}, обновлено {updated}'
            )
        )
