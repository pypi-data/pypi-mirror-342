from cotlette.core.database.fields import CharField, IntegerField, Field
from cotlette.core.database.manager import Manager
from cotlette.core.database.backends.sqlite3 import db
from cotlette.core.database.fields.related import ForeignKeyField

from cotlette.core.database.fields import AutoField


class ModelMeta(type):
    _registry = {}  # Словарь для хранения зарегистрированных моделей

    def __new__(cls, name, bases, attrs):
        # Создаем новый класс
        new_class = super().__new__(cls, name, bases, attrs)

        # Регистрируем модель в реестре, если это не базовый класс Model
        if name != "Model":
            cls._registry[name] = new_class

        # Собираем поля в словарь _fields
        fields = {}
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):  # Проверяем, является ли атрибут экземпляром Field
                attr_value.contribute_to_class(new_class, attr_name)  # Вызываем contribute_to_class
                fields[attr_name] = attr_value

        # Присоединяем _fields к классу
        new_class._fields = fields
        return new_class

    @classmethod
    def get_model(cls, name):
        """
        Возвращает модель по имени из реестра.
        """
        return cls._registry.get(name)


class Model(metaclass=ModelMeta):
    table = None

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.objects = Manager(cls)
        cls.objects.model_class = cls
    
    def __getattr__(self, name):
        """
        Динамический доступ к атрибутам объекта.
        Если атрибут не существует, вызывается AttributeError.
        """
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Динамическая установка значений атрибутов.
        """
        self.__dict__[name] = value
    
    def __str__(self):
        return "<%s object (%s)>" % (self.__class__.__name__, self.id)

    def to_dict(self, exclude_private=True):
        """
        Преобразование объекта модели в словарь.
        :param exclude_private: Если True, скрытые (private) поля не будут добавляться в словарь.
        """
        return {
            key: getattr(self, key)
            for key in self.__dict__
            if (not key.startswith("_") or not exclude_private)
        }

    @classmethod
    def create_table(cls):
        # Определяем имя таблицы
        if hasattr(cls, "table") and cls.table:
            table_name = cls.table  # Используем явное имя таблицы
        else:
            # Генерируем имя таблицы по умолчанию
            module_path = cls.__module__.split('.')
            if len(module_path) >= 3 and module_path[1] == "apps":
                app_name = module_path[2]  # Пример: 'users' или 'groups'
            else:
                raise ValueError(f"Invalid module path for model '{cls.__name__}': {cls.__module__}")
            table_name = f"{app_name}_{cls.__name__.lower()}"

        columns = []
        foreign_keys = []

        for field_name, field in cls._fields.items():
            # Формируем определение столбца
            column_def = f'"{field_name}" {field.column_type}'
            
            # Добавляем автоинкремент для первичного ключа
            if field.primary_key:
                if isinstance(field, AutoField):  # Проверяем, является ли поле автоинкрементным
                    column_def += " PRIMARY KEY AUTOINCREMENT"  # Для SQLite
                    # Если используется PostgreSQL, замените на "SERIAL PRIMARY KEY"
                else:
                    column_def += " PRIMARY KEY"
            
            if field.unique:
                column_def += " UNIQUE"
            columns.append(column_def)

            # Проверяем, является ли поле внешним ключом
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                foreign_keys.append(
                    f'FOREIGN KEY ("{field_name}") REFERENCES "{related_model.table or related_model.__name__}"("id")'
                )

        # Объединяем колонки и внешние ключи в один список
        all_parts = columns + foreign_keys

        # Формируем финальный SQL-запрос
        query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(all_parts)});'

        db.execute(query)  # Выполняем запрос на создание таблицы
        db.commit()        # Фиксируем изменения

    def save(self):
        """
        Сохраняет текущий объект в базе данных.
        Если объект уже существует (имеет id), выполняется UPDATE.
        Если объект новый (id отсутствует или равен None), выполняется INSERT.
        """
        # Получаем значения полей объекта
        data = {field: getattr(self, field, None) for field in self._fields}

        # Преобразуем значения в поддерживаемые SQLite типы
        def convert_value(value):
            if isinstance(value, (int, float, str, bytes, type(None))):
                return value
            elif hasattr(value, '__str__'):
                return str(value)  # Преобразуем объект в строку, если это возможно
            else:
                raise ValueError(f"Unsupported type for database: {type(value)}")

        data = {key: convert_value(value) for key, value in data.items()}

        # Проверяем, существует ли объект в базе данных
        if hasattr(self, 'id') and self.id is not None:
            # Обновляем существующую запись (UPDATE)
            fields = ', '.join([f"{key}=?" for key in data if key != 'id'])
            values = tuple(data[key] for key in data if key != 'id') + (self.id,)
            update_query = f"UPDATE {self.__class__.__name__} SET {fields} WHERE id=?"
            db.execute(update_query, values)
            db.commit()
        else:
            # Создаем новую запись (INSERT)
            fields = ', '.join([key for key in data if key != 'id'])
            placeholders = ', '.join(['?'] * len(data))
            values = tuple(data[key] for key in data if key != 'id')

            insert_query = f"INSERT INTO {self.__class__.__name__} ({fields}) VALUES ({placeholders})"
            db.execute(insert_query, values)
            db.commit()

            # Получаем id созданной записи
            self.id = db.lastrowid
