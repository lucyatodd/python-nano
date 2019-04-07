from mysql.connector import (connection)
import configparser
import io
import pandas as pd

config = configparser.RawConfigParser()
config.read("config.properties")

user = config.get('DatabaseSection','mysql.user') 
password = config.get('DatabaseSection','mysql.password')
host = config.get('DatabaseSection','mysql.host')
port = config.get('DatabaseSection','mysql.port')
database = config.get('DatabaseSection','mysql.database')

cnx = connection.MySQLConnection(user=user, password=password, host=host, port=port, database=database)

cursor = database.cursor()

# read data
book = pd.read_excel('Zoo_data.xlsx')
book.head()

query1 = """
    CREATE TABLE [Zoo](
        Name varchar(255),
        Class varchar(255),
        Population varchar(255)
    )"""

query = """
    INSERT INTO [Zoo] (
        Name varchar(255),
        Class varchar(255),
        Population varchar(255)
    ) VALUES (?, ?, ?)"""

# execute create table
cursor.execute(query1)
cnx.commit()

# grab existing row count in the database for validation later
cursor.execute("SELECT count(*) FROM Zoo")
before_import = cursor.fetchone()

for r in range(1, book.nrows):
    Name = book.cell(r,0).value
    Class = book.cell(r,1).value
    Population = book.cell(r,2).value

    # Assign values from each row
    values = (Name, Class, Population)

    # Execute sql Query
    cursor.execute(query, values)

# Commit the transaction
cnx.commit()

# If you want to check if all rows are imported
cursor.execute("SELECT count(*) FROM Zoo")
result = cursor.fetchone()

print((result[0] - before_import[0]) == len(book.index))


