import unittest
from backend.db import DB
from backend.user import User
from backend.goals import Goals

# goals_table_command = ("CREATE TABLE Goals "
#                      "(Type varchar(50), Value DOUBLE, "
#                      "Datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UserID INT(11) UNSIGNED, FOREIGN KEY (UserID) "
#                      "REFERENCES Users(id));")

class TestGoals(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DB()
        
        self.email = 'abc@gmail.com'
        self.password = 'defghi'
        
        self.user = User(self.db)
        self.user.create_new_user(self.email, self.password)
        self.user_id = self.user.check_email_match(self.email)
        
#         try:
#             self.db.insert_data('Drop table Goals')
#         except:
#             pass
#         self.db.insert_data(goals_table_command)
        
        self.goals = Goals(self.db, self.user_id)
        self.diet_goal_dict = {'Type': 'Calories', 'Value': 1000.0}
        self.fitness_goal_dict = {'Type': 'FitnessMinutes', 'Value': 100.0}
        self.sleep_goal_dict = {'Type': 'SleepHours', 'Value': 10.0}
        
        self.goals.set_goal(self.diet_goal_dict)
        self.goals.set_goal(self.fitness_goal_dict)
        self.goals.set_goal(self.sleep_goal_dict)
        
    def test_alter_goal(self):
        """
        Test altering a goal
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

    def test_incorrect_alter_type_goal(self):
        """
        Test for incorrect alter type.
        """
        print('Test incorrect alter type')
        self.assertFalse(self.goals.alter_goal('CaloriesS', 99.0))
        self.assertFalse(self.goals.alter_goal('FitnessMinutesS', 50.0))
        self.assertFalse(self.goals.alter_goal('SleepHoursS', 1.99))
        print("")

        
    def test_incorrect_alter_value_type_goal(self):
        """
        Test for incorrect alter value type.
        """
        print('Test incorrect alter value data type')
        self.assertFalse(self.goals.alter_goal('Calories', 'A'))
        self.assertFalse(self.goals.alter_goal('FitnessMinutes', 50))
        self.assertFalse(self.goals.alter_goal('SleepHours', 'B'))
        print('')
                
    def test_get_latest_goal(self):
        """
        Test getting the latest goal of a particular type.
        """
        print('Latest Goals')
        goal, status = self.goals.get_latest_goal(Type='Calories')
        print(goal)
        self.assertTrue(status)
        goal, status = self.goals.get_latest_goal(Type='FitnessMinutes')
        print(goal)
        self.assertTrue(status)
        goal, status = self.goals.get_latest_goal(Type='SleepHours')
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
        goal, status = self.goals.get_type_goals('Calories')
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
        print('Test incorrect set type')
        d = {'Typo': 'Calories', 'Valuo': 100.0}
        self.assertFalse(self.goals.set_goal(d))
        print("")
        
    def test_incorrect_value_type_set_goal(self):
        """
        Test for incorrect value types. We use int for the Value instead of float (in python) and double (in mysql).
        """
        print('Incorrect set value data type')
        d = {'Type': 'Calories', 'Value': 100}
        self.assertFalse(self.goals.set_goal(d))
        print("")

if __name__ == '__main__':
    unittest.main()
