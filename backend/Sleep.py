from Health import Health
from datetime import datetime, date, timedelta
import json

class Sleep(Health):
    def __init__(self, database, user_id):
        super().__init__(database, user_id, 'Sleep')


    # Input dict will have keys: SleepTime, WakeupTime
    # Table columns: UserID, Date, SleepTime, WakeupTime, Duration (in mins)
    def insert_in_database(self, input_dict):

        # Description:
        # Inserts the input from the front end in the table.
        #
        # Input:
        # input_dict (Dictionary): input dictionary from the user, described above
        #
        # Output:
        # Returns True if the entry is correctly made
        # Else returns False

        input_key_list = ['SleepTime', 'WakeupTime']

        ct = 0
        for k in input_dict.keys():
            if k not in input_key_list():
                ct + =1

        # Make sure we get all the valid keys
        assert ct == 0

        # Get the duration given sleep/ wake up time in minutes
        duration = input_dict['WakeupTime'] - input_dict['SleepTime']
        d_mins = divmod(duration.seconds, 60)[0]

        data_dict = input_dict
        data_dict['UserID'] = self.__user_id
        data_dict['Duration'] = d_mins

        try:
            self.__database.insert_row(self.__table_name,data_dict)
            return True
        except:
            print(f"insert_in_database: could not make an entry in {self.__table_name} for {data_dict}")

    def get_columns_given_range(self, startDate, endDate):
        # Description:
        # Unlike get_values_range - this returns the whole dataset
        # including sleep/ wake up time and not just duration
        # The date range is based on WakeupTime:
        # (i.e. for startDate <= WakeupTime <= endDate)

        # Input:
        # startDate (DATE): python date, not datetime
        # endDate (DATE): python date, not datetime

        # Output:
        # Returns all column data containing :
        # Date, SleepTime, WakeupTime, Duration

        query = (f"SELECT * FROM {self.__table_name} "
                 f"join Users on Users.id={self.__table_name}.UserID "
                 f"WHERE Users.id = {self.__user_id} AND WakeupTime BETWEEN "
                 f"'{str(startDate)} 00:00:00' AND '{str(endDate)} 00:00:00';"

        try:
            data = self.__database.select_data(query)
            data_dict = json.loads(data)
            return data_dict, True
        except:
            return "get_data_range: error getting data from database", False

    # def get_daily_sleep_data(self):
    #     # Description: g
    #     # Returns a dictionary with all sleep logs for today
    #     #
    #     # Input:
    #     #
    #     # Output:
    #     # Returns a dictionary with first level keys: 0,1,2 corresponding to the number of
    #     # workouts done for the day. Second level keys: WorkoutType, Minutes, CaloriesBurned
    #     # and Time. As mentioned in the FrontEnd Outline diagram.
    #
    #     todays_date = date.today()
    #     try:
    #         return get_data_range(todays_date, todays_date)
    #     except ValueError:
    #         print(f"get_daily_sleep_data: no data logged today")

    # def get_value_given_date(self, date):
    #
    #     # Description:
    #     # Returns the total sleep duration for a particular day
    #     # This is calculated based on the date the person wakes up
    #
    #     # Input:
    #     # given_date(DATE): python date, not datetime
    #
    #     # Output:
    #     # Float value
    #
    #     # Note that WakeupTime replaces Date from the previous queries. Because all the sleeps
    #     # which end on a particular day will contribute to the sleep duration for that day.
    #
    #     query = f"SELECT Duration FROM {self.__table_name}\
    #             join Users on Users.id={self.__table_name}.UserID\
    #             WHERE WakeupTime >= '{str(date)} 00:00:00'\
    #             AND UserID = {self.__user_id}"
    #
    #     try:
    #         records = self.__database.select_data(query)
    #         time = 0
    #         load_rec = json.loads(records)
    #         input_key_list = ['Duration']
    #
    #         ct = 0
    #         for k in input_dict.keys():
    #             if k not in input_key_list():
    #                 ct + =1
    #
    #         # Make sure we get all the valid keys
    #         assert ct == 0
    #         for r in records:
    #             time += r['Duration']
    #         return time
    #
    #     except ValueError:
    #         # THe user may not nap everyday. So for nap we will just return 0, if no entry if found
    #         # But the user will sleep daily, so we raise an error if that is not found.
    #         print("get_value_given_date: no data for given date")
    #
    #
    # def get_daily_value(self):
    #
    #     # Description:
    #     # Useful for the summary page/main page where we show total sleep time.
    #
    #     # Output:
    #     # Returns the total sleep time for today.
    #
    #     todays_date = date.today()
    #     try:
    #         return self.get_value_given_date(todays_date)
    #     except ValueError:
    #         print("get_daily_value: no data entered for today")
    #
    #
    # def get_values_range(self, date, duration):
    #
    #     # Description:
    #     # Useful for making the weekly and monthly (if we are doing it) charts.
    #     # Just need to pass the start date and the duration, and it computes the
    #     # total sleep duration for each date in the time frame of duration
    #
    #     # Input:
    #     # date (DATE): python date, not datetime
    #     # duration (INT): the number of days before the given date. So for instance
    #     # for weekly date duration will be 7 and we will compute (date-7, date)
    #
    #     # Output:
    #     # Returns a dictionary with the dates of that duration (date-duration, date) as the keys and the
    #     # corresponding total sleep durations as the values of the dictionary.
    #
    #     sleep_dict = {}
    #     for i in range(duration):
    #         dt = date - timedelta(days=i)
    #         try:
    #             sleep_dict[str(dt)] = self.get_value_given_date(dt)
    #         except:
    #             # If for some reasons we can't get all the data for some of the dates,
    #             # function tells us what dates it successfully got the data from (for debugging)
    #             if sleep_dict:
    #                 print(f"get_values_range: data obtained from {date} to {dt}")
    #                 return sleep_dict
    #             else ValueError:
    #                 raise ValueError(f"get_values_range: no entry has been made for {dt}")
    #     return sleep_dict
    #
    #
    # def get_weekly_values(self):
    #
    #     # Description:
    #     # Weekly values for sleep duration.
    #     # Just call the previous function with duration = 7
    #
    #     # Output:
    #     # Returns a dictionary with the keys as the dates of the last week and
    #     # the corresponding sleep duration
    #     try:
    #         return self.get_values_range(date.today(), 7)
    #     except ValueError:
    #         print("get_weekly_values: error getting weekly values")
    #
    #
    # def get_monthly_values(self):
    #
    #     # Description:
    #     # Get sleep duration for one month back (28 days or 4 weeks)
    #
    #     # Output:
    #     # Returns a dictionary with the keys as the dates of the last month and
    #     # the corresponding sleep duration
    #
    #     try:
    #         return self.get_values_range(date.today(), 28)
    #     except ValueError:
    #         print("get_weekly_values: error getting monthly values")
