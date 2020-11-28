from backend.Health import Health
from datetime import datetime
import copy
from backend.db import DB
from typing import List, Dict, Any

class Diet(Health):
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
        super().__init__(database_manager, user_id, 'Diet')
        
    def insert_in_database(self, input_dict: Dict,\
                           input_dict_keys: List[str] = ['Item', 'ServingSize', 'Barcode', 'nutri_dict'],\
                           nutri_dict_keys: List[str] = ['Cals','Protein','Fat','Carbs','Fiber'],\
                           input_dict_types: Dict[str, Any] = {'Item': str,'ServingSize': float,'Barcode': bool,'nutri_dict': None},\
                           nutri_dict_types: Dict[str, Any] = {'Cals': float,'Protein': float,'Fat': float,'Carbs': float,'Fiber': float}
                           ) -> bool:
        """Inserts input in the database. Returns true if success o/w false

        Parameters
        ----------
        input_dict : dict
            The input dictionary with keys 'input_dict_keys' i.e. Item, ServingSize, Barcode, nutri_dict
            input_dict['nutri_dict'] is another dictionary with keys 'nutri_dict_keys'
        input_dict_keys : dict
            The keys of 'input_dict'
        nutri_dict_keys : dict
            Keys of the dictionary in 'input_dict'
        input_dict_types:
            Datatypes of input_dict
        nutri_dict_types:
            Datatypes of nutri_dict
            
        Returns
        -------
        bool
            Returns True if a successful entry is made to the Diet table without errors.
        """    
        for k in input_dict.keys():
            
            if k not in input_dict_keys:
                print(f'1. INCORRECT INPUT DICTIONARY KEYS FOR TABLE {self._table_name}')
                return False
            
            if ((input_dict_types[k] is not None) and (not isinstance(input_dict[k],input_dict_types[k]))):
                print(f'1. INCORRECT INPUT DATA TYPE FOR TABLE {self._table_name}')
                return False
                
        for k in input_dict['nutri_dict'].keys():
            
            if k not in nutri_dict_keys:
                print(f'2. INCORRECT INPUT DICTIONARY KEYS FOR TABLE {self._table_name}')
                return False
        
            if not isinstance(input_dict['nutri_dict'][k],nutri_dict_types[k]):
                print(f'2. INCORRECT INPUT DATA TYPE FOR TABLE {self._table_name}')
                return False
        
        data_dict = copy.deepcopy(input_dict)
        del data_dict['nutri_dict']
        data_dict['UserID'] = self._user_id
        data_dict['Datetime'] = datetime.now()
        
        for k in input_dict['nutri_dict'].keys():
            data_dict[k] = input_dict['nutri_dict'][k]

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            print(f'INSERTION INTO TABLE {self._table_name} UNSUCCESSFUL')
            return False
        
        
    def insert_in_database_datetime(self, input_dict: Dict, date_time: datetime,\
                           input_dict_keys: List[str] = ['Item', 'ServingSize', 'Barcode', 'nutri_dict'],\
                           nutri_dict_keys: List[str] = ['Cals','Protein','Fat','Carbs','Fiber'],\
                           input_dict_types: Dict[str, Any] = {'Item': str,'ServingSize': float,'Barcode': bool,'nutri_dict': None},\
                           nutri_dict_types: Dict[str, Any] = {'Cals': float,'Protein': float,'Fat': float,'Carbs': float,'Fiber': float}
                           ) -> bool:
        """Inserts input in the database. Returns true if success o/w false

        Parameters
        ----------
        input_dict : dict
            The input dictionary with keys 'input_dict_keys' i.e. Item, ServingSize, Barcode, nutri_dict
            input_dict['nutri_dict'] is another dictionary with keys 'nutri_dict_keys'
        input_dict_keys : dict
            The keys of 'input_dict'
        nutri_dict_keys : dict
            Keys of the dictionary in 'input_dict'
        input_dict_types:
            Datatypes of input_dict
        nutri_dict_types:
            Datatypes of nutri_dict
        date_time:
            Manually entering the date time. Useful while testing the fetching code.
            
        Returns
        -------
        bool
            returns true if entry is without errors o/w false
        """    
        for k in input_dict.keys():
            
            if k not in input_dict_keys:
                print(f'1. INCORRECT INPUT DICTIONARY KEYS FOR TABLE {self._table_name}')
                return False
            
            if ((input_dict_types[k] is not None) and (not isinstance(input_dict[k],input_dict_types[k]))):
                print(f'1. INCORRECT INPUT DATA TYPE FOR TABLE {self._table_name}')
                return False
                
        for k in input_dict['nutri_dict'].keys():
            
            if k not in nutri_dict_keys:
                print(f'2. INCORRECT INPUT DICTIONARY KEYS FOR TABLE {self._table_name}')
                return False
        
            if not isinstance(input_dict['nutri_dict'][k],nutri_dict_types[k]):
                print(f'2. INCORRECT INPUT DATA TYPE FOR TABLE {self._table_name}')
                return False
        
        data_dict = copy.deepcopy(input_dict)
        del data_dict['nutri_dict']
        data_dict['UserID'] = self._user_id
        data_dict['Datetime'] = date_time
        
        for k in input_dict['nutri_dict'].keys():
            data_dict[k] = input_dict['nutri_dict'][k]

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            print(f'INSERTION INTO TABLE {self._table_name} UNSUCCESSFUL')
            return False
