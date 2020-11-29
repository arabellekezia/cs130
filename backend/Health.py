from abc import ABC, abstractmethod
from backend.db import DB
from datetime import datetime
from typing import List, Dict
import copy

class Health(ABC):
    """
    A class used to represent Health

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
 
    def __init__(self, database_manager: DB, user_id: int, table_name: str) -> None:
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
        self._table_name = table_name
        
        
    def get_columns_given_range(self, start_date: datetime, end_date: datetime) -> (List[Dict], bool):
        """Returns the columns from the database given date range. Returns
        columns, true if the start_date, end_date is correct o/w false.

        Parameters
        ----------
        start_date : datetime
            The start date
        end_date : datetime
            The end date

        Returns
        -------
        list
            a list of tuples from 'start_date' to 'end_date' from '_table_name'. Each element of the list is a dictionary.
        bool
            true if database query succesful, false otherwise
        """
        try:
            result = self._database_manager.sel_time_frame(self._table_name, f"{start_date}", f"{end_date}", self._user_id)
            if result:
                for r in result:
                    r['Datetime'] = int(r['Datetime'].timestamp())
                return result, True
            else:
                return None, False
        except:
            return None, False
    
    @abstractmethod
    def insert_in_database(self, input_dict):
        """Inserts input in the database. Returns true if success o/w false

        Parameters
        ----------
        input_dict : dict
        """
        pass
