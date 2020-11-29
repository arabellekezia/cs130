import unittest
from backend.db import DB
from backend.user import User
from backend.Diet import Diet
from datetime import datetime, date, timedelta
import time

class TestDiet(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB()
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        self.fullname = 'ABC'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password, self.fullname)
        self.user_id = self.user.check_email_match(self.email)
        
        self.diet = Diet(self.db, self.user_id)
        self.diet_dict = {'Item': 'Apple',\
                         'ServingSize': 1.0,\
                         'Barcode': False,\
                         'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.dt1 = datetime.now()
        self.unix_time = round(time.time())
        
    def test_0_data_insertion(self):
        """
        Test fetching diet data from database
        """
        s = self.diet.insert_in_database_datetime(self.diet_dict, self.dt1)
        self.assertEqual(s, True) 
    
    def test_1_data_fetching_unix_time_and_insertion(self):
        """
        Test fetching diet data from database
        """
        result, success = self.diet.get_columns_given_range(self.dt1, self.dt1+timedelta(days=1))

        self.assertTrue(success)
        self.assertEqual(result[0]['Datetime'],self.unix_time)


    def test_3_incorrect_key(self):
        """
        Test for incorrect keys. We send incorrect key: ItemS
        """
        d = {'ItemS': 'Apple',\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                 'ServingSizeS': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                 'ServingSize': 1.0,\
                 'BarcodeS': False,\
                 'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dictS': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        
    def test_4_incorrect_key_1(self):
        """
        Test for incorrect keys. We send incorrect key: CalsS
        """
        d = {'Item': 'Apple',\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'CalsS': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'Cals': 100.0,'ProteinS': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'CarbsS': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'FatS': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'FatS': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'FiberS': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        
        
    def test_5_incorrect_value(self):
        """
        Test for incorrect value type.
        """
        d = {'Item': 1,\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                 'ServingSize': 'Apple',\
                 'Barcode': False,\
                 'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
             'ServingSize': 1.0,\
             'Barcode': 'Apple',\
             'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))

    def test_6_incorrect_value_1(self):
        """
        Test for incorrect value type.
        """
        d = {'Item': 'Apple',\
                 'ServingSize': 1.0,\
                 'Barcode': False,\
                 'nutri_dict': {'CalsS': 'Apple','Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                     'ServingSize': 1.0,\
                     'Barcode': False,\
                     'nutri_dict': {'Cals': 100.0,'Protein': 'Apple', 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                     'ServingSize': 1.0,\
                     'Barcode': False,\
                     'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 'Apple', 'Fat': 100.0, 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                     'ServingSize': 1.0,\
                     'Barcode': False,\
                     'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 'Apple', 'Fiber': 100.0}}
        self.assertFalse(self.diet.insert_in_database(d))
        d = {'Item': 'Apple',\
                     'ServingSize': 1.0,\
                     'Barcode': False,\
                     'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 'Apple'}}
        self.assertFalse(self.diet.insert_in_database(d))

        
    def test_7_data_fetching(self):
        """
        Test fetching diet data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.diet.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success)
        
        self.diet_dict = {'Item': 'Apple',\
                         'ServingSize': 1.0,\
                         'Barcode': False,\
                         'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        
    def test_8_data_fetching_values(self):
        """
        Test fetching diet data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.diet.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success)
        self.assertEqual(result[0]['Item'], 'Apple')
        self.assertEqual(result[0]['ServingSize'], 1.0)
        self.assertEqual(result[0]['Cals'], 100.0)
        self.assertEqual(result[0]['Fiber'], 100.0)
        self.assertEqual(result[0]['Carbs'], 100.0)
        self.assertEqual(result[0]['Fat'], 100.0)
        self.assertEqual(result[0]['Protein'], 100.0)
        self.assertFalse(result[0]['Barcode'])
        
    def test_9_incorrect_data_fetching(self):
        """
        Test fetching diet data from database
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.diet.get_columns_given_range(dt1+timedelta(days=10),dt1+timedelta(days=11))

        self.assertFalse(success)
        
        
    def test_9_data_fetching_multiple(self):
        """
        Test fetching diet data from database
        """
        d = {'Item': 'Apple',\
             'ServingSize': 1.0,\
             'Barcode': False,\
             'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        _ = self.diet.insert_in_database_datetime(d, datetime.now()+timedelta(days=1))
        d = {'Item': 'Orange',\
             'ServingSize': 1.0,\
             'Barcode': False,\
             'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        _ = self.diet.insert_in_database_datetime(d, datetime.now()+timedelta(days=1)+timedelta(hours=2))
        d = {'Item': 'Banana',\
             'ServingSize': 1.0,\
             'Barcode': False,\
             'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        _ = self.diet.insert_in_database_datetime(d, datetime.now()+timedelta(days=1)+timedelta(hours=4))
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day)
        result, success = self.diet.get_columns_given_range(dt1+timedelta(days=1),dt1+timedelta(days=2))

        self.assertTrue(success)
        self.assertEqual(len(result), 3)

if __name__ == '__main__':
    unittest.main()
