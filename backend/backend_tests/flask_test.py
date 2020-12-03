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
            print(req)

        self.token = requests.post(self.url + 'login', data=self.user)

        dateTo = datetime.utcnow()
        dateFrom = dateTo - timedelta(days=1)
        self.get_data = {'token': self.token,
                        'dateFrom': dateFrom,
                        'dateTo': dateTo}

    def test_enterWorkout(self):
        token = self.token
        data = {'weight':120,
                'workout':'basketball',
                'minutes': 45.8,
                'token':token}
        method = 'enterWorkout'
        req = requests.post(self.url + method, data=data)
        self.assertEqual(req, 200)

    def test_mult_enterWorkout(self):
        method = 'enterWorkout'
        data1 = {'weight':130,
                'workout':'run',
                'minutes': 68.2,
                'token':self.token}

        req = requests.post(self.url + method, data=data1)
        self.assertEqual(req, 200)

        data2 = {'weight':120,
                'workout':'swim',
                'minutes': 57.4,
                'token':self.token}
        req = requests.post(self.url + method, data=data2)
        self.assertEqual(req, 200)

    def test_error_enterWorkout(self):
        method = 'enterWorkout'
        req = requests.post(self.url + method, data={})
        self.assertEqual(req, 400)

        data1 = {'weight':120.1,
                'workout':'run',
                'minutes': 68.2,
                'token':self.token}

        req = requests.post(self.url + method, data=data1)
        self.assertNotEqual(req, 200)

        data2 = {'weight':120,
                'minutes': 57.4,
                'token':self.token}
        req = requests.post(self.url + method, data=data2)
        self.assertNotEqual(req, 200)

    def test_addMeal(self):
        data = {'token':self.token,
                'item': 'Cookie Butter Cookies',
                'ServingSize': 2,
                'barcode': 'false'}
        method = 'addMeal'
        req = requests.post(self.url + method, data=data)
        self.assertEqual(req, 200)

    def test_addMeal_API(self):
        data = {'token':self.token,
                'item': 'Oreo',
                'ServingSize': 5,
                'barcode': 'true'}
        method = 'addMeal'
        req = requests.post(self.url + method, data=data)
        self.assertEqual(req, 200)

    def test_mult_addMeal(self):
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

    def test_insertSleepEntry(self):
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
        method = 'insertSleepEntry'
        dateTo = datetime.utcnow()
        dateFrom = dateTo - timedelta(hours=6) - timedelta(minutes=27)

        data1 = {'token':self.token,
                'dateTo': dateTo,
                'nap': False}
        req = requests.post(self.url + method, data=data)
        self.assertNotEqual(req, 200)

        dateTo2 = datetime.now()
        dateFrom2 = dateTo - timedelta(hours=6) - timedelta(minutes=27)
        data2 = {'token':self.token,
                'dateFrom': dateFrom2,
                'dateTo': dateTo2,
                'nap': False}
        req = requests.post(self.url + method, data=data)
        self.assertNotEqual(req, 200)

    def test_changeGoal(self):
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

    def test_error_changeGoal(self):
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

    def test_getNutritionalData(self):
        data = {'item': 'Cookie Butter Cookies',
                'barcode': 'false',
                'serving_size': 2}
        method = 'getNutritionalData'
        req = requests.get(self.url + method, data=data)
        self.assertEqual(req, 200)

    def test_getAvailableFoods(self):
        data = {'item': 'Cookie Butter Cookies',
                'barcode': 'false',
                'nMatches': 1,
                'serving_size': 2}
        method = 'getAvailableFoods'
        req = requests.get(self.url + method, data=data)
        self.assertEqual(req, 200)

    def test_getMeals(self):
        method = 'getMeals'
        req = requests.get(self.url + method, data=self.get_data)
        self.assertEqual(req, 200)

    def test_getSleepData(self):
        method = 'getSleepData'
        req = requests.get(self.url + method, data=self.get_data)
        self.assertEqual(req, 200)

    def test_getFitnessData(self):
        method = 'getFitnessData'
        req = requests.get(self.url + method, data=self.get_data)
        self.assertEqual(req, 200)

    def test_getAllGoals(self):
        method = 'getAllGoals'
        req = requests.get(self.url + method, data={'token':self.token})
        self.assertEqual(req, 200)

    def test_getTypeGoals(self):
        method = 'getTypeGoals'
        data1 = {'token':self.token,
                'type':'Calories'}
        req = requests.get(self.url + method, data=data1)
        self.assertEqual(req, 200)

        data2 = {'token':self.token,
                'type':'FitnessMinutes'}
        req = requests.get(self.url + method, data=data2)
        self.assertEqual(req, 200)

        data3 = {'token':self.token,
                'type':'SleepHours'}
        req = requests.get(self.url + method, data=data3)
        self.assertEqual(req, 200)


if __name__ == '__main__':
    unittest.main()
