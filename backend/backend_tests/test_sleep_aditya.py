import unittest
from backend.db import DB
from backend.user import User
from backend.Sleep_aditya import Sleep
from datetime import datetime, date, timedelta
import time

sleep_table_command = ("CREATE TABLE Sleep "
         "(Minutes INT NOT NULL, Nap BOOLEAN, SleepTime TIMESTAMP, WakeupTime TIMESTAMP, "
         "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
         "REFERENCES Users(id));")

class TestSleep(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB()
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password)
        self.user_id = self.user.check_email_match(self.email)
        
#         try:
#             self.db.insert_data('Drop table Sleep')
#         except:
#             pass
#         self.db.insert_data(sleep_table_command)
        
        self.sleep = Sleep(self.db, self.user_id)
        self.sleep_dict = {'Nap': False,\
                           'SleepTime': datetime.now(),\
                           'WakeupTime': datetime.now() + timedelta(hours=4) + timedelta(minutes=23)}
#         self.sleep.insert_in_database(self.sleep_dict)
        
    def test_1_data_fetching_unix_time_and_insertion(self):
        """
        Test fetching diet data from database
        """
        print('Unix Time 1')
        dt1 = datetime.now()
        unix_time = round(time.time())
        self.assertTrue(self.sleep.insert_in_database_datetime(self.sleep_dict, dt1))
        print('Waiting ...')
        result, success = self.sleep.get_columns_given_range(dt1, dt1+timedelta(days=1))
        print(result)
        print("")
        self.assertTrue(success)
        self.assertEqual(result[0]['Datetime'],unix_time)
        
#     def test_insert_in_database(self):
#         """
#         Test inserting an input in the database
#         """
#         self.assertTrue(self.sleep.insert_in_database(self.sleep_dict))

    def test_incorrect_key(self):
        """
        Test for incorrect keys. We send incorrect key: ItemS
        """
        print('Test Incorrect Key')
        d = {
           'NapS': False,\
           'SleepTime': datetime.now(),\
           'WakeupTime': datetime.now() + timedelta(hours=8)}
        self.assertFalse(self.sleep.insert_in_database(d))
        d = {
           'Nap': False,\
           'SleepTimeS': datetime.now(),\
           'WakeupTime': datetime.now() + timedelta(hours=8)}
        self.assertFalse(self.sleep.insert_in_database(d))
        d = {
           'Nap': False,\
           'SleepTime': datetime.now(),\
           'WakeupTimeS': datetime.now() + timedelta(hours=8)}
        self.assertFalse(self.sleep.insert_in_database(d))
        print("")
        
    def test_incorrect_value(self):
        """
        Test for incorrect value type.
        """
        print('Test Incorrect Value')
        d = {
             'Nap': 10,\
             'SleepTime': datetime.now(),\
             'WakeupTime': datetime.now() + timedelta(hours=8)}
        self.assertFalse(self.sleep.insert_in_database(d))
        d = {
             'Nap': False,\
             'SleepTime': 10,\
             'WakeupTime': datetime.now() + timedelta(hours=8)}
        self.assertFalse(self.sleep.insert_in_database(d))
        d = {
           'NapS': False,\
           'SleepTime': datetime.now(),\
           'WakeupTime': 10}
        self.assertFalse(self.sleep.insert_in_database(d))
        print("")
        
    def test_data_fetching(self):
        """
        Test fetching sleep data from database
        """
        print('Fetched Result 1: Single Fetch')
        result, success = self.sleep.get_columns_given_range(date.today(), date.today()+timedelta(days=1))
        print(result)
        print("")
        self.assertTrue(success)
        
    def test_minutes_computation(self):
        """
        Test the minute computation in sleep
        """
        print('Fetched Result 1: Single Fetch')
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.sleep.get_columns_given_range(dt1, dt1+timedelta(days=1))
        print(result)
        print("")
        self.assertTrue(success)
        self.assertTrue(result[0]['Minutes'],263)
        
    def test_incorrect_data_fetching(self):
        """
        Test fetching sleep data from database
        """
        print('Fetched Result 2: Incorrect Fetching')
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.sleep.get_columns_given_range(dt1+timedelta(days=10),dt1+timedelta(days=11))
        print(result)
        print("")
        self.assertFalse(success)        
        
    def test_data_fetching_multiple(self):
        """
        Test fetching sleep data from database
        """
        print('Fetched Result 3: Multiple Fetching')
        d = {
               'Nap': False,\
               'SleepTime': datetime.now() + timedelta(days=1),\
               'WakeupTime': datetime.now() + timedelta(days=1) + timedelta(hours=2) + timedelta(minutes=23)}
        _ = self.sleep.insert_in_database(d)
        d = {
               'Nap': False,\
               'SleepTime': datetime.now() + timedelta(days=1),\
               'WakeupTime': datetime.now() + timedelta(days=1) + timedelta(hours=4) + timedelta(minutes=23)}
        _ = self.sleep.insert_in_database(d)
        d = {
               'Nap': False,\
               'SleepTime': datetime.now() + timedelta(days=1),\
               'WakeupTime': datetime.now() + timedelta(days=1) + timedelta(hours=6) + timedelta(minutes=23)}
        _ = self.sleep.insert_in_database(d)
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.sleep.get_columns_given_range(dt1 + timedelta(days=1),dt1+timedelta(days=2))
        print(result)
        print("")
        self.assertTrue(success)
        self.assertEqual(len(result),3)

if __name__ == '__main__':
    unittest.main()
