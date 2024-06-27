import mysql.connector
from mysql.connector import connection
import psycopg2
import jwt # namespace pyjwt: https://pyjwt.readthedocs.io/en/stable/usage.html
import datetime

cnx = mysql.connector.connect(user='scott', password='password', # CWEID 259
                              host='127.0.0.1',
                              database='employees')

cnx.close()

passwd = "passw0?d"

cnx1 = mysql.connector.connect(user='scott', password=passwd, # CWEID 259
                              host='127.0.0.1',
                              database='employees')

cnx1.close()

cnx2 = connection.MySQLConnection(user='scott', password='password', # CWEID 259
                                 host='127.0.0.1',
                                 database='employees')

cnx2.close()

passcode = "passw0?d"
cnx3 = connection.MySQLConnection(user='scott', password=passcode, # CWEID 259
                                 host='127.0.0.1',
                                 database='employees')

cnx3.close()


config = {
  'user': 'scott',
  'password': 'password', 
  'host': '127.0.0.1',
  'database': 'employees',
  'raise_on_warnings': True
}

cnx4 = mysql.connector.connect(**config) # CWEID 259

cnx4.close()

conn = psycopg2.connect("dbname=test user=postgres password=secret") # CWEID 259
conn.close()

conn_str = "dbname=test user=postgres password=secret"
conn1 = pycopg2.connect(conn_str) # CWEID 259
conn1.close()

conn2 = psycopg2.connect(dbname="test", user="postgres", password="secret") # CWEID 259
conn2.close()

secret = "super-secret"
conn3 = psycopg2.connect(dbname="test", user="postgres", password=secret) # CWEID 259
conn3.close()

account_id = "NOT-TO-BE-DISCLOSED" # CWEID 259
secret_key = "SUPER-SECRET-KEY" # CWEID 259 ??
sfuid = 25319  
issue_at = datetime.datetime.utcnow().timestamp()
payload = {"SFUID": sfuid, "issue_at": issue_at}
headers = {"alg": "HS256", "typ": "JWT"}
jwt_token = jwt.encode(payload, secret_key, headers=headers) # CWEID 259
