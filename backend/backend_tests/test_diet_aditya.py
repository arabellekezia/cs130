import unittest
from backend.db import DB
from backend.user import User
from backend.Diet import Diet
from datetime import datetime, date, timedelta

diet_table_command = ("CREATE TABLE Diet "
        "(Item varchar(300) NOT NULL, ServingSize DOUBLE, Cals DOUBLE, Protein DOUBLE, Carbs DOUBLE, "
        "Fat DOUBLE, Fiber DOUBLE, Barcode BOOLEAN, " 
        "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
        "REFERENCES Users(id));")

class TestDiet(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB()
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password)
        self.user_id = self.user.check_email_match(self.email)
        
        try:
            self.db.insert_data('Drop table Diet')
        except:
            pass
        self.db.insert_data(diet_table_command)
        
        self.diet = Diet(self.db, self.user_id)
        self.diet_dict = {'Item': 'Apple',\
                         'ServingSize': 1.0,\
                         'Barcode': False,\
                         'nutri_dict': {'Cals': 100.0,'Protein': 100.0, 'Carbs': 100.0, 'Fat': 100.0, 'Fiber': 100.0}}
        self.diet.insert_in_database(self.diet_dict)
        
    def test_insert_in_database(self):
        """
        Test inserting an input in the database
        """
        self.assertTrue(self.diet.insert_in_database(self.diet_dict))

    def test_incorrect_key(self):
        """
        Test for incorrect keys. We send incorrect key: ItemS
        """
        print('Test Incorrect Key')
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
        print("")
        
    def test_incorrect_key_1(self):
        """
        Test for incorrect keys. We send incorrect key: CalsS
        """
        print('Test Incorrect Key 1: Single Fetch')
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
        print("")
        
        
    def test_incorrect_value(self):
        """
        Test for incorrect value type.
        """
        print('Test Incorrect Value')
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
        print("")

    def test_incorrect_value_1(self):
        """
        Test for incorrect value type.
        """
        print('Incorrect Value 1')
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
        print("")

        
    def test_data_fetching(self):
        """
        Test fetching diet data from database
        """
        print('Fetched Result 1')
        result, success = self.diet.get_columns_given_range(date.today(), date.today()+timedelta(days=1))
        print(result)
        print("")
        self.assertTrue(success)
        
    def test_incorrect_data_fetching(self):
        """
        Test fetching diet data from database
        """
        print('Fetched Result 2: Incorrect Fetching')
        result, success = self.diet.get_columns_given_range(date.today()+timedelta(days=10),date.today()+timedelta(days=11))
        print(result)
        print("")
        self.assertFalse(success)
        
        
    def test_data_fetching_multiple(self):
        """
        Test fetching diet data from database
        """
        print('Fetched Result 3: Multiple Fetching')
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
        result, success = self.diet.get_columns_given_range(date.today()+timedelta(days=1),date.today()+timedelta(days=2))
        print(result)
        print("")
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()
