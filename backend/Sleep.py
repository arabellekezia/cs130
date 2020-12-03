from backend.Health import Health
from datetime import date, datetime, timezone
import copy
from typing import List, Dict, Any, Tuple, Optional
from backend.db import DB

class Sleep(Health):
    """
    A class used to represent Sleep
    
    Inherits the Health class.

    ...

    Attributes
    ----------
    _database_manager : DB
        The database manager.
    _user_id : int
        The unique user id.
    _table_name : str
        The name of the table which stores data for a particular aspect of health: Diet, Fitness, Sleep.
    _params : List[str]
        List of strings corresponding to the columns of table 'table_name'. The frontend does not require all
        the columns from the database, for instance, user name or email is not required for computing the total workout minutes.

    Methods
    -------
    get_columns_give_range(start_date: datetime, end_date: datatima) -> Tuple[List[Dict],bool]
        Returns data from the sleep table between a given date-time range.
    insert_in_database(input_dict: Dict, input_dict_keys: List[str], input_dict_types: Dict[str, Any], data_time: datetime) -> bool
        Inserts the sleep entry in the sleep table.
    """    
    def __init__(self, database_manager: DB, user_id: int, params_sleep: Optional[List[str]] = ['Minutes', 'Nap',\
                                                  'SleepTime', 'WakeupTime', 'Datetime', 'UserID']) -> None:
        """
        Initializes the sleep class.
        
        Parameters
        ----------
        database_manager: DB
            The database manager
        user_id: int
            The unique user id
        params_sleep: List[str]
            The list of columns from the Sleep table required by the frontend. 
        """
        super().__init__(database_manager, user_id, 'Sleep', params_sleep)


    def insert_in_database(self, input_dict: Dict,\
                          input_dict_keys: Optional[List[str]] = ['SleepTime', 'WakeupTime', 'Nap'],\
                          input_dict_types: Optional[Dict[str,Any]] = {'SleepTime': datetime,'WakeupTime': datetime,'Nap': bool},\
                          date_time: Optional[datetime] = None) -> bool:
        """
        Inserts input in the database. Returns True if the insertion is successful otherwise False. The 'input_dict' contains
        the sleep time, wakeup time and an indicator if the sleep is a nap or a regular night sleep.

        Parameters
        ----------
        input_dict : Dict
            The input dictionary with keys 'input_dict_keys' i.e. 'SleepTime', 'WakeupTime' and 'Nap'
        input_dict_keys : List[str]
            The keys of 'input_dict'.
        input_dict_types : Dict
            The datatypes of the input_dict.
        date_time : datetime
            Manually entering the date-time for the sleep. Useful while testing the code.
            
        Returns
        -------
        success : bool
            Returns True if the database entry is successful without any errors otherwise False
        """    
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
        if date_time is None:
            data_dict['Datetime'] = datetime.utcnow()
        else:
            data_dict['Datetime'] = date_time

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            return False
            
    def get_columns_given_range(self, startDate: datetime, endDate: datetime) -> Tuple[List[Dict], bool]:
        """Gets data from the Sleep table between 'start_date' and 'end_date'. We need to over-write the 
        function from the Health class because for sleep when given a start and end date we find all the
        entries whose wake up time is between the two entries, rather than the the date-time of the database entry.
        This is done because the total sleep in a day can a cumulative sum of all the sleeps with wake up times
        in that day. For instance, when a user wakes up in the morning of Dec 4, we will include that sleep
        for Dec 4, similarly if the user has any naps throughtout that day it will also be included in Dec 4.
        So the wake up time is really useful here.

        Parameters
        ----------
        start_date : datetime
            The start date.
        end_date : datetime
            The end date.

        Returns
        -------
        result : List[Dict]
            A list of dictionaries between 'start_date' to 'end_date' from the Sleep table. 
        success : bool
            Returns True if query succesful, otherwise False.
        """
        query = (f"SELECT {self._get_params(self._params)} FROM {self._table_name} "\
                 f"join Users on Users.id={self._table_name}.UserID "\
                 f"WHERE Users.id = {self._user_id} AND WakeupTime BETWEEN "\
                 f"'{str(startDate)}' AND '{str(endDate)}';")

        try:
            result = self._database_manager.select_data(query)
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].replace(tzinfo=timezone.utc).timestamp())
                    r['SleepTime'] = int(r['SleepTime'].replace(tzinfo=timezone.utc).timestamp())
                    r['WakeupTime'] = int(r['WakeupTime'].replace(tzinfo=timezone.utc).timestamp())
                return result, True
            else:
                return None, False
        except:
            return -1, False
