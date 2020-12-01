import unittest
from datetime import datetime
from backend.db import DB
from backend.user import User
from backend.Fitness import Fitness

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

        self.fit1 = Fitness(self.db, self.user_id1)
        self.fit2 = Fitness(self.db, self.user_id2)

    def test_insert_one_user(self):
        dict = {'WorkoutType': 'Basketball', 'Minutes': 50, 'CaloriesBurned': 327.9}
        self.assertTrue(self.fit1.insert_in_database(dict))

    def test_insert_mult_users(self):
        dict1 = {'WorkoutType': 'Running', 'Minutes': 70, 'CaloriesBurned': 453.3}
        dict2 = {'WorkoutType': 'Lift', 'Minutes': 45, 'CaloriesBurned': 87.6}
        self.assertTrue(self.fit1.insert_in_database(dict1))
        self.assertTrue(self.fit2.insert_in_database(dict2))

    def insert_wrong_data(self):
        dict1 = {}
        dict2 = {'WorkoutType': 'Lift', 'Minutes': '45', 'CaloriesBurned': 87.6}
        dict3 = {'Minutes': 45, 'CaloriesBurned': 87.6}
        dict2 = {'WorkoutType': 'Lift', 'Minutes': 40.9, 'CaloriesBurned': 80}
        self.assertFalse(self.sleep1.insert_in_database(dict1))
        self.assertFalse(self.sleep1.insert_in_database(dict2))
        self.assertFalse(self.sleep1.insert_in_database(dict3))

    def test_get_data(self):
        res1 = self.fit1.get_columns_given_range(startDate, endDate)
        self.assertTrue(res1)
        self.assertEqual(len(res1), 2)

        res2 = self.fit2.get_columns_given_range(startDate, endDate)
        self.assertTrue(res2)
        self.assertEqual(len(res2), 1)

if __name__ == '__main__':
    unittest.main()
