import mysql.connector

DB_NAME = 'BetterYou'

Tables = {}

Tables['Users']={
"CREATE TABLE 'Users' (\
 'id' int(11) NOT NULL AUTO_INCREMENT\
 'email' varchar(256) NOT NULL\
 'password' varchar(256) NOT NULL\
  PRIMARY KEY ('id'))"
}

Tables['Sleep']={
"CREATE TABLE 'Sleep' (\
 'UserID' int(11) NOT NULL\
 'Minutes' int(11) NOT NULL\
 'Nap' bool NOT NULL\
 'SleepTime' datetime NOT NULL\
 'WakeupTime' datetime NOT NULL\
 'Datetime' datetime) NOT NULL CURRENT_TIMESTAMP\
 FOREIGN KEY('UserID')"
}

Tables['Diet']={
"CREATE TABLE 'Diet'(\
 'UserID' int(11) NOT NULL\
 'Item' varchar(256) NOT NULL\
 'ServingSize' float NOT NULL\
 'Cals' float NOT NULL\
 'Fat' float NOT NULL\
 'Fiber' float NOT NULL\
 'Protein' float NOT NULL\
 'Carbs' float NOT NULL\
 'Datetime' datetime NOT NULL CURRENT_TIMESTAMP\
 'Barcode' bool NOT NULL\
 FOREIGN KEY ('UserID'))"
}

Tables['Fitness']={
"CREATE TABLES 'Fitness'(\
 'UserID' int(11) NOT NULL\
 'WorkoutType' varchar(256) NOT NULL\
 'Minutes' int(11) NOT NULL\
 'CaloriesBurned' float NOT NULL\
 'Datetime' datetime NOT NULL CURRENT_TIMESTAMP\
  FOREIGN_KEY ('UserID'))"
}

Tables['Goals']={
"CREATE TABLES 'Goals'(\
 'UserID' int(11) NOT NULL\
 'Value' float NOT NULL\
 'Type' varchar(1) NOT NULL\
 'Datetime' datetime NOT NULL CURRENT_TIMESTAMP\
 FOREIGN_KEY ('UserID'))"
}

host = 'localhost'
user = 'root'
password = "bootipul"
charSet = "utf8mb4"
# cusrorType = pymysql.cursors.DictCursor
connection = mysql.connector.connect(host=host, user=user, password=password,charset=charSet)
# connection = pymysql.connect(host=host, user=user, password=password,charset=charSet,cursorclass=cusrorType)

try:
    cursor = connection.cursor()
    sqlStatement = f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
    cursor.execute(sqlStatement)
    for table_name in Tables.keys():
        statement = Tables[table_name]
        cursor.execute(statement)

except Exception as e:
    print("Exeception occured:{}".format(e))
else:
    connection.close()

# connection = mysql.connector.connect(host=host, user=user, password=password,charset=charSet, db=DB_NAME)
# try:
#     cursor = connection.cursor()
#     for table_name in Tables.keys():
#         statement = Tables[table_name]
#         cursor.execute(statement)
# except Exception as e:
#     print("Exeception occured:{}".format(e))
# finally:
#     connection.close()
