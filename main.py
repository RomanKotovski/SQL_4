import psycopg2
from psycopg2.sql import SQL, Identifier


def create_db(conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(40) NOT NULL,
            lastname VARCHAR(40) NOT NULL,
            email VARCHAR(60) NOT NULL UNIQUE
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id SERIAL PRIMARY KEY,
            phone_number INTEGER NOT NULL,
            client_id INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE
        );
        """)

def add_client(conn, firstname, lastname, email, phone_number=None):
    cur.execute("""
        INSERT INTO client(firstname, lastname, email) 
        VALUES (%s, %s, %s) 
        RETURNING id, firstname, lastname, email;     
        """, (firstname, lastname, email))
    print(cur.fetchone())


def add_phone(conn, client_id, phone_number):
    cur.execute("""
        INSERT INTO phone(phone_number, client_id) 
        VALUES (%s, %s) 
        RETURNING client_id, id, phone_number;     
        """, (phone_number, client_id))
    print(cur.fetchone())


def change_client(conn, client_id, firstname=None, lastname=None, email=None, phones=None):
    arg_list = {'firstname': firstname, "lastname": lastname, 'email': email}
    for key, arg in arg_list.items():
        if arg:
            conn.execute(SQL("UPDATE client SET {}=%s WHERE id=%s").format(Identifier(key)), (arg, client_id))
    conn.execute("""
                SELECT * FROM client
                WHERE id=%s
                """, client_id)
    print(cur.fetchall())


def delete_phone(conn, client_id, phone_number):
    cur.execute("""
        DELETE FROM phone WHERE client_id=%s AND phone_number=%s;
    """, (client_id, phone_number))
    cur.execute("""
           SELECT * FROM phone;
           """)
    print(cur.fetchall())

def delete_client(conn, client_id):
    cur.execute("""
        DELETE FROM client WHERE id=%s;
    """, (client_id,))
    cur.execute("""
            SELECT * FROM client;
            """)
    print(cur.fetchall())

def find_client(conn, firstname=None, lastname=None, email=None, phone_number=None):
    cur.execute("""
        SELECT * FROM client c JOIN phone p ON c.id = p.client_id WHERE firstname=%s OR lastname=%s 
        OR email=%s OR p.phone_number=%s;
        """, (firstname, lastname, email, phone_number))
    print(cur.fetchall())

with psycopg2.connect(database="clients", user="postgres", password="956841") as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE client cascade;
        DROP TABLE phone cascade;
        """)
        create_db(cur)
        add_client(cur, 'Will', 'Smith', 'agent_j@mail.ru')
        add_client(cur, 'Tony', 'Stark', 'ironman@mail.ru')
        add_phone(cur, 1, 999216)
        add_phone(cur, 1, 216546)
        add_phone(cur, 2, 9999999)
        # change_client(cur, '1', firstname='Tomas', email='a_tomas@mail.ru')
        find_client(cur, 'Tony')

conn.close()



