from backend.Health import Health
from datetime import date, datetime
import copy
from typing import List, Dict, Any
from backend.db import DB

class Sleep(Health):
    """
    A class used to represent Sleep

    ...

    Attributes
    ----------
    database_manager : DB
        the database manager
    user_id : int
        the unique user id
    table_name : str
        the name of the table for that aspect of health, like Diet, Fitness, Sleep

    Methods
    -------
    get_columns_give_range()
        Returns the columns from the table 'table_name' for a given time range
    insert_in_database()
        Inserts the input into the database
    """
    def __init__(self, database_manager: DB, user_id: int) -> None:
        super().__init__(database_manager, user_id, 'Sleep')


    def insert_in_database(self, input_dict: Dict,\
                          input_dict_keys: List[str] = ['SleepTime', 'WakeupTime', 'Nap'],\
                          input_dict_types: Dict[str,Any] = {'SleepTime': datetime,'WakeupTime': datetime,'Nap': bool}) -> bool:

        for k in input_dict.keys():
            
            if k not in input_dict_keys:
                return False
            
            if ((input_dict_types[k] is not None) and (not isinstance(input_dict[k],input_dict_types[k]))):
                return False

        duration = input_dict['WakeupTime'] - input_dict['SleepTime']
        d_mins = divmod(duration.seconds, 60)[0]

        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self._user_id
        data_dict['Minutes'] = d_mins
        data_dict['Datetime'] = datetime.now()

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            return False
        
    def insert_in_database_datetime(self, input_dict: Dict,date_time: datetime,\
                          input_dict_keys: List[str] = ['SleepTime', 'WakeupTime', 'Nap'],\
                          input_dict_types: Dict[str,Any] = {'SleepTime': datetime,'WakeupTime': datetime,'Nap': bool}) -> bool:

        for k in input_dict.keys():
            
            if k not in input_dict_keys:
                return False
            
            if ((input_dict_types[k] is not None) and (not isinstance(input_dict[k],input_dict_types[k]))):
                return False

        duration = input_dict['WakeupTime'] - input_dict['SleepTime']
        d_mins = divmod(duration.seconds, 60)[0]

        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self._user_id
        data_dict['Minutes'] = d_mins
        data_dict['Datetime'] = date_time

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            return False
            
    def get_columns_given_range(self, startDate: datetime, endDate: datetime) -> (List[Dict], bool):


        query = (f"SELECT * FROM {self._table_name} "\
                 f"join Users on Users.id={self._table_name}.UserID "\
                 f"WHERE Users.id = {self._user_id} AND WakeupTime BETWEEN "\
                 f"'{str(startDate)}' AND '{str(endDate)}';")

        try:
            result = self._database_manager.select_data(query)
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].timestamp())
                    r['SleepTime'] = int(r['SleepTime'].timestamp())
                    r['WakeupTime'] = int(r['WakeupTime'].timestamp())
                return result, True
            else:
                return None, False
        except:
            return None, False
