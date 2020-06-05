import pyodbc
import pandas as pd

server = 'servidorrpueba.database.windows.net'
database = 'Bicicletas'
username = 'adminudea'
password = 'udea2020**'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(
   'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


Query = ("SELECT * "
         "FROM BiciUsuarios"
        )

sql = Query

df_complete = pd.read_sql(sql, cnxn)
print(df_complete)