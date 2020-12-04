import unittest
from backend.db import DB
from backend.user import User
from backend.Fitness import Fitness
from datetime import datetime, date, timedelta
import time
import copy

class TestFitness(unittest.TestCase):
    """
    Tests for Fitness.py
    """

    @classmethod
    def setUpClass(self):
        """
        Set up the unit test.
        """
        self.db = DB()
        
        self.email = 'abc@gmail.com' 
        self.password = 'defghi'
        self.fullname = 'ABC'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password, self.fullname)
        self.user_id = self.user.check_email_match(self.email)
                
        self.email_1 = 'xyz@gmail.com' 
        self.password_1 = 'klmno'
        self.fullname_1 = 'XYZ'
        
        self.user_1 = User(self.db)
        self.user_1.create_new_user(self.email_1, self.password_1, self.fullname_1)
        self.user_id_1 = self.user_1.check_email_match(self.email_1)

        self.fitness = Fitness(self.db, self.user_id)
        self.fitness_dict = {'WorkoutType': 'Running',\
                             'Minutes': 10.0,\
                             'CaloriesBurned': 100.9}
        self.fitness_1 = Fitness(self.db, self.user_id_1)
        self.fitness_dict_1 = {'WorkoutType': 'Sleeping',\
                             'Minutes': 100.0,\
                             'CaloriesBurned': 10.9}
        
        self.dt1 = datetime.utcnow()
        self.unix_time = round(time.time())

    def test_0_data_insertion(self):
        """
        Test database insertion for a single user.
        """
        s = self.fitness.insert_in_database(self.fitness_dict, date_time=self.dt1)
        self.assertTrue(s)
        
    def test_1_data_insertion_multiple_users(self):
        """
        Test database insertion for multiple users.
        """
        s = self.fitness.insert_in_database(self.fitness_dict, date_time=self.dt1)
        self.assertEqual(s, True)
        s_1 = self.fitness_1.insert_in_database(self.fitness_dict_1, date_time=self.dt1)
        self.assertEqual(s_1, True)
        
    def test_2_incorrect_key(self):
        """
        Test for incorrect keys. The input keys are the columns of the fitness table.
        """
        d = copy.deepcopy(self.fitness_dict)
        del(d['WorkoutType'])
        d['WorkoutTypeS'] = 'Running'
        self.assertFalse(self.fitness.insert_in_database(d))

        d = copy.deepcopy(self.fitness_dict)
        del(d['Minutes'])
        d['MinutesS'] = 10.0
        self.assertFalse(self.fitness.insert_in_database(d))

        d = copy.deepcopy(self.fitness_dict)
        del(d['CaloriesBurned'])
        d['CaloriesBurnedS'] = 100.9
        self.assertFalse(self.fitness.insert_in_database(d))
        
    def test_3_incorrect_value(self):
        """
        Test for incorrect value data type before inserting in the fitness database.
        """
        d = copy.deepcopy(self.fitness_dict)
        d['WorkoutType'] = 1
        self.assertFalse(self.fitness.insert_in_database(d))

        d = copy.deepcopy(self.fitness_dict)
        d['Minutes'] = 'Running'
        self.assertFalse(self.fitness.insert_in_database(d))

        d = copy.deepcopy(self.fitness_dict)
        d['CaloriesBurned'] = 1
        self.assertFalse(self.fitness.insert_in_database(d))
       
    def test_4_data_fetching_unix_time_and_insertion(self): 
        """
        Test fetching fitness data from database and also check if the UNIX TIMESTAMP is correct.
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.fitness.get_columns_given_range(dt1, dt1+timedelta(days=1))
        self.assertTrue(success)
        self.assertEqual(result[0]['Datetime'],self.unix_time)
                    
    def test_6_data_fetching_values_multiple_users(self):
        """
        Test fetching fitness data from database for multiple users.
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.fitness.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success)
        self.assertEqual(result[0]['WorkoutType'], 'Running')
        self.assertEqual(result[0]['Minutes'], 10.0)
        self.assertEqual(result[0]['CaloriesBurned'], 100.9)
        
        result_1, success_1 = self.fitness_1.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success_1)
        self.assertEqual(result_1[0]['WorkoutType'], 'Sleeping')
        self.assertEqual(result_1[0]['Minutes'], 100.0)
        self.assertEqual(result_1[0]['CaloriesBurned'], 10.9)

    def test_7_incorrect_data_fetching(self):
        """
        Test fetching fitness from the database for incorrect date range. The function should return False. 
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.fitness.get_columns_given_range(dt1+timedelta(days=10),dt1+timedelta(days=11))
        self.assertFalse(success)        
        
    def test_8_data_fetching_multiple(self):
        """
        Test fetching multiple fitness data entries from the database.
        """
        d = {'WorkoutType': 'Running',\
             'Minutes': 10.0,\
             'CaloriesBurned': 100.9}
        _ = self.fitness.insert_in_database(d, date_time=datetime.utcnow()+timedelta(days=1)+timedelta(minutes=1))
        d = {'WorkoutType': 'Jogging',\
             'Minutes': 10.0,\
             'CaloriesBurned': 100.9}
        _ = self.fitness.insert_in_database(d, date_time=datetime.utcnow()+timedelta(days=1)+timedelta(minutes=2))
        d = {'WorkoutType': 'Dancing',\
             'Minutes': 10.0,\
             'CaloriesBurned': 100.9}
        _ = self.fitness.insert_in_database(d, date_time=datetime.utcnow()+timedelta(days=1)+timedelta(minutes=4))
        d1 = date.today() + timedelta(days=1)
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.fitness.get_columns_given_range(dt1,dt1+timedelta(days=1))

        self.assertEqual(len(result), 3)
        self.assertTrue(success)
        self.assertEqual(result[0]['WorkoutType'],'Running')
        self.assertEqual(result[1]['WorkoutType'],'Jogging')
        self.assertEqual(result[2]['WorkoutType'],'Dancing')
        
    def test_9_incorrect_database(self):
        """
        Test database insertion for a single user with incorrect database. Test case to increase the coverage. 
        """
        fitness = Fitness(None, self.user_id_1)
        s = fitness.insert_in_database(self.fitness_dict, date_time=self.dt1)
        self.assertFalse(s)
        
if __name__ == '__main__':
    unittest.main()
