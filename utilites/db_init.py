import sqlite3


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('db.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@ensure_connection
def initialize(conn):

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS t_users (
            pk_user_id INTEGER PRIMARY KEY,
            user_city TEXT
        )
    ''')

    conn.commit()
