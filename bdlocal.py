import mysql.connector as mysql
from datetime import date, datetime


# Conexión a base de datos

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="biciusuario"

)

cursor = db.cursor()


# cursor.execute("CREATE TABLE ingreso (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, cc INT(11), name VARCHAR(255), hingreso VARCHAR(255), porteria VARCHAR(255), hsalida VARCHAR(255))")


# -----------------------------------------------------------------------------------------------
# Funciones

# registros
def insertar_registro(dato):
    query = "INSERT INTO registro (cc, nombre, serie, marca, color) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, dato)
    db.commit()


def select_registro():
    query = "SELECT * FROM registro"
    cursor.execute(query)
    print("TABLA  registro")
    resultado = cursor.fetchall()
    for i in resultado:
        print(i)

    print("------------------------------------------------------------------------------")


def delete_registro():
    query = "DELETE FROM registro WHERE cc=0"
    cursor.execute(query)
    db.commit()


def where_registro(cc):
    query = "SELECT * FROM registro WHERE cc=" + str(cc)
    cursor.execute(query)
    return cursor.fetchall()


# ------------------------------------------------------------------------------------------------------------
#Ingreso

def insertar_ingreso(dato):
    query = "INSERT INTO ingreso (cc, nombre, horaingreso, porteriaingreso) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, dato)
    db.commit()


def cedula_ingreso(dato):
    query = "INSERT INTO ingreso (cc, horaingreso) VALUES (%s, %s)"
    cursor.execute(query, dato)
    db.commit()


def nombre_porteria(name, pingreso, cc):
    query = "UPDATE ingreso SET nombre = \'" + name + "\', porteriaingreso = \'" + pingreso + "\' WHERE cc =" + str(cc)
    cursor.execute(query)
    db.commit()

def salida_porteria(hora_salida, porteria_salida, cc):
    query = "UPDATE ingreso SET horasalida= \'" + hora_salida + "\', porteriasalida = \'" + porteria_salida + "\' WHERE cc=" + str(cc)
    cursor.execute(query)
    db.commit()

#horasalida VARCHAR(255), porteriasalida VARCHAR(255))

def select_ingreso(b=1):
    query = "SELECT * FROM ingreso"
    cursor.execute(query)
    print("TABLA ingreso")
    resultado = cursor.fetchall()
    if b == 0:
        for i in resultado:
            print(i)
        print("------------------------------------------------------------------------------")
    return resultado


def mostrar_tablas():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for i in tables:
        print(i)

def where_ingreso(cc):
    query = "SELECT * FROM ingreso WHERE cc="+ str(cc)
    cursor.execute(query)
    return cursor.fetchall()


def delete_ingreso(cc):
    query = "DELETE FROM ingreso WHERE cc=" + str(cc)
    cursor.execute(query)
    db.commit()

def limpiar_ingreso():
    query = "DELETE FROM ingreso"
    cursor.execute(query)
    db.commit()


#__________------------------------------------------------------------------------------------
#salida

def insert_salida(dato):
    query = "INSERT INTO salida (cc, nombre, porteriasalida, horasalida) VALUES (%s, %s, %s, %s)"
    cursor.execute(query,dato)
    db.commit()


def select_salida():
    query = "SELECT * FROM salida"
    cursor.execute(query)
    return cursor.fetchall()

def where_salida(cc):
    query = "SELECT * FROM salida WHERE cc=" + str(cc)
    cursor.execute(query)
    return cursor.fetchall()

def hora_porteria_salida(cc):
    query = "SELECT horasalida, porteriasalida FROM salida WHERE cc="+ str(cc)
    cursor.execute(query)
    return cursor.fetchall()

def limpiar_salida():
    query = "DELETE FROM salida"
    cursor.execute(query)
    db.commit()
#---------------------------------------------------------------------------------------------

def insert_pendientes_salida(dato):

    query = "UPDATE pendientes SET porteriasalida= \'"+ dato[2] +"\', horasalida= \'"+ dato[3] + "\', fechasalida= \'" + dato[4] + "\' WHERE cc = " + str(dato[0])
    print(query)
    cursor.execute(query)
    db.commit()

def insert_pendientes_entrada(dato):
    query = "INSERT INTO pendientes (cc, nombre, horaingreso, porteriaingreso, fechaingreso) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, dato)
    db.commit()

def select_pendientes(b=0):
    query = "SELECT * FROM pendientes"
    cursor.execute(query)
    pendientes = cursor.fetchall()
    if b == 1:
        for i in pendientes:
            print(i)
    else:
        return pendientes

def where_pendientes(cc):
    query = "SELECT * FROM pendientes WHERE cc="+ str(cc)
    cursor.execute(query)
    return cursor.fetchall()

#cursor.execute("DROP TABLE ingreso")
"""
cursor.execute("CREATE TABLE ingreso (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, cc INT(11), nombre VARCHAR(255), horaingreso VARCHAR(255), porteriaingreso VARCHAR(255))")
cursor.execute("CREATE TABLE registro (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, cc INT(11), nombre VARCHAR(255), serie VARCHAR(255), marca VARCHAR(255), color VARCHAR(255), foto VARCHAR(255))")

cursor.execute("CREATE TABLE salida (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, cc INT(11), nombre VARCHAR(255), horasalida VARCHAR(255), porteriasalida VARCHAR(255))")

cursor.execute("CREATE TABLE pendientes (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, cc INT(11), "
               "nombre VARCHAR(255), horaingreso VARCHAR(255), porteriaingreso VARCHAR(255), "
               "fechaingreso VARCHAR(255), horasalida VARCHAR(255), porteriasalida VARCHAR(255), "
               "fechasalida VARCHAR(255))")

"""
#cc = "1037648995"
#delete_ingreso(cc)
#query = "SHOW TABLES"
#cursor.execute(query)
#print(cursor.fetchall())
cc = 22069224
nombre = "Maria Cuartas"
hora = "00:06:21"
porteria = "Ferrocarril"
fecha = "01-06-2020"
dato = (cc, nombre, hora, porteria, fecha)
#insert_pendientes(dato)
#select_pendientes(1)
#cursor.execute("DROP TABLE ingreso")
#cursor.execute("DROP TABLE salida")
#select_pendientes(1)
#cursor.execute("DROP TABLE pendientes")
#insert_pendientes_entrada(dato)
#insert_pendientes_salida(dato)
#select_pendientes(1)
#insert_pendientes_entrada(dato)

