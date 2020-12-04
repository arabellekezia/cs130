import unittest
from unittest.mock import patch
import backend.db
from backend.staywell_api import StaywellAPI

class TestStaywellAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.database = None
        self.staywellAPI = StaywellAPI()
        self.userID = 11

    def test_no_data(self):
        data = {'no data': -1}
        msg, status = self.staywellAPI.staywell(data, self.userID, self.database)
        self.assertEqual(status, 400)
        
    def test_no_data_1(self):
        msg, status = self.staywellAPI.staywell(None, self.userID, self.database)
        self.assertEqual(status, 400)

    def test_no_mins(self):
        data = {'weight': 200, 'workout': 'Tennis'}
        msg, status = self.staywellAPI.staywell(data, self.userID, self.database)
        self.assertEqual(status, 400)

    def test_wrong_mins_type(self):
        data = {'weight': 200, 'workout': 'Tennis'}
        data['minutes'] = "hi"
        msg, status = self.staywellAPI.staywell(data, self.userID, self.database)
        self.assertEqual(status, 400)

    def test_invalid_mins(self):
        data = {'weight': 200, 'workout': 'Tennis'}
        data['minutes'] = -4
        msg, status = self.staywellAPI.staywell(data, self.userID, self.database)
        self.assertEqual(status, 400)

    def test_no_weight(self):
        data = {'minutes': 200, 'workout': 'Tennis'}
        msg, status = self.staywellAPI.staywell(data, self.userID, self.database)
        self.assertEqual(status, 400)

    def test_wrong_mins_type(self):
        data = {'minutes': 200, 'workout': 'Tennis'}
        data['weight'] = "hi"
        msg, status = self.staywellAPI.staywell(data, self.userID, self.database)
        self.assertEqual(status, 400)

    def test_invalid_mins(self):
        data = {'minutes': 200, 'workout': 'Tennis'} 
        data['weight'] = -20
        msg, status = self.staywellAPI.staywell(data, self.userID, self.database)
        self.assertEqual(status, 400)

    def test_no_workout(self):
        data = {'minutes': 200, 'weight': 120}
        msg, status = self.staywellAPI.staywell(data, self.userID, self.database)
        self.assertEqual(status, 400)

    def test_invalid_workoutt(self):
        data = {'minutes': 200, 'weight': 120}
        data['workout'] = 'Doing Nothing'
        msg, status = self.staywellAPI.staywell(data, self.userID, self.database)
        self.assertEqual(status, 400)

    @patch('backend.db.DB')
    def test_success(self, mock_db):
        assert mock_db is backend.db.DB
        data = {'weight': 120, 'workout': 'Tennis', 'minutes': 90}
        actual_db = backend.db.DB()
        cals, status = self.staywellAPI.staywell(data, self.userID, actual_db)
        
        data = {'weight': 140, 'workout': 'Tennis', 'minutes': 90}
        cals_1, status_1 = self.staywellAPI.staywell(data, self.userID, actual_db)
        
        data = {'weight': 170, 'workout': 'Tennis', 'minutes': 90}
        cals_2, status_2 = self.staywellAPI.staywell(data, self.userID, actual_db)
        
        data = {'weight': 200, 'workout': 'Tennis', 'minutes': 90}
        cals_3, status_3 = self.staywellAPI.staywell(data, self.userID, actual_db)
        
        data = {'weight': 50, 'workout': 'Tennis', 'minutes': 90}
        cals_4, status_4 = self.staywellAPI.staywell(data, self.userID, actual_db)
        
        assert mock_db.called
        self.assertEqual(status, 200)
        self.assertEqual(status_1, 200)
        self.assertEqual(status_2, 200)
        self.assertEqual(status_3, 200)
        self.assertEqual(status_4, 200)
        self.assertIsNotNone(cals)
        self.assertIsNotNone(cals_1)
        self.assertIsNotNone(cals_2)
        self.assertIsNotNone(cals_3)
        self.assertIsNotNone(cals_4)

if __name__ == '__main__':
    unittest.main()
