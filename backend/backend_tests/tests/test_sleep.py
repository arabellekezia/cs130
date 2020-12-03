import unittest
from backend.db import DB
from backend.user import User
from backend.Sleep import Sleep
from datetime import datetime, date, timedelta, timezone
import time
import copy

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
                
        self.email_1 = 'xyz@gmail.com' 
        self.password_1 = 'klmno'
        self.fullname_1 = 'XYZ'
        
        self.user_1 = User(self.db)
        self.user_1.create_new_user(self.email_1, self.password_1, self.fullname_1)
        self.user_id_1 = self.user_1.check_email_match(self.email_1)

        self.sleep = Sleep(self.db, self.user_id)
        self.sleep_1 = Sleep(self.db, self.user_id_1)
        
        self.sleep_time = datetime.utcnow()
        self.wakeup_time = datetime.utcnow() + timedelta(hours=1) + timedelta(minutes=3)
        self.sleep_dict = {'Nap': False,\
                           'SleepTime': self.sleep_time,\
                           'WakeupTime': self.wakeup_time}
        
        self.sleep_time_1 = datetime.utcnow() + timedelta(hours=1)
        self.wakeup_time_1 = datetime.utcnow() + timedelta(hours=2) + timedelta(minutes=3)
        self.sleep_dict_1 = {'Nap': False,\
                           'SleepTime': self.sleep_time_1,\
                           'WakeupTime': self.wakeup_time_1}
        
        self.dt1 = datetime.utcnow()
        self.unix_time = round(time.time())

    def test_0_data_insertion(self):
        s = self.sleep.insert_in_database(self.sleep_dict, date_time=self.dt1)
        self.assertTrue(s)
        
    def test_1_data_insertion_multiple_user(self):
        s = self.sleep.insert_in_database(self.sleep_dict, date_time=self.dt1)
        self.assertTrue(s)
        s_1 = self.sleep_1.insert_in_database(self.sleep_dict_1, date_time=self.dt1)
        self.assertTrue(s_1)

    def test_2_incorrect_key(self):
        """
        Test for incorrect keys. We send incorrect key: ItemS
        """
        d = copy.deepcopy(self.sleep_dict)
        del(d['Nap'])
        d['NapS'] = False
        self.assertFalse(self.sleep.insert_in_database(d))
        
        d = copy.deepcopy(self.sleep_dict)
        del(d['SleepTime'])
        d['SleepTimeS'] = datetime.utcnow()
        self.assertFalse(self.sleep.insert_in_database(d))

        d = copy.deepcopy(self.sleep_dict)
        del(d['WakeupTime'])
        d['WakeupTimeS'] = datetime.utcnow()
        self.assertFalse(self.sleep.insert_in_database(d))
        
    def test_3_incorrect_value(self):
        """
        Test for incorrect value type.
        """
        d = copy.deepcopy(self.sleep_dict)
        d['Nap'] = 10
        self.assertFalse(self.sleep.insert_in_database(d))
        
        d = copy.deepcopy(self.sleep_dict)
        d['SleepTime'] = 10
        self.assertFalse(self.sleep.insert_in_database(d))

        d = copy.deepcopy(self.sleep_dict)
        d['WakeupTime'] = 10
        self.assertFalse(self.sleep.insert_in_database(d))
       
    def test_4_data_fetching_unix_time_and_insertion(self):
        """
        Test fetching sleep data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.sleep.get_columns_given_range(dt1, dt1+timedelta(days=1))
        self.assertTrue(success)
        self.assertEqual(result[0]['Datetime'],self.unix_time)

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
        
        result_1, success_1 = self.sleep_1.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success_1)
        self.assertEqual(result_1[0]['SleepTime'],round(self.sleep_time_1.replace(tzinfo=timezone.utc).timestamp()))
        self.assertEqual(result_1[0]['WakeupTime'],round(self.wakeup_time_1.replace(tzinfo=timezone.utc).timestamp()))
        self.assertFalse(result_1[0]['Nap'])
        self.assertTrue(result_1[0]['Minutes'],263)

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