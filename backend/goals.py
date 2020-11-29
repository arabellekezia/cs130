from datetime import datetime, date, timedelta
import copy
from backend.db import DB
from typing import Any, List, Dict, Tuple


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
    set_goal()
            Inserts the goal in the database
    get_latest_goal()
            Returns the latest goal depending on the type
    get_all_goals()
            Returns all the goals stored in the goals table
    get_type_goals()
            Returns all the goals of a particular type
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
        self._database_manager = database_manager
        self._user_id = user_id
        self._table_name = 'Goals'
        self._params = ['Type', 'Value', 'Datetime', 'UserID']
    
    def _get_params(self, params):
        if len(params) == 1:
            return params[0]
        params_string = ''
        for p in params:
            params_string += p + ', '
        params_string = params_string[:-2]
        return params_string
    
    def set_goal(self, input_dict: Dict, input_dict_keys: List[str] = ['Type', 'Value'], input_dict_types: Dict[str, Any] = {'Type': str,'Value': float}) -> bool:
        """Inserts input in the database. Returns true if success o/w false
    
        Parameters
        ----------
        input_dict : dict
            The input dictionary with keys 'input_dict_keys' i.e. Type, Value
        input_dict_keys : dict
            The keys of 'input_dict'
        input_types: list
            List with the data types of input_dict
                    
        Returns
        -------
        bool
            returns true if entry is without errors o/w false
        """ 
        for k in input_dict.keys():

            if k not in input_dict_keys:
                return False

            if ((input_dict_types[k] is not None) and (not isinstance(input_dict[k],input_dict_types[k]))):
                return False
            
        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self._user_id
        
        try:
            self._database_manager.insert_row_1(self._table_name, data_dict)
            return True
        except:
            return False 
        
    def get_latest_goal(self, Type: str) -> (List[Dict], bool):
        """Gets the latests goal of type Type from the goal table.
    
        Parameters
        ----------
        Type : str
            Calories, FitnessMinutes, SleepHours
                    
        Returns
        -------
        list
            Returns a the latest goal from the table of type 'Type' in a list. The elements of the list are dictionaries.
        bool
            true if database query succesful, false otherwise
        """ 
            
        query = f"SELECT {self._get_params(self._params)} FROM {self._table_name}\
        join Users on Users.id={self._table_name}.UserID\
        WHERE Goals.Type = '{Type}' AND Users.id = '{self._user_id}'\
        ORDER BY Datetime DESC LIMIT 1;"        
        try:
            result = self._database_manager.select_data(query)
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].timestamp())
                return result, True
            else:
                return None, False
        except:
            return None, False

    def get_all_goals(self) -> (List[Dict], bool):
        """Gets all the goal of from the goal table.
    
        Parameters
        ----------
                    
        Returns
        -------
        list
            Returns all the goals from the table in a list. The elements of the list are dictionaries.
        bool
            true if database query succesful, false otherwise 
        """ 
        query = (f"select {self._get_params(self._params)} from {self._table_name} "
                 f"join Users on Users.id={self._table_name}.UserID "
                 f"where Users.id = '{self._user_id}';")
        try:
            result = self._database_manager.select_data(query)
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].timestamp())
                return result, True
            else:
                return None, False
        except:
            return None, False

    def get_type_goals(self, Type: str) -> (List[Dict], bool):
        """Gets all the goal of type Type of from the goal table.
    
        Parameters
        ----------
        Type : char
            D for Diet (Cals), F for Fitness (Minutes), S for Sleep (Minutes)
                    
        Returns
        -------
        list
            Returns all the goals from the table of type Type in a list. The elements of the list are dictionaries.
        bool
            true if database query succesful, false otherwise
        """ 
        query = (f"select {self._get_params(self._params)} from {self._table_name} "
                 f"join Users on Users.id={self._table_name}.UserID "
                 f"where Users.id = '{self._user_id}' and Goals.Type = '{Type}';")
        try:
            result = self._database_manager.select_data(query)
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].timestamp())
                return result, True
            else:
                return None, False
        except:
            return None, False

    def alter_goal(self, goal_type: str, value: float, type_list: List = ['Calories', 'FitnessMinutes', 'SleepHours']) -> bool:
        if goal_type not in type_list:
            return False
        if not isinstance(value, float):
            return False
        cmd = f"UPDATE Goals SET Value = {value} where UserID = {self._user_id} and Type = '{goal_type}';"
        try:
            self._database_manager.insert_data(cmd)
            return True
        except:
            return False
