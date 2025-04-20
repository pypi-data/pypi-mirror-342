import sqlite3


class Database:
    def __init__(self):
        self.db_url = "db.sqlite3"

    def connect(self):
        """Создает новое соединение с базой данных."""
        return sqlite3.connect(self.db_url)
    
    def execute(self, query, params=None, fetch=False):
        """
        Выполняет SQL-запрос и возвращает результат (если требуется).
        :param query: SQL-запрос для выполнения.
        :param params: Параметры для подстановки в запрос.
        :param fetch: Если True, возвращает результаты запроса.
        :return: Курсор или результаты запроса.
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            return cursor  # Возвращаем курсор для доступа к атрибутам

    def commit(self):
        """Фиксирует изменения в базе данных."""
        with self.connect() as conn:
            conn.commit()


# Создаем экземпляр Database
db = Database()