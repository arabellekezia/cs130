from datetime import datetime, date, timedelta, timezone
import copy
from backend.db import DB
from typing import Any, List, Dict, Tuple, Optional


class Goals():
    """
    A class used to represent Goals.

    ...

    Attributes
    ----------
    _database_manager : DB
        The database manager.
    _user_id : int
        The unique user id.
    _table_name : str
        The name of the goal table.
    _params : List[str]
        Column names for the goal table useful for the frontend.

    Methods
    -------
    set_goal(input_dict: Dict, input_dict_keys: List[str], input_dict_types: Dict[str, Any]) -> bool
        Inserts goals in the database.
    get_latest_goal(Type: str) -> Tuple[List[Dict], bool]
        Returns the latest goal depending on the type.
    get_all_goals() -> Tuple[List[Dict], bool]
        Returns all the goals stored in the goals table.
    get_type_goals(Type: str) -> Tuple[List[Dict], bool]
        Returns all the goals of a particular type.
    alter_goals(goal_type: str, value: flaot, type_list: List[str]) -> bool
        Change the goals.
    _get_params(params: List[str]) -> str
        Concatenates a list of string with comma separation which will be useful 
        for querying the database. (Private member method)
    """
    def __init__(self, database_manager: DB, user_id: int) -> None:
        """
        Initialize the goal class.
        
        Parameters
        ----------
        database_manager : DB
            The database manager.
        user_id : int
            The unique user id.
        """
        self._database_manager = database_manager
        self._user_id = user_id
        self._table_name = 'Goals'
        self._params = ['Type', 'Value', 'Datetime', 'UserID']
    
    def _get_params(self, params: List[str]) -> str:
        """
        Converts a list of strings (subset of column names of the goals table) into a string which can be used to query the database.
        
        Parameters
        ----------
        params : List[str]
            List of a subset of columns of the table 'table_name' for which data is returned given a get query.
            
        Returns
        -------
        params_string : str
            Returns a string which is used to query the database.
        
        """
        params_string = ''
        for p in params:
            params_string += p + ', '
        params_string = params_string[:-2]
        return params_string
    
    def set_goal(self, input_dict: Dict[Any], input_dict_keys: Optional[List[str]] = ['Type', 'Value'],\
                 input_dict_types: Optional[Dict[str, Any]] = {'Type': str,'Value': float}) -> bool:
        """
        Inserts input in the database. Returns true if success otherwise false
    
        Parameters
        ----------
        input_dict : Dict[Any]
            The input dictionary with keys 'input_dict_keys' i.e. Type, Value
        input_dict_keys : Optional[List[str]]
            The keys of 'input_dict' in a List, defaults to field names in the Goals table.
        input_types: Optional[Dict[str, Any]]
            List with the data types of input_dict, defaults to fields and types for the Goals table.
                    
        Returns
        -------
        success : bool
            Returns True if entry is without errors otherwise False.
        """ 
        for k in input_dict.keys():

            if k not in input_dict_keys:
                return False

            if ((input_dict_types[k] is not None) and (not isinstance(input_dict[k],input_dict_types[k]))):
                return False
            
        data_dict = copy.deepcopy(input_dict)
        data_dict['UserID'] = self._user_id
        data_dict['Datetime'] = datetime.utcnow() 
        
        try:
            self._database_manager.insert_row_1(self._table_name, data_dict)
            return True
        except:
            return False 
        
    def get_latest_goal(self, Type: str) -> Tuple[Any, bool]:
        """
        Gets the latests goal of type Type from the goal table.
    
        Parameters
        ----------
        Type : str
            Calories, FitnessMinutes, SleepHours -> Types of Goals
                    
        Returns
        -------
        result : Tuple[Any, bool]
            Returns the latest goal from the table of type 'Type' in a list, None if no goal, or -1 if there
            is an issue with the query. The second part of the tuple is a bool for whether or not the query was
            successful.
        """ 
            
        query = f"SELECT {self._get_params(self._params)} FROM {self._table_name}\
        join Users on Users.id={self._table_name}.UserID\
        WHERE Goals.Type = '{Type}' AND Users.id = '{self._user_id}'\
        ORDER BY Datetime DESC LIMIT 1;"        
        try:
            result = self._database_manager.select_data(query)
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].replace(tzinfo=timezone.utc).timestamp())
                return result, True
            else:
                return None, False
        except:
            return -1, False

    def get_all_goals(self) -> Tuple[Any, bool]:
        """
        Gets all the goal of from the goal table.
                    
        Returns
        -------
        result : Tuple[Any, bool]
            Returns all goals from the table in a list, None if no goal, or -1 if there is an issue with the query.
            The second part of the tuple is a bool for whether or not the query was successful.
        """ 
        query = (f"select {self._get_params(self._params)} from {self._table_name} "
                 f"join Users on Users.id={self._table_name}.UserID "
                 f"where Users.id = '{self._user_id}';")
        try:
            result = self._database_manager.select_data(query)
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].replace(tzinfo=timezone.utc).timestamp())
                return result, True
            else:
                return None, False
        except:
            return -1, False

    def get_type_goals(self, Type: str) -> Tuple[Any, bool]:
        """
        Gets all the goal of type Type of from the goal table.
    
        Parameters
        ----------
        Type : str
            Calories for Diet (Cals), FitnessMinutes for Fitness (Minutes), SleepHours for Sleep (Minutes).
                    
        Returns
        -------
        result : Tuple[Any, bool]
            Returns all goals from the table of type 'Type' in a list, None if no goal, or -1 if there is an issue
            with the query. The second part of the tuple is a bool for whether or not the query was successful.
        """ 
        query = (f"select {self._get_params(self._params)} from {self._table_name} "
                 f"join Users on Users.id={self._table_name}.UserID "
                 f"where Users.id = '{self._user_id}' and Goals.Type = '{Type}';")
        try:
            result = self._database_manager.select_data(query)
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].replace(tzinfo=timezone.utc).timestamp())
                return result, True
            else:
                return None, False
        except:
            return -1, False

    def alter_goal(self, goal_type: str, value: float, \
       type_list: Optional[List[str]] = ['Calories', 'FitnessMinutes', 'SleepHours']) -> bool:
        """
        Change the existing goals.
        
        Parameters
        ----------
        goal_type : str
            The type of goal to be changed, Diet, Fitness or Sleep.
        value : float
            The new goal value.
        type_list : List[str]
            List of the three types of goals.
        
        Returns
        -------
        success : bool
            Returns True if the goal is changed successfully, otherwise False.
        """
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
