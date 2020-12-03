from backend.Health import Health
from datetime import datetime
import copy
from backend.db import DB
from typing import List, Dict, Any, Tuple, Optional

class Diet(Health):
    """
    A class used to represent Diet. 
    
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
        the columns from the database, for instance, user name or email is not required for computing the total calories.

    Methods
    -------
    get_columns_give_range(start_date: datetime, end_date: datatima) -> Tuple[List[Dict],bool]
        Returns data from the diet table between a given date-time range.
    insert_in_database(input_dict: Dict, input_dict_keys: List[str], nutri_dict_keys: List[str], input_dict_types: Dict[str, Any],
                       nutri_dict_types: Dict[str, Any], date_time: datetime) -> bool
        Inserts the input into the diet table.
    """
    def __init__(self, database_manager: DB, user_id: int,
                 params_diet: Optional[List[str]] = ['Item', 'ServingSize', 'Cals', 'Protein', 'Carbs', 'Fat', 'Fiber', 'Barcode', 'Datetime', 'UserID']) -> None:
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
                           input_dict_keys: Optional[List[str]] = ['Item', 'ServingSize', 'Barcode', 'nutri_dict'],
                           nutri_dict_keys: Optional[List[str]] = ['Cals','Protein','Fat','Carbs','Fiber'],
                           input_dict_types: Optional[Dict[str, Any]] = {'Item': str,'ServingSize': float,'Barcode': bool,'nutri_dict': None},
                           nutri_dict_types: Optional[Dict[str, Any]] = {'Cals': float,'Protein': float,'Fat': float,'Carbs': float,'Fiber': float},
                           date_time: Optional[datetime] = None) -> bool:
        """
        Inserts input in the database. Returns True if insertion is successful otherwise returns False. The input_dict consists of the
        item label, serving size, barcode indicator and the nutrient dictionary for the item which either comes from the api or throught manual entry.

        Parameters
        ----------
        input_dict : Dict
            The input dictionary with fields and values that need to be entered into the database for the Diet table.
        input_dict_keys : Optional[List[str]]
            The keys of the input_dict, these correspond to fields in the Diet table. Defaulted to a List of all the fields.
        input_dict_types : Optional[Dict[str, Any]]
            The fields and corresponding data types in the Diet table, defaulted to the schema of the table.
        date_time : Optional[datetime]
            Manually entered datetime for the food entry, defaults to None since the database is configured to use
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
                
        for k in input_dict['nutri_dict'].keys():
            
            if k not in nutri_dict_keys:
                return False
        
            if not isinstance(input_dict['nutri_dict'][k],nutri_dict_types[k]):
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
