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
data = pd.read_excel('Zoo_data.xls')

# export
data.to_excel('Zoo_data.xls', index=False)

# Open the workbook and define the worksheet
book = xlrd.open_workbook("Zoo_data.xls")
sheet = book.sheet_by_name("Sheet1")

query1 = """
CREATE TABLE [LEAF].[ZZZ] (
    Name varchar(255),
    Class varchar(255),
    Population varchar(255)
)"""

query = """
INSERT INTO [LEAF].[ZZZ] (
     Name varchar(255),
    Class varchar(255),
    Population varchar(255)
) VALUES (?, ?, ?)"""

# execute create table
try:
    cursor.execute(query1)
    conn.commit()
except pyodbc.ProgrammingError:
    pass

# grab existing row count in the database for validation later
cursor.execute("SELECT count(*) FROM LEAF.ZZZ")
before_import = cursor.fetchone()

for r in range(1, sheet.nrows):
    Name = sheet.cell(r,0).value
    Class = sheet.cell(r,1).value
    Population = sheet.cell(r,2).value

    # Assign values from each row
    values = (Name, Class, Population)

    # Execute sql Query
    cursor.execute(query, values)

# Commit the transaction
cnx.commit()

# If you want to check if all rows are imported
cursor.execute("SELECT count(*) FROM LEAF.ZZZ")
result = cursor.fetchone()

print((result[0] - before_import[0]) == len(data.index))  # should be True

# Close the database connection
cnx.close()



