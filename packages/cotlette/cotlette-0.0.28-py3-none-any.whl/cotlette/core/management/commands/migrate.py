import os
import importlib
from datetime import datetime

from cotlette.core.management.base import BaseCommand
from cotlette.conf import settings
from cotlette.core.database.backends.sqlite3 import db


class Command(BaseCommand):
    help = (
        "Applies database migrations to bring the database schema up to date."
    )
    missing_args_message = "You must provide an app name or use --all to apply migrations for all apps."

    def add_arguments(self, parser):
        """
        Define command-line arguments for the migrate command.
        """
        parser.add_argument(
            "app_name",
            nargs="?",
            help="The name of the app to apply migrations for.",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            dest="all_apps",
            help="Apply migrations for all installed apps.",
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
                self.apply_migrations_for_app(app_label)
        elif app_name:
            # Если указано конкретное приложение
            self.apply_migrations_for_app(app_name)
        else:
            raise ValueError("You must provide an app name or use --all.")

    def apply_migrations_for_app(self, app_label):
        """
        Apply migrations for a specific app.
        """
        try:
            # Проверяем существование папки migrations
            app_path = os.path.join(*app_label.split('.'))
            migration_dir = os.path.join(settings.BASE_DIR, app_path, "migrations")
            if not os.path.exists(migration_dir):
                self.stdout.write(f"No migrations found for app '{app_label}'. Skipping.")
                return

            # Получаем список файлов миграций
            migration_files = [
                f for f in os.listdir(migration_dir)
                if f.endswith(".py") and not f.startswith("__")
            ]

            # Сортируем файлы миграций по временной метке
            migration_files.sort()

            # Применяем миграции
            applied_migrations = self.get_applied_migrations()
            for migration_file in migration_files:
                migration_name = migration_file[:-3]  # Убираем расширение .py
                if migration_name in applied_migrations:
                    self.stdout.write(f"Migration '{migration_name}' already applied. Skipping.")
                    continue

                # Импортируем и выполняем миграцию
                module_name = f"{app_label}.migrations.{migration_name}"
                migration_module = importlib.import_module(module_name)
                self.apply_migration(migration_module)

                # Отмечаем миграцию как выполненную
                self.mark_migration_as_applied(migration_name)

        except Exception as e:
            self.stderr.write(f"Error applying migrations for app '{app_label}': {e}")

    def get_applied_migrations(self):
        """
        Retrieve a set of applied migrations from the database.
        """
        try:
            # Создаем таблицу для отслеживания миграций, если её нет
            db.execute("""
                CREATE TABLE IF NOT EXISTS cotlette_migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app TEXT NOT NULL,
                    name TEXT NOT NULL,
                    applied TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db.commit()

            # Получаем список выполненных миграций
            cursor = db.execute("SELECT name FROM cotlette_migrations")
            return {row[0] for row in cursor.fetchall()}
        except Exception as e:
            self.stderr.write(f"Error retrieving applied migrations: {e}")
            return set()

    def apply_migration(self, migration_module):
        """
        Apply a single migration by executing its operations.
        """
        self.stdout.write(f"Applying migration '{migration_module.__name__}'...")
        for operation in migration_module.Migration.operations:
            if operation.__class__.__name__.startswith("CreateModel"):
                self.create_table(operation)
            elif operation.__class__.__name__.startswith("AddField"):
                self.add_field(operation)
            elif operation.__class__.__name__.startswith("RemoveField"):
                self.remove_field(operation)
            elif operation.__class__.__name__.startswith("DeleteModel"):
                self.delete_table(operation)
            else:
                self.stderr.write(f"Unsupported operation: {operation}")

    def create_table(self, operation):
        """
        Execute a CreateModel operation to create a new table.
        """
        model_name, fields = self.parse_create_model(operation)
        columns = []
        for field in fields:
            column_def = f'"{field[0]}" {field[1]}'
            column_atts = field[2] if len(field) == 3 else None
            if column_atts:
                primary_key = column_atts.get("primary_key")
                autoincrement = column_atts.get("autoincrement")
                unique = column_atts.get("unique")
                if primary_key:
                    column_def += " PRIMARY KEY"
                if autoincrement:
                    column_def += " AUTOINCREMENT"
                if unique:
                    column_def += " UNIQUE"
            columns.append(column_def)

        query = f"CREATE TABLE IF NOT EXISTS {model_name} ({', '.join(columns)})"
        db.execute(query)
        db.commit()

    def add_field(self, operation):
        """
        Execute an AddField operation to add a new column to a table.
        """
        table_name, field_name, field_type = self.parse_add_field(operation)
        query = f"ALTER TABLE {table_name} ADD COLUMN {field_name} {field_type}"
        db.execute(query)
        db.commit()

    def remove_field(self, operation):
        """
        Execute a RemoveField operation to drop a column from a table.
        """
        table_name, field_name = self.parse_remove_field(operation)
        query = f"ALTER TABLE {table_name} DROP COLUMN {field_name}"
        db.execute(query)
        db.commit()

    def delete_table(self, operation):
        """
        Execute a DeleteModel operation to drop a table.
        """
        table_name = self.parse_delete_model(operation)
        query = f"DROP TABLE IF EXISTS {table_name}"
        db.execute(query)
        db.commit()

    def mark_migration_as_applied(self, migration_name):
        """
        Mark a migration as applied in the database.
        """
        db.execute("""
            INSERT INTO cotlette_migrations (app, name)
            VALUES (?, ?)
        """, ("app_label", migration_name))  # TODO: Replace "app_label" with actual app name
        db.commit()

    def parse_create_model(self, operation):
        """
        Parse a CreateModel operation string into model name and fields.
        """
        model_name = operation.table
        fields = operation.fields
        return model_name, fields

    def parse_add_field(self, operation):
        """
        Parse an AddField operation string into table name, field name, and field type.
        """
        parts = operation.split("(")
        table_name = parts[0].split("table='")[1].split("'")[0]
        field_name = parts[1].split("name='")[1].split("'")[0]
        field_type = parts[1].split("type='")[1].split("'")[0]
        return table_name, field_name, field_type

    def parse_remove_field(self, operation):
        """
        Parse a RemoveField operation string into table name and field name.
        """
        parts = operation.split("(")
        table_name = parts[0].split("table='")[1].split("'")[0]
        field_name = parts[1].split("name='")[1].split("'")[0]
        return table_name, field_name

    def parse_delete_model(self, operation):
        """
        Parse a DeleteModel operation string into table name.
        """
        parts = operation.split("(")
        table_name = parts[0].split("name='")[1].split("'")[0]
        return table_name