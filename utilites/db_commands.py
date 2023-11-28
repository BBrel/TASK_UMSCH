from utilites.db_init import ensure_connection


@ensure_connection
def add_user(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT pk_user_id FROM t_users WHERE pk_user_id = ?", (user_id,))

    if c.fetchone() is None:
        c.execute('INSERT INTO t_users(pk_user_id) VALUES(?)', (user_id,))
    conn.commit()


@ensure_connection
def add_city(conn, user_id, city):
    c = conn.cursor()
    c.execute('UPDATE t_users SET (user_city) = ? WHERE pk_user_id = ?', (city, user_id,))
    conn.commit()


@ensure_connection
def get_user_city(conn, user_id):
    c = conn.cursor()
    c.execute('SELECT user_city FROM t_users WHERE pk_user_id = ?', (user_id,))
    return c.fetchone()


@ensure_connection
def check_user(conn, user_id):
    c = conn.cursor()
    c.execute('SELECT * FROM t_users WHERE pk_user_id = ?', (user_id,))
    return c.fetchone()
