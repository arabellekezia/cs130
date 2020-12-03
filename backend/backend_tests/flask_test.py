import requests
import unittest
import backend.app
from datetime import datetime, timedelta
class FlaskTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.url = 'http://localhost:5000/'
        # self.token = '123abc'
        self.reg_user = {'email':'test@gmail.com',
                    'password':'123',
                    'fullname':'Test'}
        self.user = {'email':'test@gmail.com',
                    'password':'123'}
        req = requests.post(self.url + 'register', data=self.reg_user)
        if req != 200:
            print("User can't be registered")

        self.token = requests.post(self.url + 'login', data=self.user)

        dateTo = datetime.utcnow()
        dateFrom = dateTo - timedelta(days=1)
        self.get_data = {'token': self.token,
                        'dateFrom': dateFrom,
                        'dateTo': dateTo}

    def test_enterWorkout(self):
        """
        Test data insertion for Fitness to the database.
        """
        token = self.token
        data = {'weight':120,
                'workout':'Basketball: game',
                'minutes': 45.8,
                'token':token}
        method = 'enterWorkout'
        req = requests.post(self.url + method, data=data)
        self.assertEqual(req, 200)

    def test_mult_enterWorkout(self):
        """
        Test multiple data insertions for Fitness to the database.
        """
        method = 'enterWorkout'
        data1 = {'weight':130,
                'workout':'Running: 6 min/mile',
                'minutes': 68.2,
                'token':self.token}

        req = requests.post(self.url + method, data=data1)
        self.assertEqual(req, 200)

        data2 = {'weight':120,
                'workout':'Swimming: general',
                'minutes': 57.4,
                'token':self.token}
        req = requests.post(self.url + method, data=data2)
        self.assertEqual(req, 200)

    def test_error_enterWorkout(self):
        """
        Test incorrect data insertion for Fitness to the database.
        """
        method = 'enterWorkout'
        req = requests.post(self.url + method, data={})
        self.assertEqual(req, 400)

        data1 = {'weight':120,
                'workout':'run',
                'minutes': 68.2,
                'token':self.token}

        req = requests.post(self.url + method, data=data1)
        self.assertNotEqual(req, 200)

        data2 = {'weight':120.5,
                'workout':'Running: 6 min/mile',
                'minutes': 57.4,
                'token':self.token}
        req = requests.post(self.url + method, data=data2)
        self.assertNotEqual(req, 200)

        data3 = {'weight':120,
                'minutes': 57.4,
                'token':self.token}
        req = requests.post(self.url + method, data=data3)
        self.assertNotEqual(req, 200)

    def test_getFitnessData(self):
        """
        Test fetching data for Fitness from the database.
        """
        method = 'getFitnessData'
        req = requests.get(self.url + method, data=self.get_data)
        self.assertEqual(req, 200)
        self.assertEqual(len(req), 3)
        self.assertEqual(req[0]['workout'], 'Basketball: game')

    def test_addMeal(self):
        """
        Test inserting data for meals to the database.
        """
        data = {'token':self.token,
                'item': 'Cookie Butter Cookies',
                'ServingSize': 2,
                'barcode': 'false'}
        method = 'addMeal'
        req = requests.post(self.url + method, data=data)
        self.assertEqual(req, 200)

    def test_addMeal_API(self):
        """
        Test inserting data for meals to the database using the Edamam API.
        """
        data = {'token':self.token,
                'item': 'Oreo',
                'ServingSize': 5,
                'barcode': 'true'}
        method = 'addMeal'
        req = requests.post(self.url + method, data=data)
        self.assertEqual(req, 200)

    def test_mult_addMeal(self):
        """
        Test multiple insertions of data for meals to the database.
        """
        method = 'addMeal'
        data1 = {'token':self.token,
                'item': 'Chicken',
                'ServingSize': 1,
                'barcode': 'false'}
        req = requests.post(self.url + method, data=data1)
        self.assertEqual(req, 200)

        data2 = {'token':self.token,
                'item': 'Orange',
                'ServingSize': 3,
                'barcode': 'false'}
        req = requests.post(self.url + method, data=data2)
        self.assertEqual(req, 200)

    def test_error_addMeal(self):
        """
        Test incorrect insertion of meals data to the database.
        """
        method = 'addMeal'

        data1 = {'token':self.token,
                'item': 'Chicken',
                'ServingSize': 1.98,
                'barcode': 'false'}
        req = requests.post(self.url + method, data=data1)
        self.assertNotEqual(req, 200)

        data2 = {'token':self.token,
                'item': 'Orange',
                'ServingSize': 3}
        req = requests.post(self.url + method, data=data2)
        self.assertNotEqual(req, 200)

        data3 = {'token':self.token,
                'item': 2,
                'ServingSize': 3}
        req = requests.post(self.url + method, data=data3)
        self.assertNotEqual(req, 200)

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

    def test_insertSleepEntry(self):
        """
        Test inserting sleep data to the database.
        """
        dateTo = datetime.utcnow()
        dateFrom = dateTo - timedelta(hours=6) - timedelta(minutes=27)
        data = {'token':self.token,
                'dateFrom': dateFrom,
                'dateTo': dateTo,
                'nap': False}
        method = 'insertSleepEntry'
        req = requests.post(self.url + method, data=data)
        self.assertEqual(req, 200)

    def test_error_insertSleepEntry(self):
        """
        Test inserting incorrect sleep data to the database.
        """
        method = 'insertSleepEntry'
        dateTo = datetime.utcnow()
        dateFrom = dateTo - timedelta(hours=6) - timedelta(minutes=27)

        data1 = {'token':self.token,
                'dateTo': dateTo,
                'nap': False}
        req = requests.post(self.url + method, data=data1)
        self.assertNotEqual(req, 200)

        dateTo2 = datetime.now()
        dateFrom2 = dateTo - timedelta(hours=6) - timedelta(minutes=27)
        data2 = {'token':self.token,
                'dateFrom': dateFrom2,
                'dateTo': dateTo2,
                'nap': False}
        req = requests.post(self.url + method, data=data2)
        self.assertNotEqual(req, 200)

    def test_getSleepData(self):
        """
        Test fetching all sleep data inputted by the user from the database.
        """
        method = 'getSleepData'
        req = requests.get(self.url + method, data=self.get_data)
        self.assertEqual(req, 200)

    def test_changeGoal(self):
        """
        Test modifying goals data in the database.
        """
        method = 'changeGoal'
        data1 = {'token':self.token,
                'type': 'FitnessMinutes',
                'value':60}
        req = requests.post(self.url + method, data=data1)
        self.assertEqual(req, 200)

        data2 = {'token':self.token,
                'type': 'Calories',
                'value':1800}
        req = requests.post(self.url + method, data=data2)
        self.assertEqual(req, 200)

        data3 = {'token':self.token,
                'type': 'SleepHours',
                'value':8}
        req = requests.post(self.url + method, data=data3)
        self.assertEqual(req, 200)

    def test_mult_changeGoal(self):
        """
        Test modifying goals data multiple times in the database.
        """
        method = 'changeGoal'
        data1 = {'token':self.token,
                'type': 'FitnessMinutes',
                'value':60}
        req = requests.post(self.url + method, data=data1)
        self.assertEqual(req, 200)

        method = 'changeGoal'
        data2 = {'token':self.token,
                'type': 'FitnessMinutes',
                'value':57}
        req = requests.post(self.url + method, data=data2)
        self.assertEqual(req, 200)

        data3 = {'token':self.token,
                'type': 'Calories',
                'value':1800}
        req = requests.post(self.url + method, data=data3)
        self.assertEqual(req, 200)

        data4 = {'token':self.token,
                'type': 'Calories',
                'value':1500}
        req = requests.post(self.url + method, data=data4)
        self.assertEqual(req, 200)

        data5 = {'token':self.token,
                'type': 'SleepHours',
                'value':8}
        req = requests.post(self.url + method, data=data5)
        self.assertEqual(req, 200)

        data6 = {'token':self.token,
                'type': 'SleepHours',
                'value':9}
        req = requests.post(self.url + method, data=data6)
        self.assertEqual(req, 200)

    def test_error_changeGoal(self):
        """
        Test modifying goals data in the database given incorrect parameters.
        """
        method = 'changeGoal'
        data1 = {'token':self.token,
                'type': 'Fitness',
                'value':60}
        req = requests.post(self.url + method, data=data1)
        self.assertNotEqual(req, 200)

        data2 = {'token':self.token,
                'type': 'Calories',
                'value':1800.23}
        req = requests.post(self.url + method, data=data2)
        self.assertNotEqual(req, 200)

        data3 = {'token':self.token,
                'type': 'Sleep',
                'value':8}
        req = requests.post(self.url + method, data=data3)
        self.assertNotEqual(req, 200)

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
