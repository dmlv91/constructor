import os
import requests
import mysql.connector

from datetime import datetime
from configparser import ConfigParser
from mysql.connector import Error

print("DB functional test")

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

#Check if it is possible to connect to database
print("Checking if it is possible to connect to database")
assert connection.is_connected() == True
print("SUCCESS!!")
print("----------")

#Check if it is possible to write to database
print("Checking if it is possible to write to database")
cursor = get_cursor()
try:
	cursor = connection.cursor()
	result  = cursor.execute( "INSERT INTO `ast_daily` (`create_date`, `hazardous`, `name`, `url`, `diam_min`, `diam_max`, `ts`, `dt_utc`, `dt_local`, `speed`, `distance`, `ast_id`) VALUES ('testDate', '0', 'testName', 'testURL', '10.5', '99.9', '1234567890', 'testDateUTC', 'testDateLocal', '1234567890', '1234567890', '12345')")
	connection.commit()
except Error as e :
	print('Problem inserting asteroid values into DB: ' + str(e))
	pass

assert cursor.fetchwarnings() == None
print("SUCCESS!!")
print("-----------")

#Check if it possible to write to databes with incorrect data types
print("Checking if it is possible to insert invalid data types into database")
cursor = get_cursor()
try:
	cursor = connection.cursor()
	result  = cursor.execute( "INSERT INTO `ast_daily` (`create_date`, `hazardous`, `name`, `url`, `diam_min`, `diam_max`, `ts`, `dt_utc`, `dt_local`, `speed`, `distance`, `ast_id`) VALUES ('10.5', 'yes', 'testName', 'testURL', 'yes', 'yes', '12.5', 'testDateUTC', 'testDateLocal', '123456789012', '1234567890.56', 'value')")
	connection.commit()
except Error as e :
	print('Problem inserting asteroid values into DB: ' + str(e))
	pass

assert cursor.fetchwarnings() != None
