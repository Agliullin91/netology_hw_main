import sqlalchemy


class Database:

    db = 'postgresql://vkinder:1234@localhost:5432/vkinder'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()

    @staticmethod
    def _get_id(table):
        """Служебная. Возвращает id для новой записи в таблицу БД."""
        last_id = Database.connection.execute(f"""SELECT Id FROM {table} ORDER BY Id DESC;""").fetchone()
        new_id = last_id[0] + 1
        return new_id

    @staticmethod
    def insert_result(user_id, search_data):
        """Добавляет новую запись в базу данных."""
        offset = search_data.get('offset')
        keys = list(search_data.keys())
        result = ', '.join(keys[:-1])
        Database.connection.execute(f"""INSERT INTO Search 
               VALUES({Database._get_id('Search')}, '{user_id}', {offset}, '{result}');
        """)

    @staticmethod
    def table_check(table):
        """Функция проверки таблицы."""
        request = Database.connection.execute(f"""SELECT * FROM {table};""").fetchall()
        print(request)
