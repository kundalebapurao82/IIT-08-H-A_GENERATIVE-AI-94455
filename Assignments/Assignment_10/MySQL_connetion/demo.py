import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASS")

database = "sunbeam"

try:
    conn = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database= database

    )

    print("Connected to MYSQL database!")

    # create a cursor to execute queries
    cursor = conn.cursor()

    # Ex. Fetch tables
    # cursor.execute("SHOW TABLES")
    # tables = cursor.fetchall()
    # print("Tables in database: ", tables)

    # Ex. fetch some data
    cursor.execute("SELECT * FROM employees LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


    
    # close cursor and connection
    cursor.close()
    conn.close()
    print("Connection closed.")



except mysql.connector.Error as err:
    print("Error: ", err)
