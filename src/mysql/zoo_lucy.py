import logging
import logging.config
from mysql.connector import (connection)
import configparser
import io
import pandas as pd
from IPython.display import display

logging.config.fileConfig("logging.properties")
logger = logging.getLogger("simpleExample")

config = configparser.RawConfigParser()
config.read("config.properties")

user = config.get('DatabaseSection','mysql.user') 
password = config.get('DatabaseSection','mysql.password')
host = config.get('DatabaseSection','mysql.host')
port = config.get('DatabaseSection','mysql.port')
database = config.get('DatabaseSection','mysql.database')

cnx = connection.MySQLConnection(user=user, password=password, host=host, port=port, database=database)

if (cnx) :
    logger.info("Connected")

cursor = cnx.cursor()

# read data
book = pd.read_excel('Zoo_data.xlsx')

if book is None : 
    logger.error("book not imported") 

dropZooTableDDL = "DROP TABLE Zoo"

createZooTableDDL = """
    CREATE TABLE  Zoo (
        Name varchar(255),
        Class varchar(255),
        Population int(255)
    )"""

logger.debug("Dropping Zoo Table")
cursor.execute(dropZooTableDDL)
cnx.commit()

logger.debug("Creating Zoo Table")
cursor.execute(createZooTableDDL)
cnx.commit()

# grab existing row count in the database for validation later
cursor.execute("SELECT count(*) FROM Zoo")
before_import = cursor.fetchone()

rowCount = len(book.index)
for r in range(1, rowCount):
    name = book.iloc[r,0]
    clazz = book.iloc[r,1]
    population = book.iloc[r,2]

# Assign values from each row
values = (name, clazz, population)

logger.debug("name: " + name)

# Execute sql Query
insertZooTableDDL = """
    INSERT INTO  Zoo (Name, Class, Population) 
        VALUES (values)
    )"""

cursor.execute(insertZooTableDDL)
cnx.commit()

# If you want to check if all rows are imported
cursor.execute("SELECT count(*) FROM Zoo")
result = cursor.fetchone()

logger.info((result[0] - before_import[0]) == len(book.index))

