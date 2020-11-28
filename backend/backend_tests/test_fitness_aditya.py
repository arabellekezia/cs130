import sys
sys.path.append("../")
import unittest
from db import DB
from user import User
from Fitness import Fitness
from datetime import datetime, date, timedelta

fitness_table_command = ("CREATE TABLE Fitness "
           "(WorkoutType varchar(256), Minutes INT NOT NULL, CaloriesBurned DOUBLE, "
           "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
           "REFERENCES Users(id));")

class TestFitness(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB('localhost', 'root', 'softwareengineering130', 'CS130_test')
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password)
        self.user_id = self.user.check_email_match(self.email)
        
        try:
            self.db.insert_data('Drop table Fitness')
        except:
            pass
        self.db.insert_data(fitness_table_command)
        
        self.fitness = Fitness(self.db, self.user_id)
        self.fitness_dict = {'WorkoutType': 'Running',\
                             'Minutes': 10,\
                             'CaloriesBurned': 100.9}
        self.fitness.insert_in_database(self.fitness_dict)
        
    def test_insert_in_database(self):
        """
        Test inserting an input in the database
        """
        self.assertTrue(self.fitness.insert_in_database(self.fitness_dict))

    def test_incorrect_key(self):
        """
        Test for incorrect keys. We send incorrect key: ItemS
        """
        print('Test Incorrect Key')
        d = {'WorkoutTypeS': 'Running',\
             'Minutes': 10,\
             'CaloriesBurned': 100.9}
        self.assertFalse(self.fitness.insert_in_database(d))
        d = {'WorkoutType': 'Running',\
             'MinutesS': 10,\
             'CaloriesBurned': 100.9}
        self.assertFalse(self.fitness.insert_in_database(d))
        d = {'WorkoutType': 'Running',\
             'Minutes': 10,\
             'CaloriesBurnedS': 100.9}
        self.assertFalse(self.fitness.insert_in_database(d))
        print("")
        
    def test_incorrect_value(self):
        """
        Test for incorrect value type.
        """
        print('Test Incorrect Value')
        d = {'WorkoutType': 1,\
             'Minutes': 10,\
             'CaloriesBurned': 100.9}
        self.assertFalse(self.fitness.insert_in_database(d))
        d = {'WorkoutType': 'Running',\
             'Minutes': 'Running',\
             'CaloriesBurned': 100.9}
        self.assertFalse(self.fitness.insert_in_database(d))
        d = {'WorkoutType': 'Running',\
             'Minutes': 10,\
             'CaloriesBurned': 100}
        self.assertFalse(self.fitness.insert_in_database(d))
        print("")
        
    def test_data_fetching(self):
        """
        Test fetching diet data from database
        """
        print('Fetched Result 1: Single Fetch')
        result, success = self.fitness.get_columns_given_range(date.today(), date.today()+timedelta(days=1))
        print(result)
        print("")
        self.assertTrue(success)
        
    def test_incorrect_data_fetching(self):
        """
        Test fetching diet data from database
        """
        print('Fetched Result 2: Incorrect Fetching')
        result, success = self.fitness.get_columns_given_range(date.today()+timedelta(days=10),date.today()+timedelta(days=11))
        print(result)
        print("")
        self.assertFalse(success)        
        
    def test_data_fetching_multiple(self):
        """
        Test fetching diet data from database
        """
        print('Fetched Result 3: Multiple Fetching')
        d = {'WorkoutType': 'Running',\
             'Minutes': 10,\
             'CaloriesBurned': 100.9}
        _ = self.fitness.insert_in_database_datetime(d, datetime.now()+timedelta(days=1))
        d = {'WorkoutType': 'Jogging',\
             'Minutes': 10,\
             'CaloriesBurned': 100.9}
        _ = self.fitness.insert_in_database_datetime(d, datetime.now()+timedelta(days=1)+timedelta(hours=2))
        d = {'WorkoutType': 'Dancing',\
             'Minutes': 10,\
             'CaloriesBurned': 100.9}
        _ = self.fitness.insert_in_database_datetime(d, datetime.now()+timedelta(days=1)+timedelta(hours=4))
        result, success = self.fitness.get_columns_given_range(date.today()+timedelta(days=1),date.today()+timedelta(days=2))
        print(result)
        print("")
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()