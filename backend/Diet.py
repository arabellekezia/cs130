from backend.Health import Health
from datetime import datetime
import copy
from backend.db import DB
from typing import List, Dict, Any, Tuple, Optional

PARAMS_DIET = ['Item', 'ServingSize', 'Cals', 'Protein', 'Carbs', 'Fat', 'Fiber', 'Barcode', 'Datetime', 'UserID']
INPUT_KEYS = ['Item', 'ServingSize', 'Barcode', 'nutri_dict']
NUTRI_KEYS = ['Cals','Protein','Fat','Carbs','Fiber']
INPUT_TYPES = {'Item': str,'ServingSize': float,'Barcode': bool,'nutri_dict': None}
NUTRI_TYPES = {'Cals': float,'Protein': float,'Fat': float,'Carbs': float,'Fiber': float}

class Diet(Health):
    """
    A class used to represent a users ndiet. 
    
    Inherits the Health class.

    ...

    Attributes
    ----------
    _database_manager : DB
        The database manager. (Private member variable)
    _user_id : int
        The unique user id. (Priavte member variance)
    _table_name : str
        The PyMySQL table name for Diet. (Priavate member variable)
    _params : List[str]
        List of strings corresponding to the columns of the diet table. The frontend does not require all the
        columns from the database, for instance, username/email is not required for computing the total calories. (Private member variable)

    Methods
    -------
    get_columns_give_range(start_date: datetime, end_date: datatima) -> Tuple[List[Dict],bool]
        Returns data from the diet table between a given date-time range. Useful for computing the daily and weekly nutritional values.
    insert_in_database(input_dict: Dict, date_time: datetime) -> bool
        Inserts the user meal with its nutritional values into the diet table.
    """
    def __init__(self, database_manager: DB, user_id: int,
                 params_diet: Optional[List[str]] = PARAMS_DIET) -> None:
        """
        Initializes the diet class.
        
        Parameters
        ----------
        database_manager: DB
            The database manager
        user_id: int
            The unique user id
        params_diet: Optional[List[str]]
            The list of columns from the Diet table required by the frontend, this defaults to all of the fields in the Diet table.
        """
        super().__init__(database_manager, user_id, 'Diet', params_diet)
        
    def insert_in_database(self, input_dict: Dict,
                           date_time: Optional[datetime] = None) -> bool:  
        """
        Inserts a user meal along with its nutritional contents in the database. Returns True if insertion is successful otherwise returns False. 
        The input_dict (user meal) consists of the item label, serving size, barcode indicator and the nutrient dictionary for the item. The nutrients
        are obtained using the Edamam API either through a string query look-up or a barcode scan.

        Parameters
        ---------- 
        input_dict : Dict
            The input dictionary corresponding to a user meal including the nutritional value of the meal.
        date_time : Optional[datetime]
            Manually entered datetime for a meal entry, defaults to None since the database is configured to use
            current timestamp when 'date_time' is not provided. This is useful for testing the backend methods.
        
        Returns
        -------
        success : bool 
            Returns True if the database entry is successful without any errors, False otherwise.
        """    
        for k in input_dict.keys():
            
            if k not in INPUT_TYPES:
                return False
            
            if ((INPUT_TYPES[k] is not None) and (not isinstance(input_dict[k],INPUT_TYPES[k]))):
                return False
                
        for k in input_dict['nutri_dict'].keys():
            
            if k not in NUTRI_KEYS:
                return False
        
            if not isinstance(input_dict['nutri_dict'][k],NUTRI_TYPES[k]):
                return False
        
        data_dict = copy.deepcopy(input_dict)
        del data_dict['nutri_dict']
        data_dict['UserID'] = self._user_id
        if date_time is None:
            data_dict['Datetime'] = datetime.utcnow()
        else:
            data_dict['Datetime'] = date_time
        
        for k in input_dict['nutri_dict'].keys():
            data_dict[k] = input_dict['nutri_dict'][k]

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            return False
