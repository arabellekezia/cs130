from Health import Health

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
        super().__init__(database, user_id, 'Fitness')
    
    def insert_in_database(self, input_dict,\
                          input_dict_keys = ['WorkoutType', 'Minutes', 'CaloriesBurned']):
        """Inserts input in the database. Returns true if success o/w false

        Parameters
        ----------
        input_dict : dict
            The input dictionary with keys 'input_dict_keys' i.e. 'WorkoutType', 'Minutes', 'CaloriesBurned'
        input_dict_keys : dict
            The keys of 'input_dict'
            
        Returns
        -------
        bool
            returns true if entry is without errors o/w false
        """    
        
        ct = 0
        for k in input_dict.keys():
            if k not in input_dict_keys():
                ct+=1
        assert ct == 0
        
        data_dict = input_dict
        date_dict['UserID'] = self.__user_id
        data_dict['Date'] = datetime.now()

        try:
            self.__database_manager.insert_row(self.__table_name,data_dict)
            return True
        except:
            return False
