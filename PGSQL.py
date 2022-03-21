from optparse import Values
from tkinter import Y
from tokenize import Name
import psycopg2
import time
# ---------------------------------------------------------------------------------------------

#definando os endereçamentos
DB_HOST = 'localhost'
DB_NAME = 'Teste'
DB_USER = 'postgres'
DB_PASS = '123'
DB_id = '5432'


conn = None
cur = None
#criando as tables no banco de dados postgres
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
                            Date timestamp without time zone NOT NULL,
                            repet BOOLEAN NOT NULL);
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

#insere os dados ao banco de dados em suas labels 
def write(NAME, DATE, REPET):
    cur.execute(
        "INSERT INTO cliente (name, date, repet) values (%s, %s, %s);", (NAME, DATE, REPET))
    conn.commit()

#Atualiza as datas para se repetirem na próxima semana  
def write_newdate(NEWDATE,DATENOW):
    cur.execute(
        "UPDATE cliente SET date=%s WHERE date=%s;", (NEWDATE, DATENOW))
    conn.commit()

#Cria uma tupla com o valores da table cliente.name 
def readname():
    cur.execute('SELECT cliente.name FROM cliente ;')
    Nomes = cur.fetchall()
    return Nomes

#Cria um tupla com os valores de cliente.date
def readDate():
    cur.execute('SELECT cliente.date FROM cliente;')
    Datas = cur.fetchall()
    return Datas

#Deleta os compromissos pelo id 
def excluircompromisso(y):
    cur.execute("DELETE FROM cliente WHERE cliente.id=%s;", (y))
    conn.commit()

#cria uma tupla dos valores do id padrão. Encontramos um "," no processo então tivemos que trasformar em uma lista para formata-los
def readid():
    cur.execute('SELECT cliente.id FROM cliente;')
    ides = cur.fetchall()
    lst = [list(row) for row in ides]
    print(lst)
    return lst

#Cria um tupla das datas, formatando-os para o padrão da lib datetime
def lista_datas():
    cur.execute('SELECT cliente.date FROM cliente;')
    Datas = cur.fetchall()
    lista_d = [list(row)[0].strftime(r"%Y-%m-%d %H:%M") for row in Datas]
    
    return lista_d

#cria uma lista com os valores bool dos compromissos, eles indicam se o compromisso de repete(True) ou não(False)
def read_repet():
    cur.execute('SELECT cliente.repet FROM cliente;')
    repet = cur.fetchall()
    lista_r = [list(row)[0] for row in repet]
    return lista_r



