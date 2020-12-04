from backend.Health import Health
import copy
from datetime import datetime
from backend.db import DB
from typing import List, Dict, Any, Tuple, Optional

PARAMS_FITNESS = ['WorkoutType', 'Minutes', 'CaloriesBurned', 'Datetime', 'UserID']
INPUT_KEYS = ['WorkoutType', 'Minutes', 'CaloriesBurned']
INPUT_TYPES = {'WorkoutType': str, 'Minutes': float, 'CaloriesBurned': float}

class Fitness(Health):
    """
    A class used to represent users Fitness, monitor workout and track the caloried burned.
    
    Inherits the Health class.

    ...

    Attributes
    ----------
    _database_manager : DB
        The database manager. (Private member variable)
    _user_id : int
        The unique user id. (Private member variable)
    _table_name : str
        The PyMySQL table name for Fitness. (Private member variable.) 
    _params : List[str]
        List of strings corresponding to the columns of the fitness table. The frontend does not require all the columns
        from the fitness table, for instance, user name or email is not required for computing the total workout minutes. (Private member variable)

    Methods
    -------
    get_columns_give_range(start_date: datetime, end_date: datatima) -> Tuple[List[Dict],bool]
        Returns data from the fitness table between a given date-time range. Useful for computing the daily and weekly statistics.
    insert_in_database(input_dict: Dict, date_time: datetime) -> bool
        Inserts the fitness entry (workout, calories burned etc) into the fitness table.
    """
    
    def __init__(self, database_manager: DB, user_id: int,
                 params_fitness: Optional[List[str]] = PARAMS_FITNESS) -> None:
        """
        Initializes the fitness class.
        
        Parameters
        ----------
        database_manager: DB
            The database manager
        user_id: int
            The unique user id
        params_fitness: Optional[List[str]]
            The list of columns from the Fitness table required by the frontend. Defaults to all fields of the Fitness table.
        """
        super().__init__(database_manager, user_id, 'Fitness', params_fitness)
    
    def insert_in_database(self, input_dict: Dict,
                          date_time: Optional[datetime] = None) -> bool:
        """
        Inserts the workout input in the database. Returns True if the insertion is successful otherwise False. 
        The 'input_dict' (workout session) contains the workout type, workout duration in minutes and the amount of calories burned.

        Parameters
        ----------
        input_dict : Dict
            The input dictionary with fields and values that need to be entered into the database for the Fitness table.
        date_time : Optional[datetime]
            Manually entered datetime for the workout entry, defaults to None since the database is configured to use
            current timestamp when 'date_time' is not provided. This is useful for testing the fitness class.
            
        Returns
        -------
        success : bool
            Returns True if the database entry is successful without any errors, False otherwise.
        """    
        for k in input_dict.keys():
            
            if k not in INPUT_KEYS:
                return False
            
            if ((INPUT_TYPES[k] is not None) and (not isinstance(input_dict[k], INPUT_TYPES[k]))):
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
