import pyodbc
import pandas as pd

server = 'servidorrpueba.database.windows.net'
database = 'Bicicletas'
username = 'adminudea'
password = 'udea2020**'
driver = '{ODBC Driver 17 for SQL Server}'
db = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

cursor = db.cursor()


# ---------------------------------------------------------------------------------------------------
# registros

def insertar_registro(dato):
    query = "INSERT INTO registro (cedula, nombre, serie, marca, color) VALUES (" + str(dato[0]) + ", \'" + dato[
        1] + "\', \'" + dato[2] + "\', \'" + dato[3] + "\', \'" + dato[4] + "\')"

    cursor.execute(query)
    db.commit()


def select_registro(b=0):
    query = "SELECT * FROM registro"
    cursor.execute(query)
    resultado = cursor.fetchall()
    if b == 1:
        for i in resultado:
            print(i)
    else:
        return resultado


def delete_registro():
    query = "DELETE FROM registro WHERE cedula=0"
    cursor.execute(query)
    db.commit()


def where_registro(cedula):
    query = "SELECT * FROM registro WHERE cedula=" + str(cedula)
    cursor.execute(query)
    return cursor.fetchall()


def actualizar_registro(cedula, serie, marca, color):
    query = "UPDATE registro SET serie = \'" + serie + "\', marca = \'" + marca + "\', color = \'" + color + "\' WHERE cedula = " + cedula
    cursor.execute(query)
    db.commit()


# ------------------------------------------------------------------------------------------------------------
# Ingreso

def insertar_ingreso(dato):
    query = "INSERT INTO ingreso (cedula, nombre, horaingreso, porteriaingreso, disponible)  VALUES (" + str(
        dato[0]) + ", \'" + dato[
                1] + "\', \'" + dato[2] + "\', \'" + dato[3] + "\', \'" + dato[4] + "\')"
    print(query)
    cursor.execute(query)
    db.commit()


def cedula_ingreso(dato):
    query = "INSERT INTO ingreso (cedula, horaingreso) VALUES (%s, %s)"
    cursor.execute(query, dato)
    db.commit()


def nombre_porteria(name, pingreso, cedula):
    query = "UPDATE ingreso SET nombre = \'" + name + "\', porteriaingreso = \'" + pingreso + "\' WHERE cedula =" + str(
        cedula)
    cursor.execute(query)
    db.commit()


def salida_porteria(hora_salida, porteria_salida, cedula):
    query = "UPDATE ingreso SET horasalida= \'" + hora_salida + "\', porteriasalida = \'" + porteria_salida + "\' WHERE cedula=" + str(
        cedula)
    cursor.execute(query)
    db.commit()


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


def where_ingreso(cedula):
    query = "SELECT * FROM ingreso WHERE cedula=" + str(cedula)
    cursor.execute(query)
    return cursor.fetchall()


def delete_ingreso(cedula):
    query = "DELETE FROM ingreso WHERE cedula=" + str(cedula)
    cursor.execute(query)
    db.commit()


def limpiar_ingreso():
    query = "DELETE FROM ingreso"
    cursor.execute(query)
    db.commit()


def disponible_ingreso(cedula):
    query = "UPDATE ingreso SET disponible = 'false' WHERE cedula = " + cedula
    cursor.execute(query)
    db.commit()


# ---------------------------------------------------------------------------------------------
# Salida

def insert_salida(dato):
    # query = "INSERT INTO salida (cedula, nombre, porteriasalida, horasalida, disponible) VALUES (%s, %s, %s, %s, %s)"
    query = "INSERT INTO salida  VALUES (" + str(dato[0]) + ", \'" + dato[
        1] + "\', \'" + dato[2] + "\', \'" + dato[3] + "\', \'" + dato[4] + "\')"
    print(query)

    cursor.execute(query)
    db.commit()


def select_salida(b=0):
    query = "SELECT * FROM salida"
    cursor.execute(query)
    if b == 1:
        for i in cursor.fetchall():
            print(i)
    else:
        return cursor.fetchall()


def where_salida(cedula):
    query = "SELECT * FROM salida WHERE cedula=" + str(cedula)
    cursor.execute(query)
    return cursor.fetchall()


def hora_porteria_salida(cedula):
    query = "SELECT horasalida, porteriasalida FROM salida WHERE cedula=" + str(cedula)
    cursor.execute(query)
    return cursor.fetchall()


def limpiar_salida():
    query = "DELETE FROM salida"
    cursor.execute(query)
    db.commit()


def disponible_salida(cedula):
    query = "UPDATE salida SET disponible = 'false' WHERE cedula = " + cedula
    cursor.execute(query)
    db.commit()


# ---------------------------------------------------------------------------------------------
# Pendientes
def insert_pendientes_salida(dato):
    query = "UPDATE pendientes SET porteriasalida= \'" + dato[2] + "\', horasalida= \'" + dato[
        3] + "\', fechasalida= \'" + dato[4] + "\' WHERE cedula = " + str(dato[0])
    print(query)
    cursor.execute(query)
    db.commit()


def insert_pendientes_entrada(dato):
    query = "INSERT INTO pendientes (cedula, nombre, horaingreso, porteriaingreso, fechaingreso) VALUES (" + str(
        dato[0]) + ", \'" + dato[
                1] + "\', \'" + dato[2] + "\', \'" + dato[3] + "\', \'" + dato[4] + "\')"
    cursor.execute(query)
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


def where_pendientes(cedula):
    query = "SELECT * FROM pendientes WHERE cedula=" + str(cedula)
    cursor.execute(query)
    return cursor.fetchall()

def delete_pendiente(cedula):
    query = "DELETE FROM pendientes WHERE cedula= "+ str(cedula)
    cursor.execute(query)
    db.commit()
