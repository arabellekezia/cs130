import sys
sys.path.append("../")
import unittest
from db import DB
from user import User
from datetime import datetime, date, timedelta
import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB('localhost', 'root', 'softwareengineering130', 'CS130_test')
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password)
        
    def test_create_new_user(self):
        """
        Test inserting an input in the database
        """
        email = f'{get_random_string(4)}@gmail.com'
        password = 'abcd'
        self.assertTrue(self.user.create_new_user(email,password))
        
    def test_user_already_exists(self):
        """
        Test inserting an input in the database
        """
        email = 'abc@gmail.com'
        password = 'defghi'
        self.assertFalse(self.user.create_new_user(email,password))
        
    def test_email_match(self):
        """
        Test inserting an input in the database
        """
        email = 'abc@gmail.com'
        password = 'defghi'
        self.assertTrue(isinstance(self.user.check_email_match(email),int))
        
    def test_incorrect_email_match(self):
        """
        Test inserting an input in the database
        """
        email = 'pqr@gmail.com'
        password = 'defghi'
        self.assertEqual(self.user.check_email_match(email),-1)
        
    def test_password_match(self):
        """
        Test inserting an input in the database
        """
        email = 'abc@gmail.com'
        password = 'defghi'
        self.assertTrue(isinstance(self.user.check_password_match(email,password),int))
        
    def test_incorrect_password_match(self):
        """
        Test inserting an input in the database
        """
        email = 'abc@gmail.com'
        password = 'xyz'
        self.assertEqual(self.user.check_password_match(email,password),-1)
        

if __name__ == '__main__':
    unittest.main()