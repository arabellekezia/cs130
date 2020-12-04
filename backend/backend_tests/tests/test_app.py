import requests
import unittest
from datetime import datetime, timedelta, timezone
from backend.db import DB

# TODO: change tests from names to test_# due to execution order
# manually check db where indicated

class FlaskAppTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """
        Set up class variables for testing the Flasp app.
        """        
        self.url = 'http://localhost:5000/'
        self.db = DB()
        self.reg_user = {'email':'test@gmail.com',
                    'password':'123',
                    'fullname':'Test'}
        self.user = {'email':'test@gmail.com',
                    'password':'123'}
        resp = requests.post(self.url + 'register', data=self.reg_user)
        #assert (resp.status_code == 200)

        resp = requests.post(self.url + 'auth/login', data=self.user)
        self.token = resp.text
        assert (resp.status_code == 200)
        date1 = datetime.now() + timedelta(days=1)
        date2 = date1 - timedelta(days=2)
        dateTo = date1.replace(tzinfo = timezone.utc).timestamp()
        dateFrom = date2.replace(tzinfo = timezone.utc).timestamp()
        self.get_data = {'token': self.token,
                        'dateFrom': dateFrom,
                        'dateTo': dateTo}

    def test_enterWorkout(self):
        """
        Test data insertion for Fitness to the database.
        """
        data = {'weight':120,
                'workout':'Tennis',
                'minutes': 45.8,
                'token': self.token}
        method = 'enterWorkout'
        resp = requests.post(self.url + method, data)
        self.assertEqual(resp.status_code, 200)

        # manually check the db for the entry

    def test_mult_enterWorkout(self):
        """
        Test multiple data insertions for Fitness to the database.
        """
        method = 'enterWorkout'
        data = {'weight': 130,
                'workout': 'Football: touch, flag',
                'minutes': 68.2,
                'token': self.token}

        resp = requests.post(self.url + method, data)
        self.assertEqual(resp.status_code, 200)

        data2 = {'weight': 120,
                 'workout': 'Soccer',
                 'minutes': 57.4,
                 'token':self.token}
        resp = requests.post(self.url + method, data2)
        self.assertEqual(resp.status_code, 200)

    def test_error_enterWorkout_no_data(self):
        """
        Test incorrect data insertion attemps for Fitness to the database.
        """
        method = 'enterWorkout'
        resp = requests.post(self.url + method, {})
        self.assertEqual(resp.status_code, 400)

        data = {'weight': 120.1,
                'workout':'blah',
                'minutes': 68.2,
                'token':self.token}

        resp = requests.post(self.url + method, data)
        self.assertEqual(resp.status_code, 400)

        data2 = {'wght':120,
                 'minutes': 57.4,
                 'token':self.token}
        resp = requests.post(self.url + method, data2)
        self.assertNotEqual(resp.status_code, 200)

    def test_addMeal(self):
        """
        Test inserting data for meals to the database.
        """
        data = {'token': self.token,
                'item': 'Cookie Butter Cookies',
                'ServingSize': 2,
                'barcode': 'false'}
        method = 'addMeal'
        resp = requests.post(self.url + method, data=data)
        self.assertEqual(resp.status_code, 200)

        # manually check db

    def test_mult_addMeal(self):
        """
        Test inserting data for meals to the database using the Edamam API.
        """
        method = 'addMeal'
        data1 = {'token':self.token,
                'item': 'Chicken',
                'ServingSize': 1,
                'barcode': 'false'}
        resp = requests.post(self.url + method, data=data1)
        self.assertEqual(resp.status_code, 200)

        data2 = {'token':self.token,
                'item': 'Orange',
                'ServingSize': 3,
                'barcode': 'false'}
        resp = requests.post(self.url + method, data=data2)
        self.assertEqual(resp.status_code, 200)

    def test_error_addMeal_bad_keys(self):
        """
        Test incorrect insertion attempts of meals data to the database.
        """
        method = 'addMeal'
        data1 = {'ten': self.token,
                 'stuff': 'Chicken',
                 'ServingSize': 1.98,
                 'barcode': 'false'}
        resp = requests.post(self.url + method, data=data1)
        self.assertNotEqual(resp.status_code, 200)

        data2 = {'token': self.token,
                'item': 'Orange',
                'ServingSize': "hi"}
        resp = requests.post(self.url + method, data=data2)
        self.assertNotEqual(resp.status_code, 200)

    def test_insertSleepEntry(self):
        """
        Test inserting sleep data to the database.
        """
        method = 'insertSleepEntry'
        date1 = datetime.now()
        date2 = date1 - timedelta(hours=6) - timedelta(minutes=27)
        dateTo = date1.replace(tzinfo = timezone.utc).timestamp()
        dateFrom = date2.replace(tzinfo = timezone.utc).timestamp()
        data = {'token': self.token,
                'dateFrom': dateFrom,
                'dateTo': dateTo,
                'nap': False}
        method = 'insertSleepEntry'
        resp = requests.post(self.url + method, data=data)
        self.assertEqual(resp.status_code, 200)

        # manually check db

    def test_error_insertSleepEntry_missing_data(self):
        """
        Test inserting incorrect sleep data to the database.
        """
        method = 'insertSleepEntry'
        dateTo = datetime.utcnow()
        dateFrom = dateTo - timedelta(hours=6) - timedelta(minutes=27)

        data1 = {'token':self.token,
                 'dateTo': dateTo,
                 'nap': False}
        resp = requests.post(self.url + method, data1)
        self.assertNotEqual(resp.status_code, 200)

        dateTo2 = datetime.now()
        dateFrom2 = dateTo2 - timedelta(hours=6) - timedelta(minutes=27)
        data2 = {'token': "no token",
                 'dateFrom': dateFrom2,
                 'dateTo': dateTo2,
                 'nap': False}
        resp = requests.post(self.url + method, data2)
        self.assertNotEqual(resp.status_code, 200)

    def test_changeGoal(self):
        """
        Test modifying goals data in the database.
        """
        method = 'changeGoal'
        data1 = {'token':self.token,
                'type': 'FitnessMinutes',
                'value':60}
        resp = requests.post(self.url + method, data=data1)
        self.assertEqual(resp.status_code, 200)

        # manually check the db

    def test_changeGoal_multiple(self):
        """
        Test modifying goals data multiple times in the database.
        """
        method = 'changeGoal'
        data2 = {'token':self.token,
                'type': 'Calories',
                'value':1800}
        resp = requests.post(self.url + method, data=data2)
        self.assertEqual(resp.status_code, 200)

        data3 = {'token':self.token,
                'type': 'SleepHours',
                'value':8}
        resp = requests.post(self.url + method, data=data3)
        self.assertEqual(resp.status_code, 200)

        data3 = {'token':self.token,
                'type': 'Calories',
                'value':1800}
        resp = requests.post(self.url + method, data=data3)
        self.assertEqual(resp.status_code, 200)

        data4 = {'token':self.token,
                'type': 'Calories',
                'value':1500}
        resp = requests.post(self.url + method, data=data4)
        self.assertEqual(resp.status_code, 200)

    def test_error_changeGoal_bad_values(self):
        """
        Test modifying goals data in the database given incorrect parameters.
        """
        method = 'changeGoal'
        data1 = {'token':self.token,
                 'type': 'Fake Goal Type',
                 'value':60}
        resp = requests.post(self.url + method, data=data1)
        self.assertNotEqual(resp.status_code, 200)

        data2 = {'token':self.token,
                'blah': 'Calories',
                'value':1800.23}
        resp = requests.post(self.url + method, data=data2)
        self.assertNotEqual(resp.status_code, 200)

        data3 = {}
        resp = requests.post(self.url + method, data=data3)
        self.assertNotEqual(resp.status_code, 200)

    def test_getFitnessData(self):
        """
        Test fetching data for Fitness from the database.
        """
        method = 'getFitnessData'
        resp = requests.get(self.url + method, self.get_data)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(len(data) > 2)
        self.assertEqual(data[0]['WorkoutType'], 'Tennis')

    def test_getNutritionalData(self):
        """
        Test fetching data for nutritional data from the database.
        """
        data = {'item': 'Cookie Butter Cookies',
                'ServingSize': 2}
        method = 'getNutritionalData'
        resp = requests.get(self.url + method, data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['0']['Label'], 'Cookie Butter Cookies')

    def test_error_getNutritionalData(self):
        """
        Test fetching data for Fitness from the database with incorrect search values.
        """
        method = 'getNutritionalData'

        data1 = {'item': 2,
                'serving_size': 1.6}
        resp = requests.get(self.url + method, data1)
        self.assertNotEqual(resp.status_code, 200)

        data2 = {'item': 'Cookie Butter Cookies',
                'barcode': 'false'}
        resp = requests.get(self.url + method, data2)
        self.assertNotEqual(resp.status_code, 200)

    def test_getAvailableFoods(self):
        """
        Test fetching available food data from Edamam API given item name and number of matches.
        """
        data = {'item': 'Peanut Butter',
                'barcode': 'false',
                'nMatches': 2,
                'ServingSize': 2}
        method = 'getAvailableFoods'
        resp = requests.get(self.url + method, data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()),2)

    def test_error_getAvailableFoods(self):
        """
        Test fetching available food data from Edamam API given incorrect search parameters.
        """
        method = 'getAvailableFoods'

        data1 = {'item': 'Peanut Butter',
                'barcode': 'false',
                'nMatches': 2.4,
                'serving_size': 2}
        resp = requests.get(self.url + method, data1)
        self.assertNotEqual(resp.status_code, 200)

        data2 = {'item': 'Peanut Butter',
                'barcode': 'false',
                'nMatches': 2}
        resp = requests.get(self.url + method, data2)
        self.assertNotEqual(resp.status_code, 200)

    def test_getMeals(self):
        """
        Test fetching all meals inputted by the user from the database.
        """
        method = 'getMeals'
        resp = requests.get(self.url + method, self.get_data)
        self.assertEqual(resp.status_code, 200)

    def test_getSleepData(self):
        """
        Test fetching all sleep data inputted by the user from the database.
        """
        method = 'getSleepData'
        resp = requests.get(self.url + method, self.get_data)
        self.assertEqual(resp.status_code, 200)

    def test_getAllGoals(self):
        """
        Test fetching all goal data from database.
        Make sure the goal values are correct and updated.
        """
        method = 'getAllGoals'
        resp = requests.get(self.url + method, {'token':self.token})
        self.assertEqual(resp.status_code, 200)
        for goal in resp.json():
            if goal['Type'] == 'FitnessMinutes':
                self.assertEqual(int(goal['Value']), 60)
            elif goal['Type'] == 'Calories':
                self.assertEqual(int(goal['Value']), 1500)
            elif goal['Type'] == 'SleepHours':
                self.assertEqual(int(goal['Value']), 8)

    def test_getTypeGoals(self):
        """
        Test fetching goal data from database based on goal type.
        Make sure the values are correct and updated.
        """
        method = 'getTypeGoals'
        data1 = {'token':self.token,
                'type':'Calories'}
        resp = requests.get(self.url + method, data1)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(int(data[0]['Value']), 1500)

        data2 = {'token':self.token,
                'type':'FitnessMinutes'}
        resp = requests.get(self.url + method, data2)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(int(data[0]['Value']), 60)

        data3 = {'token':self.token,
                'type':'SleepHours'}
        resp = requests.get(self.url + method, data3)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(int(data[0]['Value']), 8)

    def test_error_getTypeGoals(self):
        """
        Test fetching goal data from database given incorrect goal type.
        """
        method = 'getTypeGoals'
        data1 = {'token':self.token,
                'type':'Diet'}
        resp = requests.get(self.url + method, data1)
        self.assertNotEqual(resp.status_code, 200)

        data2 = {'token':self.token,
                'type':'Fitness'}
        resp = requests.get(self.url + method, data2)
        self.assertNotEqual(resp.status_code, 200)

        data3 = {'token':self.token,
                'type':'Sleep'}
        resp = requests.get(self.url + method, data3)
        self.assertNotEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
