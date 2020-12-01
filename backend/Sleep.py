from Health import Health
from datetime import datetime, date, timedelta
from db import DB
import copy

class Sleep(Health):
    def __init__(self, database, user_id):
        super().__init__(database, user_id, 'Sleep')


    # Input dict will have keys: SleepTime, WakeupTime
    # Table columns: UserID, Date, SleepTime, WakeupTime, Minutes (sleep duration)
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
            # Make sure we get all the valid keys
            if k not in input_key_list():
                return False

        # Get the duration given sleep/ wake up time in minutes
        duration = input_dict['WakeupTime'] - input_dict['SleepTime']
        d_mins = divmod(duration.seconds, 60)[0]

        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self.__user_id
        data_dict['Minutes'] = d_mins

        try:
            self.__database.insert_row(self.__table_name,data_dict)
            return True
        except:
            print(f"insert_in_database: could not make an entry in {self.__table_name} for {data_dict}")
            return False


    def get_columns_given_range(self, startDate, endDate):
        # Description:
        # Returns all Sleep data from startDate to endDate

        # Input:
        # startDate : datetime
        # endDate : datetime

        # Output:
        # Returns all column data containing :
        # Date, SleepTime, WakeupTime, Minutes

        query = (f"SELECT * FROM {self.__table_name} "
                 f"join Users on Users.id={self.__table_name}.UserID "
                 f"WHERE Users.id = {self.__user_id} AND WakeupTime BETWEEN "
                 f"'{str(startDate)} 00:00:00' AND '{str(endDate)} 00:00:00';"

        try:
            data = self.__database.select_data(query)
            return data_dict, True
        except:
            return "get_data_range: error getting data from database", False
