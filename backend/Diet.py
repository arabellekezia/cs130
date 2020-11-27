from Health import Health
from datetime import datetime, date, timedelta
import copy

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
    def __init__(self, database_manager, user_id):
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
        
    def insert_in_database(self, input_dict,\
                           input_dict_keys=['Item', 'ServingSize', 'Barcode', 'nutri_dict'],\
                           nutri_dict_keys=['Cals','Protein','Fat','Carbs','Fiber'],\
                           input_dict_types=[str,float,bool,None],\
                           nutri_dict_types=[float,float,float,float,float]
                           ):
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
            returns true if entry is without errors o/w false
        """    
        ct = 0
        for (k,t) in zip(input_dict.keys(),input_dict_types):
            if k not in input_dict_keys or ((t is not None) and (not isinstance(input_dict[k],t))):
                ct+=1
        if ct > 0:
            print(f'1. INCORRECT INPUT DICTIONARY KEYS OR INCORRECT DATATYPE FOR TABLE {self._table_name}')
            return False
        if ct == 0:
            for (k,t) in zip(input_dict['nutri_dict'].keys(),nutri_dict_types):
                if k not in nutri_dict_keys or not isinstance(input_dict['nutri_dict'][k],t):
                    ct+=1
        if ct > 0:
            print(f'2. INCORRECT INPUT DICTIONARY KEYS OR INCORRECT DATATYPE FOR TABLE {self._table_name}')
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
        
        
    def insert_in_database_datetime(self, input_dict, date_time,\
                           input_dict_keys=['Item', 'ServingSize', 'Barcode', 'nutri_dict'],\
                           nutri_dict_keys=['Cals','Protein','Fat','Carbs','Fiber'],\
                           input_dict_types=[str,float,bool,None],\
                           nutri_dict_types=[float,float,float,float,float]
                           ):
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
            Manually entring the Datetime, instead of doing datetime.now()
            
        Returns
        -------
        bool
            returns true if entry is without errors o/w false
        """    
        ct = 0
        for (k,t) in zip(input_dict.keys(),input_dict_types):
            if k not in input_dict_keys or ((t is not None) and (not isinstance(input_dict[k],t))):
                ct+=1
        if ct > 0:
            print(f'1. INCORRECT INPUT DICTIONARY KEYS OR INCORRECT DATATYPE FOR TABLE {self._table_name}')
            return False
        if ct == 0:
            for (k,t) in zip(input_dict['nutri_dict'].keys(),nutri_dict_types):
                if k not in nutri_dict_keys or not isinstance(input_dict['nutri_dict'][k],t):
                    ct+=1
        if ct > 0:
            print(f'2. INCORRECT INPUT DICTIONARY KEYS OR INCORRECT DATATYPE FOR TABLE {self._table_name}')
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
