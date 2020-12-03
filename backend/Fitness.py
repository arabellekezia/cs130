from backend.Health import Health
import copy
from datetime import datetime
from backend.db import DB
from typing import List, Dict, Any, Tuple, Optional

class Fitness(Health):
    """
    A class used to represent Fitness
    
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
        Returns data from the fitness table between a given date-time range.
    insert_in_database(input_dict: Dict, input_dict_keys: List[str], input_dict_types: Dict[str, Any],date_time: datetime) -> bool
        Inserts the fitness entry in the fitness table.
    """
    
    def __init__(self, database_manager: DB, user_id: int,
                 params_fitness: Optional[List[str]] = ['WorkoutType', 'Minutes', 'CaloriesBurned', 'Datetime', 'UserID']) -> None:
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
                          input_dict_keys: Optional[List[str]] = ['WorkoutType', 'Minutes', 'CaloriesBurned'],
                          input_dict_types: Optional[Dict[str, Any]] = {'WorkoutType': str, 'Minutes': float, 'CaloriesBurned': float},
                          date_time: Optional[datetime] = None) -> bool:
        """
        Inserts input in the database. Returns True if the insertion is successful otherwise False. The 'input_dict' contains
        the workout type, workout duration in minutes and the amount of calories burned.

        Parameters
        ----------
        input_dict : Dict
            The input dictionary with fields and values that need to be entered into the database for the Fitness table.
        input_dict_keys : Optional[List[str]]
            The keys of the input_dict, these correspond to fields in the Fitness table. Defaulted to a List of all the fields.
        input_dict_types : Optional[Dict[str, Any]]
            The fields and corresponding data types in the Fitness table, defaulted to the schema of the table.
        date_time : Optional[datetime]
            Manually entered datetime for the workout entry, defaults to None since the database is configured to use
            CURRENT_TIMESTAMP when one is not provided.
            
        Returns
        -------
        success : bool
            Returns True if the database entry is successful without any errors, False otherwise.
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
