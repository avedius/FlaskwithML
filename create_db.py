import mysql.connector
from app import db
# import pymysql
# pymysql.install_as_MySQLdb()

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    port = 3306,
    passwd="password",
)

# conn = pymysql.connect(
#     host = 'localhost',
#     port = 3306,
#     user = 'root',
#     passwd = 'password',
# )
    
my_cursor = mydb.cursor()
my_cursor.execute(" CREATE DATABASE app")
my_cursor.execute("SHOW DATABASES")
my_cursor.execute("GRANT all privileges on dbx.* to 'x'@'127.0.0.1' IDENTIFIED BY 'x' WITH GRANT OPTION;")
for db in my_cursor:
    print (db)


# db.create_all()