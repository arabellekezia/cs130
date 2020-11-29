from backend.Health import Health
import copy
from datetime import datetime
from backend.db import DB
from typing import List, Dict, Any

class Fitness(Health):
    """
    A class used to represent Diet

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
        """
        Parameters
        ----------
        database_manager : DB
            The database manager 
        user_id : int
            The unique user id
        table_name : str
            The name of the table
        """
        self._fitness_params = ['WorkoutType', 'Minutes', 'CaloriesBurned', 'Datetime', 'UserID']
        super().__init__(database_manager, user_id, 'Fitness', self._fitness_params)
    
    def insert_in_database(self, input_dict: Dict,\
                          input_dict_keys: List[str] = ['WorkoutType', 'Minutes', 'CaloriesBurned'],\
                          input_dict_types: Dict[str, Any] = {'WorkoutType': str, 'Minutes': int, 'CaloriesBurned': float}) -> bool:
        """Inserts input in the database. Returns true if success o/w false

        Parameters
        ----------
        input_dict : dict
            The input dictionary with keys 'input_dict_keys' i.e. 'WorkoutType', 'Minutes', 'CaloriesBurned'
        input_dict_keys : dict
            The keys of 'input_dict'
        input_dict_types : dict
            The datatypes of the input_dict
            
        Returns
        -------
        bool
            returns true if entry is without errors o/w false
        """    
        for k in input_dict.keys():
            
            if k not in input_dict_keys:
                return False
            
            if ((input_dict_types[k] is not None) and (not isinstance(input_dict[k],input_dict_types[k]))):
                return False
        
        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self._user_id
        data_dict['Datetime'] = datetime.now()

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            return False
        
    def insert_in_database_datetime(self, input_dict: Dict, date_time: datetime,\
                          input_dict_keys: List[str] = ['WorkoutType', 'Minutes', 'CaloriesBurned'],\
                          input_dict_types: Dict[str,Any] = {'WorkoutType': str, 'Minutes': int, 'CaloriesBurned': float}) -> bool:
        """Inserts input in the database. Returns true if success o/w false

        Parameters
        ----------
        input_dict : dict
            The input dictionary with keys 'input_dict_keys' i.e. 'WorkoutType', 'Minutes', 'CaloriesBurned'
        input_dict_keys : dict
            The keys of 'input_dict'
        input_dict_types : dict
            The datatypes of the input_dict
        date_time : datetime
            Manually entering the datetime
            
        Returns
        -------
        bool
            returns true if entry is without errors o/w false
        """    
        for k in input_dict.keys():
            
            if k not in input_dict_keys:
                return False
            
            if ((input_dict_types[k] is not None) and (not isinstance(input_dict[k],input_dict_types[k]))):
                return False
        
        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self._user_id
        data_dict['Datetime'] = date_time

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            return False
