import sqlalchemy

db = 'postgresql://vkinder:1234@localhost:5432/vkinder'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()


def get_id(table):
    last_id = connection.execute(f"""SELECT Id FROM {table} ORDER BY Id DESC;""").fetchone()
    new_id = last_id[0] + 1
    return new_id


def insert_result(user_id, search_data):
    offset = search_data.get('offset')
    keys = list(search_data.keys())
    result = ', '.join(keys[:-1])
    connection.execute(f"""INSERT INTO Search 
           VALUES({get_id('Search')}, '{user_id}', {offset}, '{result}');
    """)


def table_check(table):
    request = connection.execute(f"""SELECT * FROM {table};""").fetchall()
    print(request)


table_check('Search')