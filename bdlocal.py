import mysql.connector as mysql

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

def insertar_ingreso(dato):
    query = "INSERT INTO ingreso (cc, nombre, hingreso, porteria, hsalida) VALUES (%s, %s, %s, %s, %s)"
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


def select_ingreso(b):
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






cursor.execute("CREATE TABLE ingreso (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, cc INT(11), nombre VARCHAR(255), horaingreso VARCHAR(255), porteriaingreso VARCHAR(255), horasalida VARCHAR(255), porteriasalida VARCHAR(255))")
cursor.execute("CREATE TABLE registro (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, cc INT(11), nombre VARCHAR(255), serie VARCHAR(255), marca VARCHAR(255), color VARCHAR(255), foto VARCHAR(255))")

