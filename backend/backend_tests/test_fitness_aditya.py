import unittest
from backend.db import DB
from backend.user import User
from backend.Fitness import Fitness
from datetime import datetime, date, timedelta
import time


class TestFitness(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB()
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        self.fullname = 'ABC'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password, self.fullname)
        self.user_id = self.user.check_email_match(self.email)

        self.fitness = Fitness(self.db, self.user_id)
        self.fitness_dict = {'WorkoutType': 'Running',\
                             'Minutes': 10,\
                             'CaloriesBurned': 100.9}
        self.dt1 = datetime.now()
        self.unix_time = round(time.time())

    def test_0_data_insertion(self):
        s = self.fitness.insert_in_database_datetime(self.fitness_dict, self.dt1)
        self.assertTrue(s)
        
    def test_1_data_fetching_unix_time_and_insertion(self):
        """
        Test fetching fitness data from database
        """
        result, success = self.fitness.get_columns_given_range(self.dt1, self.dt1+timedelta(days=1))

        self.assertTrue(success)
        self.assertEqual(result[0]['Datetime'],self.unix_time)


    def test_2_incorrect_key(self):
        """
        Test for incorrect keys. We send incorrect key: ItemS
        """
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
        
    def test_3_incorrect_value(self):
        """
        Test for incorrect value type.
        """
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
        
    def test_4_data_fetching(self):
        """
        Test fetching diet data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.fitness.get_columns_given_range(dt1, dt1+timedelta(days=1))
        self.assertTrue(success)
        
    def test_5_data_fetching_values(self):
        """
        Test fetching diet data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.fitness.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success)
        self.assertEqual(result[0]['WorkoutType'], 'Running')
        self.assertEqual(result[0]['Minutes'], 10)
        self.assertEqual(result[0]['CaloriesBurned'], 100.9)

    def test_6_incorrect_data_fetching(self):
        """
        Test fetching diet data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.fitness.get_columns_given_range(dt1+timedelta(days=10),dt1+timedelta(days=11))
        self.assertFalse(success)        
        
    def test_7_data_fetching_multiple(self):
        """
        Test fetching diet data from database
        """
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

        self.assertEqual(len(result), 3)
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()
