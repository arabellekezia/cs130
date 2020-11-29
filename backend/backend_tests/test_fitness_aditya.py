import unittest
from backend.db import DB
from backend.user import User
from backend.Fitness import Fitness
from datetime import datetime, date, timedelta
import time

fitness_table_command = ("CREATE TABLE Fitness "
           "(WorkoutType varchar(256), Minutes INT NOT NULL, CaloriesBurned DOUBLE, "
           "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
           "REFERENCES Users(id));")

class TestFitness(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB()
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password)
        self.user_id = self.user.check_email_match(self.email)
        
#         try:
#             self.db.insert_data('Drop table Fitness')
#         except:
#             pass
#         self.db.insert_data(fitness_table_command)
        
        self.fitness = Fitness(self.db, self.user_id)
        self.fitness_dict = {'WorkoutType': 'Running',\
                             'Minutes': 10,\
                             'CaloriesBurned': 100.9}
#         self.fitness.insert_in_database(self.fitness_dict)
        
    def test_1_data_fetching_unix_time_and_insertion(self):
        """
        Test fetching diet data from database
        """
        print('Unix Time 1')
        dt1 = datetime.now()
        unix_time = round(time.time())
        self.assertTrue(self.fitness.insert_in_database_datetime(self.fitness_dict, dt1))
        print('Waiting ...')
        result, success = self.fitness.get_columns_given_range(dt1, dt1+timedelta(days=1))
        print(result)
        print("")
        self.assertTrue(success)
        self.assertEqual(result[0]['Datetime'],unix_time)
    
#     def test_insert_in_database(self):
#         """
#         Test inserting an input in the database
#         """
#         self.assertTrue(self.fitness.insert_in_database(self.fitness_dict))

    def test_2_incorrect_key(self):
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
        
    def test_3_incorrect_value(self):
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
        
    def test_4_data_fetching(self):
        """
        Test fetching diet data from database
        """
        print('Fetched Result 1: Single Fetch')
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.fitness.get_columns_given_range(dt1, dt1+timedelta(days=1))
        print(result)
        print("")
        self.assertTrue(success)
        
    def test_5_incorrect_data_fetching(self):
        """
        Test fetching diet data from database
        """
        print('Fetched Result 2: Incorrect Fetching')
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.fitness.get_columns_given_range(dt1+timedelta(days=10),dt1+timedelta(days=11))
        print(result)
        print("")
        self.assertFalse(success)        
        
    def test_6_data_fetching_multiple(self):
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
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.fitness.get_columns_given_range(dt1+timedelta(days=1),dt1+timedelta(days=2))
        print(result)
        print("")
        self.assertEqual(len(result), 3)
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()
