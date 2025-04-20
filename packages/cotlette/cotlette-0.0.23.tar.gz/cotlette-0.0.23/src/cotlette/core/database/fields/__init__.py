class Field:
    def __init__(self, column_type, primary_key=False, default=None, unique=False):
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.unique = unique  # Добавляем поддержку параметра unique
    
    def contribute_to_class(self, model_class, name):
        """
        Метод, который связывает поле с моделью.
        :param model_class: Класс модели, к которой добавляется поле.
        :param name: Имя поля в модели.
        """
        self.name = name  # Устанавливаем имя поля
        self.model_class = model_class

        # Добавляем поле в список полей модели
        if not hasattr(model_class, '_meta'):
            model_class._meta = {}
        if 'fields' not in model_class._meta:
            model_class._meta['fields'] = []
        model_class._meta['fields'].append(self)

        # Если поле является первичным ключом, добавляем его в _meta
        if self.primary_key:
            if 'primary_key' in model_class._meta:
                raise ValueError(f"Model '{model_class.__name__}' already has a primary key.")
            model_class._meta['primary_key'] = self


class RelatedField(Field):
    def get_related_model(self):
        """
        Возвращает связанную модель.
        """
        from cotlette.core.database.models import ModelMeta
        if isinstance(self.to, str):
            try:
                return ModelMeta.get_model(self.to)
            except KeyError:
                raise ValueError(f"Related model '{self.to}' is not registered in ModelMeta.")
        return self.to

    def contribute_to_class(self, model_class, name):
        """
        Добавляет поле в метаданные модели и настраивает связь.
        """
        super().contribute_to_class(model_class, name)
        self.name = name
        self.cache_name = f"_{name}_cache"  # Устанавливаем cache_name здесь

        # Создаем атрибут для хранения значения внешнего ключа
        setattr(model_class, f"_{name}", None)

        # Добавляем поле в метаданные модели
        if not hasattr(model_class, '_meta'):
            model_class._meta = {}
        if 'foreign_keys' not in model_class._meta:
            model_class._meta['foreign_keys'] = []
        model_class._meta['foreign_keys'].append(self)

        # Настраиваем обратную связь в связанной модели
        related_model = self.get_related_model()
        if self.related_name and hasattr(related_model, '_meta'):
            if 'reverse_relations' not in related_model._meta:
                related_model._meta['reverse_relations'] = {}
            related_model._meta['reverse_relations'][self.related_name] = model_class


class CharField(Field):
    def __init__(self, max_length, **kwargs):
        super().__init__(f"VARCHAR({max_length})", **kwargs)

class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)

class AutoField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", primary_key=True, **kwargs)
