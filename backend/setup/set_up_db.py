from backend.db import DB

users = ("CREATE TABLE Users (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
         "email varchar(256) NOT NULL, fullname varchar(256) NOT NULL, password BINARY(32) NOT NULL, salt BINARY(32) NOT NULL);")

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
           "(WorkoutType varchar(256), Minutes DOUBLE NOT NULL, CaloriesBurned DOUBLE NOT NULL, "
           "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
           "REFERENCES Users(id));")

goals = ("CREATE TABLE Goals "
         "(Type varchar(50), Value DOUBLE, "
         "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
         "REFERENCES Users(id));")

def set_up_db(db: DB) -> None:
    db.insert_data(users)
    db.insert_data(sleep)
    db.insert_data(diet)
    db.insert_data(fitness)
    db.insert_data(goals)

def drop_all_tables(db: DB) -> None:
    db.insert_data('drop table Sleep')
    db.insert_data('drop table Diet')
    db.insert_data('drop table Fitness')
    db.insert_data('drop table Goals')
    db.insert_data('drop table Users')


db = DB(False)
try:
    set_up_db(db)
    print("Production DB is set up.")
except:
    pass
