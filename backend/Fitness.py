from backend.Health import Health
import copy
from datetime import datetime
from backend.db import DB
from typing import List, Dict, Any

class Fitness(Health):
    """
    A class used to represent Fitness
    
    Inherits the Health class.

    ...

    Attributes
    ----------
    params_fitness : list of strings
        Columns to query from the fitness table for a get request. Data from all the columns is not required to 
        for different features of our app. For instance we dont need the user email/password.

    Methods
    -------
    get_columns_give_range()
        Returns data from fitness between a given date-time range.
    insert_in_database()
    """
    
    def __init__(self, database_manager: DB, user_id: int) -> None:
        """
        Initializes the fitness class.
        
        Parameters
        ----------
        params_fitness : list of strings
        Columns to query from the fitness table for a get request. Data from all the columns is not required to 
        for different features of our app. For instance we dont need the user email/password.
        """
        self._params_fitness = ['WorkoutType', 'Minutes', 'CaloriesBurned', 'Datetime', 'UserID']
        super().__init__(database_manager, user_id, 'Fitness', self._params_fitness)
    
    def insert_in_database(self, input_dict: Dict,\
                          input_dict_keys: List[str] = ['WorkoutType', 'Minutes', 'CaloriesBurned'],\
                          input_dict_types: Dict[str, Any] = {'WorkoutType': str, 'Minutes': float, 'CaloriesBurned': float},\
                          date_time: datetime = None) -> bool:
        """Inserts input in the database. Returns True if the insertion is successful otherwise False. The 'input_dict' contains
        the workout type, workout duration in minutes and the amount of calories burned.

        Parameters
        ----------
        input_dict : dict
            The input dictionary with keys 'input_dict_keys' i.e. 'WorkoutType', 'Minutes', 'CaloriesBurned'
        input_dict_keys : list of strings
            The keys of 'input_dict'.
        input_dict_types : dict
            The datatypes of the input_dict.
        date_time : datetime
            Manually entering the date-time for the workout. Useful while testing the code.
            
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
        
        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self._user_id
        if date_time is None:
            data_dict['Datetime'] = datetime.utcnow()
        else:
            data_dict['Datetime'] = date_time

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            return False
