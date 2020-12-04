import unittest
from backend.db import DB
from backend.user import User
from backend.Diet import Diet
from datetime import datetime, date, timedelta
import time
import copy
 
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
                
        self.email_1 = 'xyz@gmail.com' 
        self.password_1 = 'klmno'
        self.fullname_1 = 'XYZ'
        
        self.user_1 = User(self.db)
        self.user_1.create_new_user(self.email_1, self.password_1, self.fullname_1)
        self.user_id_1 = self.user_1.check_email_match(self.email_1)
        
        self.email_2 = 'lmn@gmail.com' 
        self.password_2 = 'qqq'
        self.fullname_2 = 'ASD'
        
        self.user_2 = User(self.db)
        self.user_2.create_new_user(self.email_2, self.password_2, self.fullname_2)
        self.user_id_2 = self.user_2.check_email_match(self.email_2)
        
        self.diet = Diet(self.db, self.user_id)
        self.diet_1 = Diet(self.db, self.user_id_1)
        self.diet_2 = Diet(self.db, self.user_id_2)
        
        
        self.diet_dict = {'Item': 'Apple',\
                         'ServingSize': 1.0,\
                         'Barcode': False,\
                         'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.diet_dict_1 = {'Item': 'Orange',\
                         'ServingSize': 2.0,\
                         'Barcode': False,\
                         'nutri_dict': {'Cals': 105.0,'Protein': 105.0, 'Carbs': 105.0, 'Fat': 105.0, 'Fiber': 105.0}}
        self.diet_dict_2 = {'Item': 'banana',\
                         'ServingSize': 2.0,\
                         'Barcode': False,\
                         'nutri_dict': {'Cals': 101.0,'Protein': 101.0, 'Carbs': 101.0, 'Fat': 101.0, 'Fiber': 101.0}}
        
        
        self.dt1 = datetime.utcnow()
        self.unix_time = round(time.time())
        
    def test_0_data_insertion(self):
        """
        Test database insertion for a single user. 
        """
        s = self.diet.insert_in_database(self.diet_dict, date_time=self.dt1)
        self.assertEqual(s, True)
        
    def test_1_data_insertion_multiple_users(self):
        """
        Test database insertion for multiple users.
        """
        s = self.diet.insert_in_database(self.diet_dict, date_time=self.dt1)
        self.assertEqual(s, True)
        s_1 = self.diet_1.insert_in_database(self.diet_dict_1, date_time=self.dt1)
        self.assertEqual(s_1, True)
        s_2 = self.diet_2.insert_in_database(self.diet_dict_2)
        self.assertEqual(s_2, True)

    def test_2_incorrect_key(self):
        """
        Test for incorrect keys. The function should return False if the input dictionary keys are incorrect.
        """
        d = copy.deepcopy(self.diet_dict)
        del(d['Item'])
        d['ItemS'] = 'Apple'
        self.assertFalse(self.diet.insert_in_database(d))

        d = copy.deepcopy(self.diet_dict)
        del(d['ServingSize'])
        d['ServinsSizeS'] = 1.0
        self.assertFalse(self.diet.insert_in_database(d))
        
        d = copy.deepcopy(self.diet_dict)
        del(d['Barcode'])
        d['BarcodeS'] = False
        self.assertFalse(self.diet.insert_in_database(d))

        d = copy.deepcopy(self.diet_dict)
        del(d['nutri_dict'])
        d['nutri_dictS'] = {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}
        self.assertFalse(self.diet.insert_in_database(d))
        
    def test_3_incorrect_key_1(self):
        """
        Test for incorrect keys in the nutri_dict. The function should return False if the nutrient names is incorrect.
        """
        d = copy.deepcopy(self.diet_dict)
        del(d['nutri_dict']['Cals'])
        d['nutri_dict']['CalsS'] = 100.0
        self.assertFalse(self.diet.insert_in_database(d))

        d = copy.deepcopy(self.diet_dict)
        del(d['nutri_dict']['Protein'])
        d['nutri_dict']['ProteinS'] = 100.0
        self.assertFalse(self.diet.insert_in_database(d))
        
        d = copy.deepcopy(self.diet_dict)
        del(d['nutri_dict']['Carbs'])
        d['nutri_dict']['CarbS'] = 100.0
        self.assertFalse(self.diet.insert_in_database(d))
        
        d = copy.deepcopy(self.diet_dict)
        del(d['nutri_dict']['Fat'])
        d['nutri_dict']['FatS'] = 100.0         
        self.assertFalse(self.diet.insert_in_database(d))
    
        d = copy.deepcopy(self.diet_dict)
        del(d['nutri_dict']['Fiber'])
        d['nutri_dict']['FiberS'] = 100.0
        self.assertFalse(self.diet.insert_in_database(d))
        
        
    def test_4_incorrect_value(self):
        """
        Test for incorrect value data type.
        """
        d = copy.deepcopy(self.diet_dict)
        d['Item'] = 1
        self.assertFalse(self.diet.insert_in_database(d))

        d = copy.deepcopy(self.diet_dict)
        d['ServingSize'] = 'Apple'
        self.assertFalse(self.diet.insert_in_database(d))

        d = copy.deepcopy(self.diet_dict)
        d['Barcode'] = 1
        self.assertFalse(self.diet.insert_in_database(d))

    def test_5_incorrect_value_1(self):
        """
        Test for incorrect value data type in the nutrients dictionary.
        """
        d = copy.deepcopy(self.diet_dict)
        d['nutri_dict']['Cals'] = 'Apple'
        self.assertFalse(self.diet.insert_in_database(d))

        d = copy.deepcopy(self.diet_dict)
        d['nutri_dict']['Protein'] = 'Apple'
        self.assertFalse(self.diet.insert_in_database(d))
        
        d = copy.deepcopy(self.diet_dict)
        d['nutri_dict']['Fiber'] = 'Apple'
        self.assertFalse(self.diet.insert_in_database(d))
        
        d = copy.deepcopy(self.diet_dict)
        d['nutri_dict']['Carbs'] = 'Apple'
        self.assertFalse(self.diet.insert_in_database(d))

        d = copy.deepcopy(self.diet_dict)
        d['nutri_dict']['Fat'] = 'Apple'
        self.assertFalse(self.diet.insert_in_database(d))

    def test_6_data_fetching_unix_time_and_insertion(self):
        """
        Test fetching diet data from database and also checks if the UNIX TIMESTAMP is correct.
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.diet.get_columns_given_range(dt1, dt1+timedelta(days=1))
        self.assertTrue(success)
        self.assertEqual(result[0]['Datetime'],self.unix_time)

    def test_7_data_fetching_values(self):
        """
        Test fetching diet data from database for multiple users. 
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
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
        
        result_1, success_1 = self.diet_1.get_columns_given_range(dt1, dt1+timedelta(days=1))

        self.assertTrue(success_1)
        self.assertEqual(result_1[0]['Item'], 'Orange')
        self.assertEqual(result_1[0]['ServingSize'], 2.0)
        self.assertEqual(result_1[0]['Cals'], 105.0)
        self.assertEqual(result_1[0]['Fiber'], 105.0)
        self.assertEqual(result_1[0]['Carbs'], 105.0)
        self.assertEqual(result_1[0]['Fat'], 105.0)
        self.assertEqual(result_1[0]['Protein'], 105.0)
        self.assertFalse(result_1[0]['Barcode'])
        
    def test_8_incorrect_data_fetching(self):
        """
        Test fetching diet data from the database for incorrect date range. The function 
        should return False.
        """
        d1 = date.today()
        dt1 = datetime(d1.year, d1.month, d1.day) + timedelta(hours=8)
        result, success = self.diet.get_columns_given_range(dt1+timedelta(days=10),dt1+timedelta(days=11))
        self.assertFalse(success)
        
    def test_9_data_fetching_multiple(self):
        """
        Test fetching multiple diet entries from the database.
        """
        d = {'Item': 'Apple',\
             'ServingSize': 1.0,\
             'Barcode': False,\
             'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        _ = self.diet.insert_in_database(d, date_time=datetime.utcnow()+timedelta(days=1)+ timedelta(minutes=1))
        d = {'Item': 'Orange',\
             'ServingSize': 1.0,\
             'Barcode': False,\
             'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        _ = self.diet.insert_in_database(d, date_time=datetime.utcnow()+timedelta(days=1)+timedelta(minutes=2))
        d = {'Item': 'Banana',\
             'ServingSize': 1.0,\
             'Barcode': False,\
             'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        _ = self.diet.insert_in_database(d, date_time=datetime.utcnow()+timedelta(days=1)+timedelta(minutes=3))
        d1 = date.today() + timedelta(days=1) 
        dt1 = datetime(d1.year, d1.month, d1.day)+ timedelta(hours=8)
        result, success = self.diet.get_columns_given_range(dt1,dt1+timedelta(days=1))

        self.assertTrue(success)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['Item'],'Apple')
        self.assertEqual(result[1]['Item'],'Orange')
        self.assertEqual(result[2]['Item'],'Banana')
        
    def test_10_incorrect_database(self):
        """
        Test database insertion for a single user with incorrect database. Test case to increase the coverage. 
        """
        diet = Diet(None, self.user_id_2)
        s = diet.insert_in_database(self.diet_dict, date_time=self.dt1)
        self.assertFalse(s)
        d1 = date.today() + timedelta(days=1) 
        dt1 = datetime(d1.year, d1.month, d1.day)+ timedelta(hours=8)
        result, success = diet.get_columns_given_range(dt1, dt1+timedelta(days=1))
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()
