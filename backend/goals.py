from datetime import datetime, date, timedelta
import copy

class Goals():
    """
    A class used to represent Goals

    ...

    Attributes
    ----------
    database_manager : DB
        The database manager
    user_id : int
        The unique user id
    table_name : str
        The name of the goal table

    Methods
    -------
    get_columns_give_range()
        Returns the columns from the table 'table_name' for a given time range
    insert_in_database()
        Inserts the input into the database
    """
 
    def __init__(self, database_manager, user_id: int) -> None:
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
        self._database_manager = database_manager
        self._user_id = user_id
        self._table_name = 'Goals'
    
    def set_goal(self, goal_dict, goal_dict_keys=['Type', 'Value'], goal_types=[str,float]):
        """Inserts input in the database. Returns true if success o/w false
    
        Parameters
        ----------
        goal_dict : dict
            The input dictionary with keys 'goal_dict_keys' i.e. Type, Value
        goal_dict_keys : dict
            The keys of 'goal_dict'
        goal_types: list
            List with the data types of goal_dict
                    
        Returns
        -------
        bool
            returns true if entry is without errors o/w false
        """  
        data_dict = copy.deepcopy(goal_dict)
        ct = 0
        for (k,t) in zip(data_dict.keys(),goal_types):
            if k not in goal_dict_keys or not isinstance(data_dict[k],t):
                ct += 1
        if ct > 0:
            print(f'INCORRECT INPUT DICTIONARY KEYS OR INCORRECT DATATYPE FOR TABLE {self._table_name}')
            return False
        
        data_dict['Datetime'] = datetime.now()
        data_dict['UserID'] = self._user_id
        
        try:
            self._database_manager.insert_row_1(self._table_name, data_dict)
            return True
        except:
            print(f'INSERTION INTO TABLE {self._table_name} UNSUCCESSFUL')
            return False 
        
    def get_latest_goal(self, Type):
        """Gets the latests goal of type Type from the goal table.
    
        Parameters
        ----------
        Type : char
            D for Diet (Cals), F for Fitness (Minutes), S for Sleep (Minutes)
                    
        Returns
        -------
        list
            Returns a the latest goal from the table of type 'Type'
        bool
            true if database query succesful, false otherwise
        """ 
            
        query = f"SELECT * FROM {self._table_name}\
        join Users on Users.id={self._table_name}.UserID\
        WHERE Goals.Type = '{Type}' AND Users.id = '{self._user_id}'\
        ORDER BY Datetime DESC LIMIT 1;"        
        try:
            result = self._database_manager.select_data(query)
            if result:
                return result, True
            else:
                print(f'FETCHING FROM TABLE {self._table_name} UNSUCCESSFUL')
                return None, False
        except:
            print(f'FETCHING FROM TABLE {self._table_name} UNSUCCESSFUL')
            return None, False

    def get_all_goals(self):
        """Gets all the goal of from the goal table.
    
        Parameters
        ----------
                    
        Returns
        -------
        list
            Returns all the goals from the table
        bool
            true if database query succesful, false otherwise
        """ 
        query = (f"select * from {self._table_name} "
                 f"join Users on Users.id={self._table_name}.UserID "
                 f"where Users.id = '{self._user_id}';")
        try:
            result = self._database_manager.select_data(query)
            if result:
                return result, True
            else:
                print(f'FETCHING FROM TABLE {self._table_name} UNSUCCESSFUL')
                return None, False
        except:
            print(f'FETCHING FROM TABLE {self._table_name} UNSUCCESSFUL')
            return None, False

    def get_type_goals(self, Type):
        """Gets all the goal of type goal_type of from the goal table.
    
        Parameters
        ----------
        Type : char
            D for Diet (Cals), F for Fitness (Minutes), S for Sleep (Minutes)
                    
        Returns
        -------
        list
            Returns all the goals from the table of type Type
        bool
            true if database query succesful, false otherwise
        """ 
        query = (f"select * from {self._table_name} "
                 f"join Users on Users.id={self._table_name}.UserID "
                 f"where Users.id = '{self._user_id}' and Goals.Type = '{Type}';")
        try:
            result = self._database_manager.select_data(query)
            if result:
                return result, True
            else:
                print(f'FETCHING FROM TABLE {self._table_name} UNSUCCESSFUL')
                return None, False
        except:
            print(f'FETCHING FROM TABLE {self._table_name} UNSUCCESSFUL')
            return None, False
