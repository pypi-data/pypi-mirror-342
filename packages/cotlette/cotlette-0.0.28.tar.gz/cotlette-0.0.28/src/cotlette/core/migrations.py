import sqlite3
from pathlib import Path
from typing import List, Any

# Импортируем настройки базы данных
from config.settings import DATABASES


class Migration:
    """
    Base class for all migrations.
    Each migration should inherit from this class and define `dependencies` and `operations`.
    """

    dependencies: List[str]
    operations: List[Any]

    def __init__(self):
        """
        Initialize the migration.
        """
        self.dependencies = []
        self.operations = []

    def apply(self):
        """
        Apply the migration by executing its operations.
        """
        # Подключаемся к базе данных
        db_path = DATABASES["default"]["NAME"]
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        try:
            for operation in self.operations:
                operation.execute(cursor)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def unapply(self):
        """
        Unapply the migration by reversing its operations.
        """
        # Подключаемся к базе данных
        db_path = DATABASES["default"]["NAME"]
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        try:
            for operation in reversed(self.operations):
                operation.reverse_execute(cursor)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()


class Operation:
    """
    Base class for all migration operations.
    Each operation should implement `execute` and `reverse_execute`.
    """

    def execute(self, cursor):
        """
        Execute the operation.
        This method should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses must implement the `execute` method.")

    def reverse_execute(self, cursor):
        """
        Reverse the operation.
        This method should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses must implement the `reverse_execute` method.")


class CreateModel(Operation):
    """
    Operation to create a new database table for a model.
    """

    def __init__(self, name: str, table:str, fields: list):
        """
        Initialize the CreateModel operation.

        :param name: The name of the model (table).
        :param fields: A list of fields for the model.
        """
        self.name = name
        self.table = table
        self.fields = fields

    def execute(self, cursor):
        """
        Execute the CreateModel operation.
        This method generates and runs the SQL to create the table.
        """
        columns = ", ".join([f"{field[0]} {field[1]}" for field in self.fields])
        query = f"CREATE TABLE {self.name} ({columns})"
        print(f"Executing SQL: {query}")
        cursor.execute(query)

    def reverse_execute(self, cursor):
        """
        Reverse the CreateModel operation.
        This method generates and runs the SQL to drop the table.
        """
        query = f"DROP TABLE IF EXISTS {self.name}"
        print(f"Executing SQL: {query}")
        cursor.execute(query)


class AddField(Operation):
    """
    Operation to add a new field to an existing model (table).
    """

    def __init__(self, model_name: str, field_name: str, field_type: str):
        """
        Initialize the AddField operation.

        :param model_name: The name of the model (table).
        :param field_name: The name of the field to add.
        :param field_type: The type of the field.
        """
        self.model_name = model_name
        self.field_name = field_name
        self.field_type = field_type

    def execute(self, cursor):
        """
        Execute the AddField operation.
        This method generates and runs the SQL to add the field.
        """
        query = f"ALTER TABLE {self.model_name} ADD COLUMN {self.field_name} {self.field_type}"
        print(f"Executing SQL: {query}")
        cursor.execute(query)

    def reverse_execute(self, cursor):
        """
        Reverse the AddField operation.
        This method generates and runs the SQL to remove the field.
        """
        query = f"ALTER TABLE {self.model_name} DROP COLUMN {self.field_name}"
        print(f"Executing SQL: {query}")
        cursor.execute(query)


class RemoveField(Operation):
    """
    Operation to remove a field from an existing model (table).
    """

    def __init__(self, model_name: str, field_name: str):
        """
        Initialize the RemoveField operation.

        :param model_name: The name of the model (table).
        :param field_name: The name of the field to remove.
        """
        self.model_name = model_name
        self.field_name = field_name

    def execute(self, cursor):
        """
        Execute the RemoveField operation.
        This method generates and runs the SQL to remove the field.
        """
        query = f"ALTER TABLE {self.model_name} DROP COLUMN {self.field_name}"
        print(f"Executing SQL: {query}")
        cursor.execute(query)

    def reverse_execute(self, cursor):
        """
        Reverse the RemoveField operation.
        This method generates and runs the SQL to re-add the field.
        """
        # Здесь нужно знать тип поля, чтобы его восстановить
        raise NotImplementedError("Re-adding a field requires knowing its type.")