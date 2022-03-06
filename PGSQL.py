from optparse import Values
from tkinter import Y
from tokenize import Name
import psycopg2

DB_HOST = 'localhost'
DB_NAME = 'Teste'
DB_USER = 'postgres'
DB_PASS = '123'
DB_id = '5432'


conn = None
cur = None
try:
    conn = psycopg2.connect(dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_id)
    cur = conn.cursor()
    create_script = ''' CREATE TABLE IF NOT EXISTS cliente (
                            id SMALLSERIAL PRIMARY KEY,
                            name varchar(40) NOT NULL,
                            Date timestamp without time zone NOT NULL);
                            '''

    cur.execute(create_script)

    conn.commit()
except Exception as error:
    print(error)
    conn.rollback()

# finally:
#     if cur is not None:
#         cur.close()
#     if conn is not None:
#         conn.close()


def write(NAME, DATE):
    cur.execute(
        "INSERT INTO cliente (name, date) values (%s, %s);", (NAME, DATE))
    conn.commit()


def readname():
    cur.execute('SELECT cliente.name FROM cliente ;')
    Nomes = cur.fetchall()
    return Nomes


def readDate():
    cur.execute('SELECT cliente.date FROM cliente;')
    Datas = cur.fetchall()
    return Datas


def excluircompromisso(y):
    cur.execute("DELETE FROM cliente WHERE cliente.id=%s;", (y))
    conn.commit()


def readid():
    cur.execute('SELECT cliente.id FROM cliente;')
    ides = cur.fetchall()
    lst = [list(row) for row in ides]
    print(lst)
    return lst


#    return ides
