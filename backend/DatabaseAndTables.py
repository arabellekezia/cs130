import pymysql

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
 'Datetime' datetime) NOT NULL\
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
 'Datetime' datetime NOT NULL\
 'Barcode' bool NOT NULL\
 FOREIGN KEY ('UserID'))"
}

Tables['Fitness']={
"CREATE TABLES 'Fitness'(\
 'UserID' int(11) NOT NULL\
 'WorkoutType' varchar(256) NOT NULL\
 'Minutes' int(11) NOT NULL\
 'CaloriesBurned' float NOT NULL\
 'Datetime' datetime NOT NULL\
  FOREIGN_KEY ('UserID'))"
}

Tables['Goals']={
"CREATE TABLES 'Goals'(\
 'UserID' int(11) NOT NULL\
 'Value' float NOT NULL\
 'Type' varchar(1) NOT NULL\
 'Datetime' datetime NOT NULL\
 FOREIGN_KEY ('UserID'))"
}

host = 'localhost'
user = 'root'
password = ""
charSet = "utf8mb4"
cusrorType = pymysql.cursors.DictCursor
connection = pymysql.connect(host=host, user=user, password=password,charset=charSet,cursorclass=cusrorType)

try:
    cursor = connectionInstance.cursor()                                    
    sqlStatement = f"CREATE DATABASE {DB_NAME}"
    cursor.execute(sqlStatement)
except Exception as e:
    print("Exeception occured:{}".format(e))
finally:
    connection.close()

connection = pymysql.connect(host=host, user=user, password=password,charset=charSet,cursorclass=cusrorType, db=DB_NAME)
try:
    cursor = connectionInstance.cursor() 
    for table_name in Tables.keys():
        statement = Tables[table_name]
        cursor.execute(statement)
except Exception as e:
    print("Exeception occured:{}".format(e))
finally:
    connection.close()