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
            client_id INTEGER NOT NULL REFERENCES client(id)
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


def change_client(conn, id, firstname=None, lastname=None, email=None, phones=None):
    arg_list = {'firstname': firstname, "lastname": lastname, 'email': email}
    for key, arg in arg_list.items():
        if arg:
            conn.execute(SQL("UPDATE client SET {}=%s WHERE id=%s").format(Identifier(key)), (arg, id))
    conn.execute("""
                SELECT * FROM client
                WHERE id=%s
                """, id)
    print(cur.fetchall())


def delete_phone(conn, client_id=None, phone_number=None):
    cur.execute("""
        DELETE FROM phone WHERE client_id=%s AND phone_number=%s;
    """, (client_id, phone_number))
    cur.execute("""
           SELECT * FROM phone;
           """)
    print(cur.fetchall())


def delete_client(conn, client_id):
    pass


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass

with psycopg2.connect(database="clients", user="postgres", password="956841") as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE client cascade;
        DROP TABLE phone cascade;
        """)
        create_db(cur)
        add_client(cur, 'will', 'smith', 'agent_j@mail.ru')
        add_phone(cur, 1, 999216)
        add_phone(cur, 1, 216546)
        # print(cur.fetchall())
        # print(change_client(cur, '1', firstname='Tomas', email='a_tomas@mail.ru'))
        delete_phone(cur, 1, 999216)
        print(cur.fetchall())





conn.close()



