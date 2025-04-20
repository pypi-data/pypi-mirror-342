from cotlette.core.database.backends.sqlite3 import db
from cotlette.core.database.fields.related import ForeignKeyField


class QuerySet:
    def __init__(self, model_class):
        self.model_class = model_class
        self.query = f'SELECT * FROM "{model_class.__name__}"'
        self.params = None

    def filter(self, **kwargs):
        # Создаем новый QuerySet для цепочки запросов
        new_queryset = QuerySet(self.model_class)
        conditions = []
        params = []

        for field_name, value in kwargs.items():
            if field_name not in self.model_class._fields:
                raise KeyError(f"Field '{field_name}' does not exist in model '{self.model_class.__name__}'")

            field = self.model_class._fields[field_name]

            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                if isinstance(value, related_model):
                    value = value.id  # Извлекаем id, если передан объект модели
                elif not isinstance(value, int):
                    raise ValueError(f"Invalid value for foreign key '{field_name}': {value}")

            conditions.append(f'"{field_name}"=?')
            params.append(value)

        # Формируем новый запрос с условиями
        new_queryset.query = f"{self.query} WHERE {' AND '.join(conditions)}"
        new_queryset.params = tuple(params)
        return new_queryset

    def all(self):
        result = db.execute(self.query, self.params, fetch=True)
        return [
            self.model_class(**{
                key: value for key, value in zip(self.model_class._fields.keys(), row)
                if key in self.model_class._fields
            })
            for row in result
        ]

    def first(self):
        # Добавляем LIMIT 1 к текущему запросу
        query = f"{self.query} LIMIT 1"
        result = db.execute(query, self.params, fetch=True)

        if result:
            row = result[0]
            return self.model_class(**{
                key: value for key, value in zip(self.model_class._fields.keys(), row)
                if key in self.model_class._fields
            })
        return None

    def execute(self):
        # Выполняем текущий запрос и возвращаем результат
        result = db.execute(self.query, self.params, fetch=True)
        return [
            self.model_class(**dict(zip(self.model_class._fields.keys(), row)))
            for row in result
        ]

    def create(self, **kwargs):
        fields = []
        placeholders = []
        values = []

        for field_name, value in kwargs.items():
            # Проверяем, существует ли поле в текущей модели
            if field_name not in self.model_class._fields:
                raise KeyError(f"Field '{field_name}' does not exist in model '{self.model_class.__name__}'")

            field = self.model_class._fields[field_name]

            # Обработка внешних ключей
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                if isinstance(value, related_model):
                    value = value.id  # Извлекаем id, если передан объект модели
                elif not isinstance(value, int):  # Проверяем, что значение — число
                    raise ValueError(f"Invalid value for foreign key '{field_name}': {value}")

            fields.append(f'"{field_name}"')
            placeholders.append("?")
            values.append(value)

        # Формируем SQL-запрос
        insert_query = f'INSERT INTO "{self.model_class.__name__}" ({", ".join(fields)}) VALUES ({", ".join(placeholders)})'
        cursor = db.execute(insert_query, values)
        db.commit()

        if not hasattr(cursor, 'lastrowid') or cursor.lastrowid is None:
            raise RuntimeError("Failed to retrieve the ID of the newly created record.")
        return self.model_class.objects.get(id=cursor.lastrowid)

    def save(self, instance):
        data = instance.__dict__

        if hasattr(instance, 'id') and instance.id is not None:
            fields = ', '.join([f'"{key}"=?' for key in data if key != 'id'])
            values = tuple(data[key] for key in data if key != 'id') + (instance.id,)
            update_query = f'UPDATE "{self.model_class.__name__}" SET {fields} WHERE id=?'
            db.execute(update_query, values)
            db.commit()
        else:
            fields = ', '.join([f'"{key}"' for key in data if key != 'id'])
            placeholders = ', '.join(['?'] * len(data))
            values = tuple(data[key] for key in data if key != 'id')

            insert_query = f'INSERT INTO "{self.model_class.__name__}" ({fields}) VALUES ({placeholders})'
            db.execute(insert_query, values)
            db.commit()

            if not hasattr(db, 'lastrowid') or db.lastrowid is None:
                raise RuntimeError("Failed to retrieve the ID of the newly created record.")
            instance.id = db.lastrowid

        return instance