import sqlalchemy
import json
import os.path


class Database:

    def __init__(self, db):
        try:
            self.db = db
            self.engine = sqlalchemy.create_engine(self.db)
            self.connection = self.engine.connect()
        except sqlalchemy.exc.OperationalError:
            self.db = None
            self.engine = None
            self.connection = None

    def _get_id(self, table):
        """Служебная. Возвращает id для новой записи в таблицу БД."""
        if self.connection is not None:
            last_id = self.connection.execute(f"""SELECT Id FROM {table} ORDER BY Id DESC;""").fetchone()
            new_id = last_id[0] + 1
        else:
            new_id = 1
        return new_id

    def _get_offset(self, table, user_id):
        """Служебная. Возвращает оффсет для поиска Вконтакте."""
        if self.connection is not None:
            current_offset = self.connection.execute(f"""SELECT user_offset FROM {table} ORDER BY Id DESC;""").fetchone()
        else:
            if os.path.exists(f'{user_id}.json') is True:
                with open(f"{user_id}.json", "r") as file:
                    result = json.load(file)
                    current_offset = [result.get('offset'), 0]
            else:
                current_offset = [1,0]
        return current_offset

    def insert_result(self, user_id, search_data):
        """Добавляет новую запись в базу данных."""
        if self.connection is not None:
            offset = search_data.get('offset')
            keys = list(search_data.keys())
            result = ', '.join(keys[:-1])
            self.connection.execute(f"""INSERT INTO Search 
               VALUES({self._get_id('Search')}, '{user_id}', {offset}, '{result}');
        """)
        else:
            with open(f"{user_id}.json", "w") as write_file:
                json.dump(search_data, write_file)

    def table_check(self, table, user_id):
        """Функция проверки таблицы."""
        if self.connection is not None:
            request = self.connection.execute(f"""SELECT * FROM {table};""").fetchall()
            print(request)
        else:
            print('Something went wrong. Database is not available.Checking if there is JSON file.')
            if os.path.exists(f'{user_id}.json') is True:
                with open(f"{user_id}.json", "r") as file:
                    result = json.load(file)
                print(result)
            else:
                print('No JSON file neither.')

