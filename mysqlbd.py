import mysql.connector as mysql

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="registro"

)

cursor = db.cursor()

cursor.execute("SELECT * FROM estudiante")

resultado = cursor.fetchall()
for i in resultado:
    print(i)



"""#Crear database, 
cursor.execute("CREATE DATABASE estudiante")
cursor.execute("SHOW DATABASES")
database = cursor.fetchall() #retorna una lista

Tablas, con primary key
cursor.execute("CREATE TABLE estudiante (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, cc INT(11), name VARCHAR(255), serie VARCHAR(255), marca VARCHAR(255), color VARCHAR(255), porteria VARCHAR(255), hora_ingreso VARCHAR(255), hora_salida VARCHAR(255))")
cursor.execute("SHOW TABLES")
tables = cursor.fetchall() #retorna una lista

Funcion DROP y DESC
cursor.execute("DROP TABLE estudiante") Elimina
cursor.execute("DESC estudiante")    Get all columns information

"""

"""
# Dropping Primary Key
cursor.execute("ALTER TABLE estudiante DROP id")
cursor.execute("DESC estudiante")
print(cursor.fetchall())
"""

"""
# Adding Primary Key
cursor.execute("ALTER TABLE estudiante ADD COLUMN id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
cursor.execute("DESC estudiante")
print(cursor.fetchall())
"""

"""
#Insertar
query = "INSERT INTO estudiante (cc, name, serie, marca, color, porteria, hora_ingreso, hora_salida) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
values = (1037648995, "Juan", "9738", "Shimano", "Verde", "Ferrocarril", "17:32:21", "22:32:12")
cursor.execute(query, values)
db.commit()
print(cursor.rowcount, "record inserted")
"""

"""
#Insertar multiples usuarios
query = "INSERT INTO estudiante (cc, name, serie, marca, color, porteria, hora_ingreso, hora_salida) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
values = [
(1037648999, "david", "9137", "Shimano", "negra", "Ferrocarril", "13:32:21", "20:32:12"),
(1037648991, "sofia", "9133", "GW", "azul", "Ferrocarril", "10:32:21", "18:22:12")
]
cursor.executemany(query, values)
db.commit()
print(cursor.rowcount, "records inserted")
"""

"""
# SELECT DATA
query = "SELECT * FROM estudiante"
cursor.execute(query)
records = cursor.fetchall()

for record in records:
    print(record)
"""

"""
# SELECT some columns
query = "SELECT name, cc FROM estudiante"
cursor.execute(query)
names = cursor.fetchall()

for name in names:
    print(name)
"""

"""
# Where
query = "SELECT * FROM estudiante WHERE id=2"
cursor.execute(query)
records = cursor.fetchall()

for record in records:
    print(record)
    """
"""
#ORDER BY

query = "SELECT * FROM estudiante ORDER BY name" # por defaul es ASC, pero tambien puede ser des
cursor.execute(query)
records = cursor.fetchall()

for record in records:
    print(record)
"""

"""
# DELETE
query = "DELETE FROM estudiante WHERE id=3"

cursor.execute(query)
db.commit()

query = "SELECT * FROM estudiante"
cursor.execute(query)
"""

"""
#Update
query = "UPDATE estudiante SET name = 'Sofi' WHERE id =1"

cursor.execute(query)
db.commit()
"""