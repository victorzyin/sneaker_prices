from sqlite3 import connect

def init_db():
    conn = connect("sneakers.db")

    conn.execute('''CREATE TABLE IF NOT EXISTS SNEAKERS
             (ID            VARCHAR      NOT NULL,
             TIME           CHAR(10)     NOT NULL,
             PRICE          INT          NOT NULL,
             PRIMARY KEY (ID, TIME)
             );''')

    return conn

def close(conn):
    conn.close()

def insert(conn, id, time, price):
    conn.execute("INSERT INTO SNEAKERS (ID, TIME, PRICE) VALUES (?, ?, ?)",
                 (id, time, price))
