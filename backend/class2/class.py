import db.py as db
from time import datetime
from abc import ABC

class Health(abc):

    def __init__(self, type, db, data_table, goal_table, user):
        self.type = type
        self.db = db
        self.data_table = data_table
        self.goal_table = goal_table
        self.user = user
        super().__init__()

    # goals method
    @abstractmethod
    def set_goal(self):
        pass

    @abstractmethod
    def get_goal(self):
        pass

    # data inputs
    @abstractmethod
    def log_data(self, date):
        pass

    @abstractmethod
    def get_weekly_data(self, start_date, end_date):
        pass

    @abstractmethod
    def get_daily_data(self, date):
        # query = go to db and get data for the date
        pass

    @abstractmethod
    def get_month_data(self, start_date, end_date):
        pass


class Sleep(Health):
    def set_goal(self, sleep_goal):
        if sleep_goal <= 0:
            print("Invalid sleep goal")
        # db.insert_row(self, goal_table, self.user
        else:
            if self.goal_table[self.user] == None:
                query = f"INSERT INTO {self.goal_table}(UserID, goal, type) VALUES ({self.user, sleep_goal}, S)"
                db.insert_data(query)
            else:
                # not sure how to execute commands
                del_query = f"DELETE FROM {self.goal_table} WHERE type=S"
                db.execute(del_query)
                query = f"INSERT INTO {self.goal_table}(UserID, goal, type) VALUES ({self.user, sleep_goal}, S)"
                db.insert_data(query)


    def get_goal(self):
        query = f"SELECT {self.user} FROM {self.goal_table} WHERE {type='S'}"
        goal = db.select_data(query)
        return goal

    # {user_id} -> {date, start_time, end_time, duration}
    def log_data(self, date, start_time, end_time):
        duration = wakeup_time - sleep_time
        # query = log date and duration
        query = f"INSERT INTO {self.data_table}(date, start_time, end_time, duration) VALUES ({date, start_time, end_time})"
        db.insert_data(query)

    def get_weekly_data(self, start_date, end_date):
        if self.data_table[self.user] == None:
            print("No data for user {}", self.user)
        query = f"SELECT {self.user}, start_time, end_time, duration FROM {self.data_table} WHERE date>={start_date} && date<={end_date}"
        vals = db.select_data(query)
        return vals

    def get_daily_data(self, date):
        if self.data_table[self.user] == None:
            print("No data for user {}", self.user)
        today = date.today()
        query = f"SELECT {self.user}, start_time, end_time, duration FROM {self.data_table} WHERE date=={today}"
        vals = db.select_data(query)
        return vals

    def get_month_data(self, start_date, end_date):
        if self.data_table[self.user] == None:
            print("No data for user {}", self.user)
        query = f"SELECT {self.user}, start_time, end_time, duration FROM {self.data_table} WHERE date>={start_date} && date<={end_date}"
        vals = db.select_data(query)
        return vals

# class Fitness(Health):

# class Diet(Health):
