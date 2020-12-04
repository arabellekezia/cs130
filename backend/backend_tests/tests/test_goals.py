import unittest
from backend.db import DB
from backend.user import User
from backend.goals import Goals

class TestGoals(unittest.TestCase):
    """
    Test for goals.py
    """

    @classmethod
    def setUpClass(self):
        """
        Set up the unit test.
        """
        self.db = DB()
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        self.fullname = 'ABCD'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password, self.fullname)
        self.user_id = self.user.check_email_match(self.email)
        
        self.goals = Goals(self.db, self.user_id)
        self.diet_goal_dict = {'Type': 'Calories', 'Value': 1000.0}
        self.fitness_goal_dict = {'Type': 'FitnessMinutes', 'Value': 100.0}
        self.sleep_goal_dict = {'Type': 'SleepHours', 'Value': 10.0}
        
        self.goals.set_goal(self.diet_goal_dict)
        self.goals.set_goal(self.fitness_goal_dict)
        self.goals.set_goal(self.sleep_goal_dict)
        
    def test_alter_goal(self):
        """
        Test altering a goal. Change all the goals and check for correctness.
        """
        self.assertTrue(self.goals.alter_goal('Calories', 99.0))
        self.assertTrue(self.goals.alter_goal('FitnessMinutes', 50.0))
        self.assertTrue(self.goals.alter_goal('SleepHours', 1.99))
        goal, status = self.goals.get_latest_goal(Type='Calories')
        self.assertEqual(goal[0]['Value'], 99.0)
        goal, status = self.goals.get_latest_goal(Type='FitnessMinutes')
        self.assertEqual(goal[0]['Value'], 50.0)
        goal, status = self.goals.get_latest_goal(Type='SleepHours')
        self.assertEqual(goal[0]['Value'], 1.99)
        
        goals = Goals(None, self.user_id)
        self.assertFalse(goals.alter_goal('Calories', 99.0))

    def test_incorrect_alter_type_goal(self):
        """
        Test for incorrect alter type. The function alter_goal() should return False.
        """ 
        self.assertFalse(self.goals.alter_goal('CaloriesS', 99.0))
        self.assertFalse(self.goals.alter_goal('FitnessMinutesS', 50.0))
        self.assertFalse(self.goals.alter_goal('SleepHoursS', 1.99))

        
    def test_incorrect_alter_value_type_goal(self):
        """
        Test for incorrect alter value data type.
        """
        self.assertFalse(self.goals.alter_goal('Calories', 'A'))
        self.assertFalse(self.goals.alter_goal('FitnessMinutes', 50))
        self.assertFalse(self.goals.alter_goal('SleepHours', 'B'))
                
    def test_get_latest_goal(self):
        """
        Test getting the latest goal of a particular type, Diet, Fitness or Sleep.
        """
        goal, status = self.goals.get_latest_goal(Type='Calories')
        self.assertTrue(status)
        goal, status = self.goals.get_latest_goal(Type='FitnessMinutes')
        self.assertTrue(status)
        goal, status = self.goals.get_latest_goal(Type='SleepHours')
        self.assertTrue(status)
        
        goals = Goals(None, self.user_id)
        goal, status = goals.get_latest_goal(Type='Calories')
        self.assertFalse(status)
        
    def test_incorrect_get_latest_goal(self):
        """
        Test incorrect goal type while getting the latest goal of a particular type.
        """
        goal, status = self.goals.get_latest_goal(Type='A')
        self.assertFalse(status)
        
    def test_get_all_goals(self):
        """
        Test getting all the goals from the table.
        """
        goals, status = self.goals.get_all_goals()
        self.assertTrue(status)
        
        goals = Goals(None, self.user_id)
        goal, status = goals.get_all_goals()
        self.assertFalse(status)
        
    def test_get_type_goals(self):
        """
        Test getting all the goals of a particular type. Mostly we will only be interested in the latest goal.
        """
        goal, status = self.goals.get_type_goals('Calories')
        self.assertTrue(status)
        
        goals = Goals(None, self.user_id)
        goal, status = goals.get_type_goals('Calories')
        self.assertFalse(status)
        
    def test_incorrect_get_type_goals(self):
        """
        Test for incorrect goal type while getting all the goals of a particular type. Mostly we will only be interested in the latest goal.
        """
        goal, status = self.goals.get_type_goals('A')
        self.assertFalse(status)
        
    def test_set_goal(self):
        """
        Test setting a goal. Set all the three goals, Diet, Fitness and Sleep.
        """
        self.assertTrue(self.goals.set_goal(self.diet_goal_dict))
        self.assertTrue(self.goals.set_goal(self.fitness_goal_dict))
        self.assertTrue(self.goals.set_goal(self.sleep_goal_dict))
        
        goals = Goals(None, self.user_id)
        self.assertFalse(goals.set_goal(self.diet_goal_dict))

    def test_incorrect_key_set_goal(self):
        """
        Test for incorrect keys. We send incorrect keys: Typo and Valuo. These keys are the columns in our tables.
        """
        d = {'Typo': 'Calories', 'Valuo': 100.0}
        self.assertFalse(self.goals.set_goal(d))
        
    def test_incorrect_value_type_set_goal(self):
        """
        Test for incorrect value data types. We use int for the Value instead of float (in python) and double (in mysql).
        """
        d = {'Type': 'Calories', 'Value': 100}
        self.assertFalse(self.goals.set_goal(d))

if __name__ == '__main__':
    unittest.main()
