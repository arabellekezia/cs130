from Health import Health
import copy
from datetime import datetime, date, timedelta

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
        super().__init__(database_manager, user_id, 'Fitness')
    
    def insert_in_database(self, input_dict,\
                          input_dict_keys = ['WorkoutType', 'Minutes', 'CaloriesBurned'],\
                          input_dict_types = [str, int, float]):
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
        ct = 0
        for (k,t) in zip(input_dict.keys(),input_dict_types):
            if k not in input_dict_keys or ((t is not None) and (not isinstance(input_dict[k],t))):
                ct+=1
        if ct > 0:
            print(f'1. INCORRECT INPUT DICTIONARY KEYS OR INCORRECT DATATYPE FOR TABLE {self._table_name}')
            return False
        
        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self._user_id
        data_dict['Datetime'] = datetime.now()

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            print(f'INSERTION INTO TABLE {self._table_name} UNSUCCESSFUL')
            return False
        
    def insert_in_database_datetime(self, input_dict,date_time,\
                          input_dict_keys = ['WorkoutType', 'Minutes', 'CaloriesBurned'],\
                          input_dict_types = [str, int, float]):
        """Inserts input in the database. Returns true if success o/w false

        Parameters
        ----------
        input_dict : dict
            The input dictionary with keys 'input_dict_keys' i.e. 'WorkoutType', 'Minutes', 'CaloriesBurned'
        input_dict_keys : dict
            The keys of 'input_dict'
        input_dict_types : dict
            Datatypes of input_dict
        date_time: datetime
            Manually entering the Datetime, instead of using datetime.now()
            
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
        
        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self._user_id
        data_dict['Datetime'] = date_time

        try:
            self._database_manager.insert_row_1(self._table_name,data_dict)
            return True
        except:
            print(f'INSERTION INTO TABLE {self._table_name} UNSUCCESSFUL')
            return False
