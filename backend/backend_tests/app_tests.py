import requests
import unittest
from datetime import datetime, timedelta
from backend.db import DB

# TODO: change tests from names to test_# due to execution order
# Add comments to post tests
# change timestamps
# manually check db where indicated
# check/reformat some entries in the getters to match the changes POST tests
# gets have option params, not data

class FlaskAppTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
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
        dateTo = datetime.utcnow()
        dateFrom = dateTo - timedelta(days=1)
        self.get_data = {'token': self.token,
                        'dateFrom': dateFrom,
                        'dateTo': dateTo}

    def test_enterWorkout(self):
        data = {'weight':120,
                'workout':'Tennis',
                'minutes': 45.8,
                'token': self.token}
        method = 'enterWorkout'
        resp = requests.post(self.url + method, data)
        self.assertEqual(resp.status_code, 200)

        # manually check the db for the entry

    def test_mult_enterWorkout(self):
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
        method = 'enterWorkout'
        resp = requests.post(self.url + method, {})
        self.assertEqual(resp.status_code, 400)

    def test_invalid_enterWorkout_values(self):
        method = 'enterWorkout'
        data = {'weight': 120.1,
                'workout':'blah',
                'minutes': 68.2,
                'token':self.token}

        resp = requests.post(self.url + method, data)
        self.assertEqual(resp.status_code, 400)

    def test_bad_data_enterWorkout(self):
        method = 'enterWorkout'
        data2 = {'wght':120,
                 'minutes': 57.4,
                 'token':self.token}
        resp = requests.post(self.url + method, data2)
        self.assertNotEqual(resp.status_code, 200)

    def test_addMeal(self):
        data = {'token': self.token,
                'item': 'Cookie Butter Cookies',
                'ServingSize': 2,
                'barcode': 'false'}
        method = 'addMeal'
        resp = requests.post(self.url + method, data=data)
        self.assertEqual(resp.status_code, 200)

        # manually check db

    def test_mult_addMeal(self):
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
        method = 'addMeal'
        data1 = {'ten': self.token,
                 'stuff': 'Chicken',
                 'ServingSize': 1.98,
                 'barcode': 'false'}
        resp = requests.post(self.url + method, data=data1)
        self.assertNotEqual(resp.status_code, 200)

    def test_error_addMeal_bad_values(self):
        method = 'addMeal'
        data2 = {'token': self.token,
                'item': 'Orange',
                'ServingSize': "hi"}
        resp = requests.post(self.url + method, data=data2)
        self.assertNotEqual(resp.status_code, 200)

    def test_insertSleepEntry(self):
        method = 'addMeal'

        # change to utc timestamps
        dateTo = datetime.utcnow()
        dateFrom = dateTo - timedelta(hours=6) - timedelta(minutes=27)
        data = {'token': self.token,
                'dateFrom': dateFrom,
                'dateTo': dateTo,
                'nap': False}
        method = 'insertSleepEntry'
        resp = requests.post(self.url + method, data=data)
        self.assertEqual(resp.status_code, 200)

        # manually check db

    def test_error_insertSleepEntry_missing_data(self):
        method = 'insertSleepEntry'
        dateTo = datetime.utcnow()
        dateFrom = dateTo - timedelta(hours=6) - timedelta(minutes=27)

        data1 = {'token':self.token,
                 'dateTo': dateTo,
                 'nap': False}
        resp = requests.post(self.url + method, data1)
        self.assertNotEqual(resp.status_code, 200)

    def test_error_insertSleepEntry_bad_value(self):
        method = 'insertSleepEntry'
        dateTo2 = datetime.now()
        dateFrom2 = dateTo2 - timedelta(hours=6) - timedelta(minutes=27)
        data2 = {'token': "no token",
                 'dateFrom': dateFrom2,
                 'dateTo': dateTo2,
                 'nap': False}
        resp = requests.post(self.url + method, data2)
        self.assertNotEqual(resp.status_code, 200)

    def test_changeGoal(self):
        method = 'changeGoal'
        data1 = {'token':self.token,
                'type': 'FitnessMinutes',
                'value':60}
        resp = requests.post(self.url + method, data=data1)
        self.assertEqual(resp.status_code, 200)

        # manually check the db

    def test_changeGoal_multiple(self):
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
        method = 'changeGoal'
        data1 = {'token':self.token,
                 'type': 'Fake Goal Type',
                 'value':60}
        resp = requests.post(self.url + method, data=data1)
        self.assertNotEqual(resp.status_code, 200)

    def test_error_changeGoal_bad_keys(self):
        method = 'changeGoal'
        data2 = {'token':self.token,
                'blah': 'Calories',
                'value':1800.23}
        resp = requests.post(self.url + method, data=data2)
        self.assertNotEqual(resp.status_code, 200)

    def test_error_changeGoal_no_data(self):
        method = 'changeGoal'
        data3 = {}
        resp = requests.post(self.url + method, data=data3)
        self.assertNotEqual(resp.status_code, 200)

    def test_getFitnessData(self):
        """
        Test fetching data for Fitness from the database.
        """
        method = 'getFitnessData'
        req = requests.get(self.url + method, data=self.get_data)
        self.assertEqual(req, 200)
        self.assertEqual(len(req), 3)
        self.assertEqual(req[0]['workout'], 'Basketball: game')

    def test_getNutritionalData(self):
        """
        Test fetching data for nutritional data from the database.
        """
        data = {'item': 'Cookie Butter Cookies',
                'barcode': 'false',
                'serving_size': 2}
        method = 'getNutritionalData'
        req = requests.get(self.url + method, data=data)
        self.assertEqual(req, 200)
        self.assertEqual(req[0], 'Cookie Butter Cookies')

    def test_error_getNutritionalData(self):
        """
        Test fetching data for Fitness from the database with incorrect search values.
        """
        method = 'getNutritionalData'

        data1 = {'item': 2,
                'serving_size': 1.6}
        req = requests.get(self.url + method, data=data1)
        self.assertEqual(req, 200)

        data2 = {'item': 'Cookie Butter Cookies',
                'barcode': 'false'}
        req = requests.get(self.url + method, data=data2)
        self.assertEqual(req, 200)

    def test_getAvailableFoods(self):
        """
        Test fetching available food data from Edamam API given item name and number of matches.
        """
        data = {'item': 'Peanut Butter',
                'barcode': 'false',
                'nMatches': 2,
                'serving_size': 2}
        method = 'getAvailableFoods'
        req = requests.get(self.url + method, data=data)
        self.assertEqual(req, 200)
        self.assertEqual(len(req),2)

    def test_error_getAvailableFoods(self):
        """
        Test fetching available food data from Edamam API given incorrect search parameters.
        """
        method = 'getAvailableFoods'

        data1 = {'item': 'Peanut Butter',
                'barcode': 'false',
                'nMatches': 2.4,
                'serving_size': 2}
        req = requests.get(self.url + method, data=data1)
        self.assertNotEqual(req, 200)

        data2 = {'item': 'Peanut Butter',
                'barcode': 'false',
                'nMatches': 2}
        req = requests.get(self.url + method, data=data2)
        self.assertNotEqual(req, 200)

    def test_getMeals(self):
        """
        Test fetching all meals inputted by the user from the database.
        """
        method = 'getMeals'
        req = requests.get(self.url + method, data=self.get_data)
        self.assertEqual(req, 200)

    def test_getSleepData(self):
        """
        Test fetching all sleep data inputted by the user from the database.
        """
        method = 'getSleepData'
        req = requests.get(self.url + method, data=self.get_data)
        self.assertEqual(req, 200)

    def test_getAllGoals(self):
        """
        Test fetching all goal data from database.
        Make sure the goal values are correct and updated.
        """
        method = 'getAllGoals'
        req = requests.get(self.url + method, data={'token':self.token})
        self.assertEqual(req, 200)
        for goal in req:
            if goal['type'] == 'FitnessMinutes':
                self.assertEqual(goal['value'], 57)
            elif goal['type'] == 'Calories':
                self.assertEqual(goal['value'], 1500)
            elif goal['type'] == 'SleepHours':
                self.assertEqual(goal['value'], 9)

    def test_getTypeGoals(self):
        """
        Test fetching goal data from database based on goal type.
        Make sure the values are correct and updated.
        """
        method = 'getTypeGoals'
        data1 = {'token':self.token,
                'type':'Calories'}
        req = requests.get(self.url + method, data=data1)
        self.assertEqual(req, 200)
        self.assertEqual(req['value'], 57)

        data2 = {'token':self.token,
                'type':'FitnessMinutes'}
        req = requests.get(self.url + method, data=data2)
        self.assertEqual(req, 200)
        self.assertEqual(req['value'], 1500)

        data3 = {'token':self.token,
                'type':'SleepHours'}
        req = requests.get(self.url + method, data=data3)
        self.assertEqual(req, 200)
        self.assertEqual(req['value'], 9)

    def test_error_getTypeGoals(self):
        """
        Test fetching goal data from database given incorrect goal type.
        """
        method = 'getTypeGoals'
        data1 = {'token':self.token,
                'type':'Diet'}
        req = requests.get(self.url + method, data=data1)
        self.assertNotEqual(req, 200)

        data2 = {'token':self.token,
                'type':'Fitness'}
        req = requests.get(self.url + method, data=data2)
        self.assertNotEqual(req, 200)

        data3 = {'token':self.token,
                'type':'Sleep'}
        req = requests.get(self.url + method, data=data3)
        self.assertNotEqual(req, 200)


if __name__ == '__main__':
    unittest.main()
