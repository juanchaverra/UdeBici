import pyodbc
#import pandas as pd

# Query Data completa

# Query Data completa
server = 'servidorrpueba.database.windows.net'
database = 'Bicicletas'
username = 'adminudea'
password = 'udea2020**'
driver = '{ODBC Driver 19 for SQL Server}'
cnxn = pyodbc.connect(
   'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


Query = ("SELECT * "
         "FROM BiciUsuarios"
        )

sql = Query

#df_complete = pd.read_sql(sql, cnxn)






"""
conn = pyodbc.connect(
    'DRIVER=FreeTDS;SERVER=servidorrpueba.database.windows.net;PORT=1433;UID=adminudea;PWD=udea2020**;DATABASE=Bicicletas;UseNTLMv2=yes;TDS_Version=8.0')


cursor = conn.cursor()

cursor.execute("SELECT * FROM BiciUsuarios")
rows = cursor.fetchall()

if rows:
    print(rows)

"""