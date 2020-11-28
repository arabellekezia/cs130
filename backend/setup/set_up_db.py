from backend.db import DB

# users = ("CREATE TABLE Users (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
#          "email varchar(256) NOT NULL, password varchar(256) NOT NULL);")

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

db = DB()
#db.insert_data(users)
#db.insert_data(sleep)
#db.insert_data(diet)
#db.insert_data(fitness)
#db.insert_data(goals)
