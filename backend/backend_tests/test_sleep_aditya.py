import unittest
from backend.db import DB
from backend.user import User
from backend.Sleep_aditya import Sleep
from datetime import datetime, date, timedelta, timezone
import time

class TestSleep(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB()
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        self.fullname = 'ABC' 
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password, self.fullname)
        self.user_id = self.user.check_email_match(self.email)

        self.sleep = Sleep(self.db, self.user_id)
        self.sleep_time = datetime.utcnow()
        self.wakeup_time = datetime.utcnow() + timedelta(hours=1) + timedelta(minutes=3)
        self.sleep_dict = {'Nap': False,\
                           'SleepTime': self.sleep_time,\
                           'WakeupTime': self.wakeup_time}
        self.dt1 = datetime.utcnow()
        self.unix_time = round(time.time())

    def test_0_data_insertion(self):
        s = self.sleep.insert_in_database_datetime(self.sleep_dict, self.dt1)
        self.assertTrue(s)
        
    def test_3_5_data_fetching_unix_time_and_insertion(self):
        """
        Test fetching sleep data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.sleep.get_columns_given_range(dt1, dt1+timedelta(days=1))
        self.assertTrue(success)
        self.assertEqual(result[0]['Datetime'],self.unix_time)

    def test_2_incorrect_key(self):
        """
        Test for incorrect keys. We send incorrect key: ItemS
        """
        d = {
           'NapS': False,\
           'SleepTime': datetime.utcnow(),\
           'WakeupTime': datetime.utcnow() + timedelta(hours=1)}
        self.assertFalse(self.sleep.insert_in_database(d))
        d = {
           'Nap': False,\
           'SleepTimeS': datetime.utcnow(),\
           'WakeupTime': datetime.now() + timedelta(hours=1)}
        self.assertFalse(self.sleep.insert_in_database(d))
        d = {
           'Nap': False,\
           'SleepTime': datetime.now(),\
           'WakeupTimeS': datetime.utcnow() + timedelta(hours=1)}
        self.assertFalse(self.sleep.insert_in_database(d))
        
    def test_3_incorrect_value(self):
        """
        Test for incorrect value type.
        """
        d = {
             'Nap': 10,\
             'SleepTime': datetime.utcnow(),\
             'WakeupTime': datetime.utcnow() + timedelta(hours=1)}
        self.assertFalse(self.sleep.insert_in_database(d))
        d = {
             'Nap': False,\
             'SleepTime': 10,\
             'WakeupTime': datetime.utcnow() + timedelta(hours=1)}
        self.assertFalse(self.sleep.insert_in_database(d))
        d = {
           'NapS': False,\
           'SleepTime': datetime.utcnow(),\
           'WakeupTime': 10}
        self.assertFalse(self.sleep.insert_in_database(d))
        
    def test_4_data_fetching(self):
        """
        Test fetching sleep data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.sleep.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success)

    def test_4_data_fetching_value(self):
        """
        Test fetching sleep data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.sleep.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success)
        self.assertEqual(result[0]['SleepTime'],round(self.sleep_time.replace(tzinfo=timezone.utc).timestamp()))
        self.assertEqual(result[0]['WakeupTime'],round(self.wakeup_time.replace(tzinfo=timezone.utc).timestamp()))
        self.assertFalse(result[0]['Nap'])
        self.assertTrue(result[0]['Minutes'],263)

    def test_5_minutes_computation(self):
        """
        Test the minute computation in sleep
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.sleep.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success)
        self.assertTrue(result[0]['Minutes'],263)
        
    def test_6_incorrect_data_fetching(self):
        """
        Test fetching sleep data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.sleep.get_columns_given_range(dt1+timedelta(days=10),dt1+timedelta(days=11))

        self.assertFalse(success)        
        
    def test_7_data_fetching_multiple(self):
        """
        Test fetching sleep data from database
        """
        d = {
               'Nap': False,\
               'SleepTime': datetime.utcnow() + timedelta(days=1),\
               'WakeupTime': datetime.utcnow() + timedelta(days=1) + timedelta(hours=1) + timedelta(minutes=23)}
        _ = self.sleep.insert_in_database(d)
        d = {
               'Nap': False,\
               'SleepTime': datetime.utcnow() + timedelta(days=1),\
               'WakeupTime': datetime.utcnow() + timedelta(days=1) + timedelta(hours=1) + timedelta(minutes=30)}
        _ = self.sleep.insert_in_database(d)
        d = {
               'Nap': False,\
               'SleepTime': datetime.utcnow() + timedelta(days=1),\
               'WakeupTime': datetime.utcnow() + timedelta(days=1) + timedelta(hours=1) + timedelta(minutes=35)}
        _ = self.sleep.insert_in_database(d)
        d1 = date.today() + timedelta(days=1)
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.sleep.get_columns_given_range(dt1,dt1+timedelta(days=1))

        self.assertTrue(success)
        self.assertEqual(len(result),3)

if __name__ == '__main__':
    unittest.main()
