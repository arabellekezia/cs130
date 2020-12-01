import unittest
from datetime import datetime
from backend.db import DB
from backend.user import User
from backend.Sleep import Sleep

class SleepTest(unittest.TestCase):

    def setUpClass(self):
        self.db = DB()

        # Create User 1
        self.fullname1 = "User 1"
        self.email1 = "user1@gmail.com"
        self.password1 = "123456789"

        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password, self.fullname)
        self.user_id1 = self.user.check_email_match(self.email)

        # Create User 2
        self.fullname2 = "User 2"
        self.email2 = "user2@gmail.com"
        self.password2 = "987654321"

        self.user.create_new_user(self.email2, self.password2, self.fullname2)
        self.user_id2 = self.user.check_email_match(self.email)

        self.sleep1 = Sleep(self.db, self.user_id1)
        self.sleep2 = Sleep(self.db, self.user_id2)

    def test_insert_one_user(self):
        sleep_time = datetime.utcnow() - timedelta(hours=8)
        wakeup_time = datetime.utcnow()
        dict = {'SleepTime': sleep_time, 'WakeupTime': wakeup_time}
        self.assertTrue(self.sleep1.insert_in_database(dict))

    def test_duration_calc(self):
        now = datetime.utcnow()
        data = self.sleep1.get_columns_given_range((now-timedelta(days=1), now))
        self.assertEqual(data[0]['Minutes'], 447)

    def test_insert_mult_users(self):
        sleep_time1 = datetime.utcnow() - timedelta(hours=6)
        sleep_time2 = datetime.utcnow() - timedelta(hours=5) - timedelta(minutes=30)
        wakeup_time = datetime.utcnow()
        dict1 = {'SleepTime': sleep_time1, 'WakeupTime': wakeup_time}
        dict2 = {'SleepTime': sleep_time2, 'WakeupTime': wakeup_time}
        self.assertTrue(self.sleep1.insert_in_database(dict1))
        self.assertTrue(self.sleep2.insert_in_database(dict2))

    def insert_wrong_data(self):
        sleep_time = datetime.utcnow() - timedelta(hours=8)
        wakeup_time = datetime.utcnow()
        dict1 = {}
        dict2 = {'Time': sleep_time, 'WakeupTime': wakeup_time}
        dict3 = {'WakeupTime': wakeup_time}
        self.assertFalse(self.sleep1.insert_in_database(dict1))
        self.assertFalse(self.sleep1.insert_in_database(dict2))
        self.assertFalse(self.sleep1.insert_in_database(dict3))

    def get_one_user_data(self):
        startDate = datetime.utcnow() - timedelta(days=2)
        endDate = datetime.utcnow()

        res1 = self.sleep1.get_columns_given_range(startDate, endDate)
        self.assertTrue(res1)
        self.assertEqual(len(res1), 2)

        res2 = self.sleep1.get_columns_given_range(startDate, endDate)
        self.assertTrue(res2)
        self.assertEqual(len(res2), 1)

if __name__ == '__main__':
    unittest.main()
