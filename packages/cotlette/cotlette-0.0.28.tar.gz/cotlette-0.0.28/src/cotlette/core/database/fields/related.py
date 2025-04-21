from cotlette.core.database.fields import RelatedField
from cotlette.core.exceptions import ValidationError

class ForeignKeyField(RelatedField):
    """
    Поле для создания внешнего ключа между моделями.
    """

    def __init__(self, to, on_delete=None, related_name=None, to_field=None, **kwargs):
        """
        :param to: Связанная модель (класс или строка с именем модели).
        :param on_delete: Функция, которая определяет поведение при удалении связанного объекта.
        :param related_name: Имя обратной связи (опционально).
        :param to_field: Поле в связанной модели, которое используется для связи (по умолчанию PK).
        :param kwargs: Дополнительные параметры.
        """
        super().__init__("INTEGER", **kwargs)
        self.to = to  # Связанная модель
        self.on_delete = on_delete  # Поведение при удалении
        self.related_name = related_name  # Имя для обратной связи
        self.to_field = to_field  # Поле в связанной модели
        self.cache_name = None  # Имя для кэширования связанного объекта

    def contribute_to_class(self, model_class, name):
        """
        Добавляет поле в метаданные модели и настраивает связь.
        """
        super().contribute_to_class(model_class, name)
        self.name = name
        self.cache_name = f"_{name}_cache"

        # Создаем атрибут для хранения значения внешнего ключа
        setattr(model_class, f"_{name}", None)

        if not hasattr(model_class, '_meta'):
            model_class._meta = {}
        if 'foreign_keys' not in model_class._meta:
            model_class._meta['foreign_keys'] = []
        model_class._meta['foreign_keys'].append(self)

        related_model = self.get_related_model()
        if self.related_name and hasattr(related_model, '_meta'):
            if 'reverse_relations' not in related_model._meta:
                related_model._meta['reverse_relations'] = {}
            related_model._meta['reverse_relations'][self.related_name] = model_class

    def get_related_model(self):
        """
        Возвращает связанную модель.
        Если self.to — строка, то ищет модель в реестре.
        """
        from cotlette.core.database.models import ModelMeta
        if isinstance(self.to, str):
            try:
                return ModelMeta.get_model(self.to)
            except KeyError:
                raise ValueError(f"Related model '{self.to}' is not registered in ModelMeta.")
        return self.to
    
    def create_related_instance(self, related_data):
        """
        Создает и возвращает экземпляр связанной модели.
        """
        related_model = self.get_related_model()
        return related_model(**related_data)

    def validate(self, value):
        """
        Валидация значения внешнего ключа.
        """
        related_model = self.get_related_model()
        if value is None:
            return  # Допустимо, если поле необязательное
        if not isinstance(value, related_model):
            raise ValidationError(f"Value must be an instance of {related_model.__name__}.")

    def __get__(self, instance, owner):
        """
        Дескриптор для получения связанного объекта.
        """
        if instance is None:
            return self

        if hasattr(instance, self.cache_name):
            return getattr(instance, self.cache_name)

        related_model = self.get_related_model()
        related_id = instance.__dict__.get(self.name)

        if related_id is None:
            return None

        try:
            related_object = related_model.objects.filter(id=related_id).first()
        except Exception as e:
            raise ValueError(f"Failed to load related object for field '{self.name}': {e}")

        setattr(instance, self.cache_name, related_object)
        return related_object

    def __set__(self, instance, value):
        """
        Дескриптор для установки значения внешнего ключа.
        """
        if isinstance(value, self.get_related_model()):
            value = value.id  # Если передан объект модели, берем его id
        elif not isinstance(value, int) and value is not None:
            raise ValueError(f"Invalid value for foreign key '{self.name}': {value}")

        # Устанавливаем значение через внутренний атрибут, чтобы избежать рекурсии
        setattr(instance, f"_{self.name}", value)

        # Очищаем кэш при изменении значения
        if hasattr(instance, self.cache_name):
            delattr(instance, self.cache_name)