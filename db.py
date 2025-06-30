import mysql.connector
import time

connection:mysql.connector

def initConnection():
    global connection
    connection =  mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace 'your_password' with your MySQL root password
        database="Athena"
    )

def closeConnection():
    global connection
    connection.close()
    
def addCommandLogs(command:str, output:str):
    pass


initConnection()

cursor = connection.cursor()

cursor.execute("SHOW DATABASES;")

result = cursor.fetchall()

for r in result:
    print(r)


closeConnection()
