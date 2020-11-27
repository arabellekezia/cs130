import sys
sys.path.append("../")
import unittest
from db import DB
from user import User
from goals import Goals

goals_table_command = ("CREATE TABLE Goals "
                     "(Type varchar(50), Value DOUBLE, "
                     "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
                     "REFERENCES Users(id));")

class TestGoals(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB('localhost', 'root', 'softwareengineering130', 'CS130')
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password)
        self.user_id = self.user.check_email_match(self.email)
        
        try:
            self.db.insert_data('Drop table Goals')
        except:
            pass
        self.db.insert_data(goals_table_command)
        
        self.goals = Goals(self.db, self.user_id)
        self.diet_goal_dict = {'Type': 'D', 'Value': 1000.0}
        self.fitness_goal_dict = {'Type': 'F', 'Value': 100.0}
        self.sleep_goal_dict = {'Type': 'S', 'Value': 10.0}
        
        self.goals.set_goal(self.diet_goal_dict)
        self.goals.set_goal(self.fitness_goal_dict)
        self.goals.set_goal(self.sleep_goal_dict)
        
    def test_set_goal(self):
        """
        Test setting a goal
        """
        self.assertTrue(self.goals.set_goal(self.diet_goal_dict))
        self.assertTrue(self.goals.set_goal(self.fitness_goal_dict))
        self.assertTrue(self.goals.set_goal(self.sleep_goal_dict))

    def test_incorrect_key_set_goal(self):
        """
        Test for incorrect keys. We send incorrect keys: Typo and Valuo
        """
        d = {'Typo': 'D', 'Valuo': 100.0}
        self.assertFalse(self.goals.set_goal(d))
        
    def test_incorrect_value_type_set_goal(self):
        """
        Test for incorrect value types. We use int for the Value instead of float (in python) and double (in mysql).
        """
        d = {'Type': 'D', 'Value': 100}
        self.assertFalse(self.goals.set_goal(d))
        
    def test_get_latest_goal(self):
        """
        Test getting the latest goal of a particular type.
        """
        print('Latest Goals')
        goal, status = self.goals.get_latest_goal(Type='D')
        print(goal)
        self.assertTrue(status)
        goal, status = self.goals.get_latest_goal(Type='F')
        print(goal)
        self.assertTrue(status)
        goal, status = self.goals.get_latest_goal(Type='S')
        print(goal)
        self.assertTrue(status)
        print("")
        
    def test_incorrect_get_latest_goal(self):
        """
        Test incorrect goal type while getting the latest goal of a particular type.
        """
        print('Latest Goals Incorrect')
        goal, status = self.goals.get_latest_goal(Type='A')
        print(goal)
        self.assertFalse(status)
        print("")
        
    def test_get_all_goals(self):
        """
        Test getting all the goals from the table.
        """
        goals, status = self.goals.get_all_goals()
        print('All Goals')
        print(goals)
        print("")
        self.assertTrue(status)
        
    def test_get_type_goals(self):
        """
        Test getting all the goals of a particular type. Mostly we will only be interested in the latest goal.
        """
        print('Type Goals')
        goal, status = self.goals.get_type_goals('D')
        print(goal)
        print("")
        self.assertTrue(status)
        
    def test_incorrect_get_type_goals(self):
        """
        Test for incorrect goal type while getting all the goals of a particular type. Mostly we will only be interested in the latest goal.
        """
        print('Type Goals Incorrect')
        goal, status = self.goals.get_type_goals('A')
        print(goal)
        print("")
        self.assertFalse(status)

if __name__ == '__main__':
    unittest.main()