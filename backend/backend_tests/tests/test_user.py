import unittest
from datetime import datetime, date, timedelta
import random
import string
from backend.db import DB 
from backend.user import User

def get_random_string(length: int) -> str:
    """
    Generates a random string of length 'length'
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

class TestUser(unittest.TestCase):
    """
    Tests for user.py
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
        
    def test_create_new_user(self):
        """
        Test inserting an input in the database
        """
        email = f'{get_random_string(4)}@gmail.com'
        password = 'abcd'
        fullname = 'ABCD'
        self.assertTrue(self.user.create_new_user(email,password,fullname))
        
    def test_user_already_exists(self):
        """
        Test inserting an input in the database
        """
        email = 'abc@gmail.com'
        password = 'defghi'
        fullname = 'ABCD'
        self.assertFalse(self.user.create_new_user(email,password,fullname))
        
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
        
        user = User(None)
        email = 'abc@gmail.com'
        password = 'defghi'
        self.assertEqual(self.user.check_password_match(None,None),-1)
        
    def test_incorrect_password_match(self):
        """
        Test inserting an input in the database
        """
        email = 'abc@gmail.com'
        password = 'xyz'
        self.assertEqual(self.user.check_password_match(email,password),-1)
        
    def test_token(self):
        """
        Test the encoding and decoding token functions.
        """
        num = 10
        token, code = self.user.encode_token(num)
        dec_num, dec_code = self.user.decode_token(token)
        self.assertEqual(num, dec_num)

if __name__ == '__main__':
    unittest.main()
