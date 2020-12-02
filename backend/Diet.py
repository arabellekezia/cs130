from backend.Health import Health
from datetime import datetime
import copy
from backend.db import DB
from typing import List, Dict, Any

class Diet(Health):
    """
    A class used to represent Diet. 
    
    Inherits the Health class.

    ...

    Attributes
    ----------
    params_diet : list of strings
        Columns to query from the diet table for a get request. Data from all the columns is not required to 
        for different features of our app. For instance we dont need the user email/password.

    Methods
    -------
    get_columns_give_range()
        Returns data from the diet table between a given date-time range.
    insert_in_database()
        Inserts the input into the diet table.
    """
    def __init__(self, database_manager: DB, user_id: int) -> None:
        """
        Initializes the diet class.
        
        Parameters
        ----------
        params_diet : list of strings
        Columns to query from the diet table for a get request. Data from all the columns is not required to 
        for different features of our app. For instance we dont need the user email/password.
        
        """
        self._params_diet = ['Item', 'ServingSize', 'Cals', 'Protein', 'Carbs', 'Fat', 'Fiber', 'Barcode', 'Datetime', 'UserID']
        super().__init__(database_manager, user_id, 'Diet', self._params_diet)
        
    def insert_in_database(self, input_dict: Dict,\
                           input_dict_keys: List[str] = ['Item', 'ServingSize', 'Barcode', 'nutri_dict'],\
                           nutri_dict_keys: List[str] = ['Cals','Protein','Fat','Carbs','Fiber'],\
                           input_dict_types: Dict[str, Any] = {'Item': str,'ServingSize': float,'Barcode': bool,'nutri_dict': None},\
                           nutri_dict_types: Dict[str, Any] = {'Cals': float,'Protein': float,'Fat': float,'Carbs': float,'Fiber': float},\
                           date_time: datetime = None,
                           ) -> bool:
        """Inserts input in the database. Returns True if insertion is successful otherwise returns False. The input_dict consists of the
        item label, serving size, barcode indicator and the nutrient dictionary for the item which either comes from the api or throught manual entry.

        Parameters
        ----------
        input_dict : dict
            The input dictionary with keys 'input_dict_keys' i.e. Item, ServingSize, Barcode, nutri_dict
            input_dict['nutri_dict'] is another dictionary with keys 'nutri_dict_keys'.
        input_dict_keys : list of strings
            The keys of 'input_dict'. Used for checking the keys before entering it in the database.
        nutri_dict_keys : list of strings
            Keys of the nutrient dictionary in 'input_dict'. Used for the checking the correct nutrients.
        input_dict_types: dict
            Datatypes of input_dict. Used for checking the data types of the input.
        nutri_dict_types: dict
            Datatypes of nutri_dict. Usef for checking the data types of the nutrients.
        date_time : datetime
            Manually entering the data-time for the item entry. Useful while testing the code.
            
        Returns
        -------
        success : bool
            Returns True if a successful entry is made to the Diet table without errors, otherwise False.
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
