from mysql.connector import (connection)
import configparser
import io
from la_mysql.db import connection

# Make the SQL command to executed
def makesql(id, subject, desc):
    sql = f"insert into topics (ID, subject, description) values ({id}, '{subject}', '{desc}')"
    print("SQL:", sql)
    return sql

# execute the 3 insert commands with different parameters
def insert(cursor, id):
    cursor.execute(makesql(id+1, "physics", "science and that"))
    cursor.execute(makesql(id+2, "biology", "animals and that"))
    cursor.execute(makesql(id+3, "german", "hilter and that"))
    cursor.execute("commit")

config = configparser.RawConfigParser()
config.read("config.properties")

user = config.get('DatabaseSection','mysql.user') 
password = config.get('DatabaseSection','mysql.password')
host = config.get('DatabaseSection','mysql.host')
port = config.get('DatabaseSection','mysql.port')
database = config.get('DatabaseSection','mysql.database')

details = f"{user} {password} {host} {port} {database}"
print("details ", details)

cnx = connection.openWith(user=user, password=password, host=host, port=port, database=database)

print("Connected ....")
mycursor = cnx.cursor()
insert(mycursor, 90)
print("insert_exectued")
cnx.close()
