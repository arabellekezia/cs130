import unittest
from pymysql.err import ProgrammingError, DataError
from backend.db import DB

class TestDB(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB()
        self.table = "TestingTable"
        cmd = ("CREATE TABLE TestingTable (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
               "name varchar(30), age INT(3));")
        self.db.insert_data(cmd)

    def test_1_insert_cmd_success(self):
        cmd = (f"insert into {self.table} (name, age) values ('Naveena', 21);")
        self.db.insert_data(cmd)

        # this just asserts that we made it this far without an exception being thrown
        self.assertTrue(True)

    def test_2_select_no_results(self):
        query = (f" select * from {self.table} where age = 100;")
        results = self.db.select_data(query)
        self.assertEqual(results, ())

    def test_3_select_with_results(self):
        query = (f" select * from {self.table} where name = 'Naveena';")
        results = self.db.select_data(query)
        self.assertEqual(len(results), 1)
        expected = {'id': 1, 'name': 'Naveena', 'age': 21}
        self.assertDictEqual(results[0], expected)

    def test_4_select_fail(self):
        query = (f" select * from NotExistingTable;")
        with self.assertRaises(ProgrammingError):
            self.db.select_data(query)

    def test_5_insert_cmd_fail(self):
        cmd = (f"insert into {self.table} (name, age) values ('Naveena', 'string');")
        with self.assertRaises(DataError):
            self.db.insert_data(cmd)

    def test_6_insert_row(self):
        data = {'name': "'Lily'", 'age': 1}
        self.db.insert_row(self.table, data)
        query = (f" select * from {self.table} where name = 'Lily';")
        results = self.db.select_data(query)
        self.assertEqual(len(results), 1)
        expected = {'id': 2, 'name': 'Lily', 'age': 1}
        self.assertDictEqual(results[0], expected)
        
    def test_7_insert_row_1(self):
        data = {'name':'ABC', 'age': 10}
        self.db.insert_row_1(self.table,data)
        query = (f" select * from {self.table} where name = 'ABC';")
        results = self.db.select_data(query)
        self.assertEqual(len(results), 1)
        expected = {'id': 3, 'name': 'ABC', 'age': 10}
        self.assertDictEqual(results[0], expected)
        
    def test_8_insert_cmd_success(self):
        cmd = (f"insert into {self.table} (name, age) values (%s, %s);")
        self.db.insert_data_1(cmd, ('DEF', 11))

        # this just asserts that we made it this far without an exception being thrown
        self.assertTrue(True)

    @classmethod
    def tearDownClass(self):
        cmd = "drop table TestingTable;"
        self.db.insert_data(cmd)


if __name__ == '__main__':
    unittest.main()
