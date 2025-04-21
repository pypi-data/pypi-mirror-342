import os
import hashlib
from datetime import datetime
import re

from cotlette.core.database.fields import AutoField
from cotlette.core.management.base import BaseCommand
from cotlette.utils.module_loading import import_string
from cotlette.conf import settings


class Command(BaseCommand):
    help = (
        "Creates new migration files based on changes detected in your models."
    )
    missing_args_message = "You must provide an app name or use --all to generate migrations for all apps."

    def add_arguments(self, parser):
        """
        Define command-line arguments for the makemigrations command.
        """
        parser.add_argument(
            "app_name",
            nargs="?",
            help="The name of the app to create migrations for.",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            dest="all_apps",
            help="Generate migrations for all installed apps.",
        )

    def handle(self, *args, **options):
        """
        Main entry point for the command.
        """
        app_name = options.get("app_name")
        all_apps = options.get("all_apps")

        # Если указан флаг --all, обрабатываем все приложения из INSTALLED_APPS
        if all_apps:
            for app_label in settings.INSTALLED_APPS:
                self.create_migrations_for_app(app_label)
        elif app_name:
            # Если указано конкретное приложение
            self.create_migrations_for_app(app_name)
        else:
            raise ValueError("You must provide an app name or use --all.")

    def create_migrations_for_app(self, app_label):
        """
        Create migration files for a specific app.
        """
        try:
            # Импортируем модуль models.py для приложения
            models_module = import_string(f"{app_label}.models")
        except ImportError:
            self.stderr.write(f"Could not find models module for app '{app_label}'. Skipping.")
            return

        # Получаем список всех моделей в приложении
        models = [
            model for model in vars(models_module).values()
            if isinstance(model, type) and hasattr(model, "_meta")  # Проверяем, что это модель
        ]

        if not models:
            self.stdout.write(f"No models found in app '{app_label}'. Skipping.")
            return

        # Генерируем путь для сохранения миграций
        app_path = os.path.join(*app_label.split('.'))
        migration_dir = os.path.join(settings.BASE_DIR, app_path, "migrations")
        os.makedirs(migration_dir, exist_ok=True)

        # Проверяем, есть ли изменения в моделях
        current_state_hash = self.calculate_models_hash(models)
        last_migration_hash = self.get_last_migration_hash(migration_dir)

        if current_state_hash == last_migration_hash:
            self.stdout.write(f"No changes detected in app '{app_label}'. Skipping migration creation.")
            return

        # Создаем новую миграцию
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        migration_file_name = f"{timestamp}_auto.py"
        migration_file_path = os.path.join(migration_dir, migration_file_name)

        # Создаем содержимое файла миграции
        migration_content = self.generate_migration_content(app_label, models)

        # Сохраняем файл миграции
        with open(migration_file_path, "w") as migration_file:
            migration_file.write(migration_content)

        # Обновляем хеш последней миграции
        self.save_last_migration_hash(migration_dir, current_state_hash)

        self.stdout.write(f"Created migration file: {migration_file_path}")

    def calculate_models_hash(self, models):
        """
        Calculate a hash representing the current state of the models.
        """
        model_definitions = []
        for model in models:
            fields = []
            for field_name, field in model._fields.items():
                params = {}
                if field.primary_key:
                    params["primary_key"] = True
                if field.unique:
                    params["unique"] = True
                # Добавляем другие параметры, если они есть
                field_definition = f'("{field_name}", "{field.column_type}", {params})'
                fields.append(field_definition)
            model_definitions.append(f"{model.__name__}({', '.join(fields)})")
        return hashlib.sha256("\n".join(sorted(model_definitions)).encode()).hexdigest()

    def get_last_migration_hash(self, migration_dir):
        """
        Retrieve the hash of the last migration from the __init__.py file.
        """
        init_file_path = os.path.join(migration_dir, "__init__.py")
        if not os.path.exists(init_file_path):
            return None

        with open(init_file_path, "r") as init_file:
            content = init_file.read()
            match = re.search(r"# Last migration hash: (\w+)", content)
            if not match:
                self.stderr.write(f"Could not find last migration hash in '{init_file_path}'.")
                return None
            return match.group(1)

    def save_last_migration_hash(self, migration_dir, hash_value):
        """
        Save the hash of the current migration to the __init__.py file.
        """
        init_file_path = os.path.join(migration_dir, "__init__.py")
        with open(init_file_path, "a") as init_file:
            init_file.write(f"\n# Last migration hash: {hash_value}\n")

    def generate_migration_content(self, app_label, models):
        """
        Generate the content of the migration file with proper formatting.
        """
        imports = ["from cotlette.core import migrations"]
        operations = []

        for model in models:
            # Добавляем операцию создания таблицы для каждой модели
            table_name = model.get_table_name()
            fields = []
            for field_name, field in model._fields.items():
                field_definition = f'("{field_name}", "{field.column_type}"'
                params = {}
                if isinstance(field, AutoField):  # Проверяем, является ли поле автоинкрементным
                    params["autoincrement"] = True
                if field.primary_key:
                    params["primary_key"] = True
                if field.primary_key:
                    params["primary_key"] = True
                if field.unique:
                    params["unique"] = True
                if params:
                    field_definition += f", {params}"
                field_definition += ")"
                fields.append(field_definition)

            # Формируем строку с полями, разделяя их запятыми и добавляя отступы
            formatted_fields = ",\n                ".join(fields)

            # Добавляем операцию CreateModel с отступами
            operations.append(
                f"""\
migrations.CreateModel(
            name='{model.__name__}',
            table='{model.get_table_name()}',
            fields=[
                {formatted_fields}
            ],
        )"""
            )

        # Формируем полный текст миграции
        imports_section = "\n".join(imports)
        operations_section = ",\n\n        ".join(operations)

        return f"""\
{imports_section}

class Migration:
    dependencies = []

    operations = [
        {operations_section}
    ]
"""