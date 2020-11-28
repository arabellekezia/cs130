users = ("CREATE TABLE Users (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
         "email varchar(256) NOT NULL, password BINARY(32) NOT NULL, salt BINARY(32) NOT NULL);")

sleep = ("CREATE TABLE Sleep "
         "(Minutes INT NOT NULL, Nap BOOLEAN, SleepTime TIMESTAMP, WakeupTime TIMESTAMP, "
         "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
         "REFERENCES Users(id));")

diet = ("CREATE TABLE Diet "
        "(Item varchar(300) NOT NULL, ServingSize DOUBLE, Cals DOUBLE, Protein DOUBLE, Carbs DOUBLE, "
        "Fat DOUBLE, Fiber DOUBLE, Barcode BOOLEAN, " 
        "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
        "REFERENCES Users(id));")

fitness = ("CREATE TABLE Fitness "
           "(WorkoutType varchar(256), Minutes INT NOT NULL, CaloriesBurned DOUBLE, "
           "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
           "REFERENCES Users(id));")

goals = ("CREATE TABLE Goals "
         "(Type varchar(50), Value DOUBLE, "
         "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
         "REFERENCES Users(id));")

import mysql.connector as mysql

class Database:
    def __init__(self, host, user, passwd, db_name):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__database_name = db_name
    
    def __connect_MySQL(self):
         return mysql.connect(host=self.__host, \
                           user=self.__user, \
                           passwd=self.__passwd)
    
    def __get_Database(self):
        return mysql.connect(host=self.__host,\
                           user=self.__user,\
                           passwd=self.__passwd,\
                           database=self.__database_name)
        
    def __close_connection(self, connection):
        connection.close()
        
    def __get_Cursor(self, database):
        if database is not None:
            return database.cursor()
        else:
            raise ValueError("Database does not exist")

    def create_Database(self):
        try:
            my_sql = self.__connect_MySQL()
            c = self.__get_Cursor(my_sql)
            c.execute(f"CREATE DATABASE {self.__database_name}")
            self.__close_connection(my_sql)
        except:
            print('Database already exists')
        
    def delete_Database(self):
        try:
            my_sql = self.__connect_MySQL()
            c = self.__get_Cursor(my_sql)
            c.execute(f'DROP DATABASE {self.__database_name}')
        except:
            print('Database did not exist')
    
    def create_Table(self, table_command):
        database = self.__get_Database()
        c = self.__get_Cursor(database)
        try:
            c.execute(table_command)
            print('Table Created')
            self.__close_connection(database)
        except:
            print('Table already created')
        
    def delete_Table(self, name):
        database = self.__get_Database()
        c = self.__get_Cursor(database)
        try:
            c.execute(f"DROP TABLE {name}")
            self.__close_connection(database)
        except:
            print('Table did not exist')
        
    def show_Databases(self):
        my_sql = self.__connect_MySQL()
        c = self.__get_Cursor(my_sql)
        c.execute("SHOW DATABASES")
        databases = c.fetchall()
        for d in databases:
            print(d)
        self.__close_connection(my_sql)
            
    def show_Tables(self):
        database = self.__get_Database()
        c = self.__get_Cursor(database)
        c.execute("SHOW TABLES")
        tables = c.fetchall()
        for t in tables:
            print(t)
        self.__close_connection(database)
            
    def show_Table(self, name):
        database = self.__get_Database()
        c = self.__get_Cursor(database)
        c.execute(f"DESC {name}")
        print(c.fetchall())
        self.__close_connection(database)

db = Database('localhost', 'root', 'softwareengineering130', 'CS130_test')

db.create_Database()

db.create_Table(users)
db.create_Table(sleep)
db.create_Table(diet)
db.create_Table(fitness)
db.create_Table(goals)

# db.delete_Database()