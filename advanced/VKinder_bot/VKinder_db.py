import sqlalchemy


class Database:

    def __init__(self, db):
        self.db = db
        self.engine = sqlalchemy.create_engine(self.db)
        self.connection = self.engine.connect()

    def _get_id(self, table):
        """Служебная. Возвращает id для новой записи в таблицу БД."""
        last_id = self.connection.execute(f"""SELECT Id FROM {table} ORDER BY Id DESC;""").fetchone()
        new_id = last_id[0] + 1
        return new_id

    def _get_offset(self, table):
        """Служебная. Возвращает оффсет для поиска Вконтакте."""
        current_offset = self.connection.execute(f"""SELECT user_offset FROM {table} ORDER BY Id DESC;""").fetchone()
        return current_offset

    def insert_result(self, user_id, search_data):
        """Добавляет новую запись в базу данных."""
        offset = search_data.get('offset')
        keys = list(search_data.keys())
        result = ', '.join(keys[:-1])
        self.connection.execute(f"""INSERT INTO Search 
               VALUES({self._get_id('Search')}, '{user_id}', {offset}, '{result}');
        """)

    def table_check(self, table):
        """Функция проверки таблицы."""
        request = self.connection.execute(f"""SELECT * FROM {table};""").fetchall()
        print(request)
