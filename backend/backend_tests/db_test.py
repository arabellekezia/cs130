import unittest
from db import DB

class TestDB(unittest.TestCase):
    def setUp(self):
        self._db = DB()

    def setting_up_db(self):
        cmd = "CREATE TABLE TestingTable (
    

    def test_select_with_results(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_select_no_results(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_select_fail(self):

    def test_insert_cmd_success(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_insert_cmd_fail(self):

if __name__ == '__main__':
    unittest.main()
