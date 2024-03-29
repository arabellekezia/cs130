from abc import ABC, abstractmethod
from backend.db import DB
from datetime import datetime, timezone
from typing import Any, List, Dict, Optional, Tuple
import copy

class Health(ABC):
    """
    A class used to represent the user Health.
    
    The main abstract class for our app which is inherited by the three major components: Diet, Fitness, and Sleep.

    ...

    Attributes
    ----------
    _database_manager : DB
        The database manager. (Private member variable)
    _user_id : int
        The unique user id. (Private member variable)
    _table_name : str
        The name of the table which stores data for a particular aspect of health: Diet, Fitness, Sleep. (Private member variable)
    _params : List[str]
        List of strings corresponding to the columns of table 'table_name'. The frontend does not require all
        the columns from the database, for instance, user name or email is not required for computing the total calories/sleep duration etc. (Private member variable)

    Methods
    -------
    get_columns_give_range(start_date : datatime, end_date : datetime) -> Tuple[List[Dict], bool]
        Returns data from table 'table_name' given between a start and end date. The exact type of data (list of dictionaries) 
        depends on the health component.  
    insert_in_database(input_dict : Dict) -> bool
        Abstract method. Inserts the input into the table 'table_name' in the database.
    _get_params(params : List[str]) -> str
        Converts a list of column names to a string which is used to query the database. (Private member method)
    """
 
    def __init__(self, database_manager: DB, user_id: int, table_name: str, params: Optional[str] = ["*"]) -> None:
        """
        Initializes the attributes.
        
        Parameters
        ----------
        database_manager : DB
            The database manager. 
        user_id : int
            The unique user id.
        table_name : str
            The name of the table.
        params : Optional[List[str]]
            List of the columns from table 'table_name', defaults to all fields in any table.
        """

        self._database_manager = database_manager
        self._user_id = user_id
        self._table_name = table_name
        self._params = params
        
    def _get_params(self, params: List[str]) -> str:
        """
        Converts a list of strings (subset of column names of table 'table_name') into a string which can be used to query the database.
        For example, given input ['Datetime', 'Cals', 'Protein'], the function returns 'Datetime, Cals, Protein'. (Private member method)
        
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
    
    def get_columns_given_range(self, start_date: datetime, end_date: datetime) -> Tuple[Any, bool]:
        """
        Gets data from table 'table_name' between 'start_date' and 'end_date'.

        Parameters
        ----------
        start_date : datetime
            The start date.
        end_date : datetime
            The end date.

        Returns
        -------
        result : Tuple[Any, bool]
            Returns a list of dictionaries corresponding to database rows between 'start_date' to 'end_date' from table
            'table_name', None if no entries, and -1 if there is an error. The second part of the tuple returns True if
            the query is succesful, False otherwise.
        """
        try:
            result = self._database_manager.sel_time_frame(self._table_name, f"{start_date}", f"{end_date}", self._user_id, params=self._get_params(self._params)) 
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].replace(tzinfo=timezone.utc).timestamp())
                return result, True
            else:
                return None, False
        except:
            return -1, False
    
    @abstractmethod
    def insert_in_database(self, input_dict) -> bool:
        """
        Inserts input in the database. Returns true if success o/w false.
        This is an Abstract method which is implemented by the individual components, Diet, Fitness, Sleep.

        Parameters
        ----------
        input_dict : dict
            Fields and values for the table to insert data into.

        Returns
        -------
        success : bool
            Whether or not the entry was able to be inserted in the database.
        """
        pass
