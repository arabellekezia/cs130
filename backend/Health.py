from abc import ABC, abstractmethod
from db import DB

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
 
    def __init__(self, database_manager, user_id, table_name):
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
        self.__database_manager = database_manager
        self.__user_id = user_id
        self.__table_name = table_name

    def get_columns_given_range(self, start_date, end_date):
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
            a list of tuples from 'start_date' to 'end_date' from '__table_name'
        bool
            true if database query succesful, false otherwise
        """
        try:
            return self.__database_manager.sel_time_frame(self.__table_name, start_date, end_date, self.__user_id), True
        except:
            None, False
    
    @abstractmethod
    def insert_in_database(self, input_dict):
        """Inserts input in the database. Returns true if success o/w false

        Parameters
        ----------
        input_dict : dict
        """
        pass
