from datetime import datetime, date, timedelta

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
 
    def __init__(self, database_manager, user_id, table_name='Goals'):
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
        super().__init__()
    
    def set_goal(self, goal_dict, goal_dict_keys=['Type', 'Value']):
        """Inserts input in the database. Returns true if success o/w false
    
        Parameters
        ----------
        goal_dict : dict
            The input dictionary with keys 'goal_dict_keys' i.e. Type, Value
        goal_dict_keys : dict
            The keys of 'goal_dict'
                    
        Returns
        -------
        bool
            returns true if entry is without errors o/w false
        """  
        ct = 0
        for k in goal_dict.keys():
            if k not in goal_dict_keys:
                ct += 1
        assert ct == 0
        
        goal_dict['Datetime'] = datetime.now()
        goal_dict['UserID'] = self.__user_id
        
        try:
            self.__database_manager.insert_row(self.__table_name, goal_dict)
            return True
        except:
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
            
        query = f"SELECT * FROM {self.__table_name}\
        join Users on Users.id={self.__table_name}.UserID\
        WHERE Type = {Type} AND UserID = {self.__user_id}\
        ORDER BY Date DESC LIMIT 1"

        try:
            return self.__database_manager.select_date(query), True
        except:
            None, False