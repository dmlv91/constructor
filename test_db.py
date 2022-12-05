import os
import requests
import mysql.connector

from datetime import datetime
from configparser import ConfigParser

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
cursor = get_cursor()
try:
	cursor = connection.cursor()
	result  = cursor.execute( "INSERT INTO `ast_daily` (`create_date`, `hazardous`, `name`, `url`, `diam_min`, `diam_max`, `ts`, `dt_utc`, `dt_local`, `speed`, `distance`, `ast_id`) VALUES ('testDate','testHazard', `testName`, `testUrl`, `testDiam_min`, `testDiam_max`, `testTs`, `testDt_utc`, `testDt_local`, `testSpeed`, `testDistance`, `testAst_id`)")
	connection.commit()
except Error as e :
	print('Problem inserting asteroid values into DB: ' + str(e))
	pass
assert cursor.fetchwarnings() == []
print("SUCCESS!!")
print("-----------")