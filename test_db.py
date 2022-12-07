import os
import requests
import mysql.connector

from datetime import datetime
from configparser import ConfigParser
from mysql.connector import Error

print("DB functional test")
print("-------------")
#reading configuration from file
config = ConfigParser()
config.read('config.ini')

#global parameters
mysql_config_mysql_host = config.get('mysql_config', 'mysql_host')
mysql_config_mysql_db = config.get('mysql_config', 'mysql_db')
mysql_config_mysql_user = config.get('mysql_config', 'mysql_user')
mysql_config_mysql_pass = config.get('mysql_config', 'mysql_pass')
connection = mysql.connector.connect(host=mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)

def get_cursor():
        global connection
        try:
                connection.ping(reconnect=True, attempts=1, delay=0)
                connection.commit()
        except mysql.connector.Error as err:
                print("No connection to db " + str(err))
                connection = init_db()
                connection.commit()
        return connection.cursor()

cursor = get_cursor()
cursor = connection.cursor(buffered=True)
#Check if it is possible to connect to database
print("Checking if it is possible to connect to database")
assert connection.is_connected() == True
print("SUCCESS!!")
print("----------")

#Check if it is possible to write to database
print("Checking if it is possible to write to database")
cursor.execute("SELECT * FROM ast_daily")
count = cursor.rowcount
try:
	result  = cursor.execute( "INSERT INTO `ast_daily` (`create_date`, `hazardous`, `name`, `url`, `diam_min`, `diam_max`, `ts`, `dt_utc`, `dt_local`, `speed`, `distance`, `ast_id`) VALUES ('testDate', '0', 'testName', 'testURL', '10.5', '99.9', '1234567890', 'testDateUTC', 'testDateLocal', '1234567890', '1234567890', '12345')")
	connection.commit()
except Error as e :
	print('Problem inserting asteroid values into DB: ' + str(e))
	pass
cursor.execute("SELECT * FROM ast_daily")
newCount = cursor.rowcount
assert newCount > count
print("SUCCESS!!")
print("-----------")

#Check if it is possible to edit entry in database
print("Checking if it is possible to edit database entry")
name = cursor.execute("SELECT id from ast_daily where name='testName'")
rec = cursor.fetchall()
cursor.execute("UPDATE ast_daily SET name='updated' where url='testURL'")
connection.commit()
newName = cursor.execute("SELECT id from ast_daily where url='testName'")
newRec = cursor.fetchall()
assert len(rec) > len(newRec)
print("SUCCESS!!")
print("-----------")

#Check if it is possible to delete entry from database
print("Checking if it is possible to delet database entry")
name = cursor.execute("SELECT id from ast_daily where name='updated'")
rec = cursor.fetchall()
cursor.execute("DELETE from ast_daily where url='testURL'")
connection.commit()
newName = cursor.execute("SELECT id from ast_daily where name='updated'")
newRec = cursor.fetchall()
assert len(rec) > len(newRec)
print("SUCCESS!!")
print("-----------")
print("DB tests finished. Database is ready to use!")
