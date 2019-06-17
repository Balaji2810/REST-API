import mysql.connector
import json


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="rest_api"
)

mycursor = mydb.cursor()
sql="select max(id) from invoices"
mycursor.execute(sql)
myresult =mycursor.fetchall()

i =myresult[0]
print(i)

