from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta

class Health(ABC):
 
    def __init__(self, table_name, goal_table_name, database_manager, user_id):
        self.__table_name = table_name
        self.__goal_table_name = goal_table_name
        self.__database_manager = database_manager
        self.__user_id = user_id
        super().__init__()
    
    # Get the value corresponding to a particular column for a particular date
    # So for diet it could be the value corresonding to a particular nutrient column
    # For fitness it could the Minutes or the CaloriesBurned column
    # While for sleep it will just be the Minutes (the sleep duration)
    @abstractmethod
    def get_value_given_date(self):
        pass
    
    # Get the daily nutrient/exercise? decomposition
    # For diet it will be the nutrient decomposition for that day.
    # For fitness it will be the workout decomposition for that based on all the exercises 
    # done in that day.
    # Basically the Pie Charts
    @abstractmethod
    def get_daily_decomposition(self):
        pass
    
    # API calling function. So for diet it will present the 5 options to the user to select from.
    # Similarly for fitness .....
    @abstractmethod
    def get_from_API(self):
        pass
    
    # Insert the user data into the database after checking for the correctness of the inputs received
    # from the frontend.
    @abstractmethod
    def insert_in_database(self):
        pass
    
    def get_daily_value(self, column):
        
        # Description:
        # Useful for the main page where we show total values for different aspects of health.
        # Calories for health, Active time for workout and duration for sleep. Returns the daily value.
        
        # Input: 
        # column (STRING): this could be 'Cals' for diet, or 'Minutes' for fitness
        
        # Output: 
        # Float value
        
        todays_date = date.today()
        try:
            return self.get_value_given_date(column, todays_date)
        except ValueError:
            print('No entry has been for today')
    
        
    def get_values_range(self, column, date, duration):
        
        # Description: 
        # Useful for making the weekly and monthly (if we are doing it) charts.
        # Just need to pass the start date and the duration, and it computes the 
        # values corresponding to a particular column for that duration.
        
        # Input:
        # column (STRING): corresonding column in the database, 
        # for instance 'Cals' for diet or 'Minutes' for fitness
        # date (DATE): python date, not datetime
        # duration (INT): the number of days before the given date. So for instance
        # for weekly date duration will be 7 and we will compute (date-7, date)
        
        # Output:
        # Returns a dictionary with the dates of that duration (date-duration, date) as the keys and the 
        # corresponding column value as the values of the dictionary.
        
        data_dict = {}
        for i in range(duration):
            dt = date - timedelta(days=i)
            # Handles the case when the number of entries in the database is less than the duration.
            try:
                data_dict[str(dt)] = self.get_value_given_date(column, dt)
            except:
                if data_dict:
                    return data_dict
                else:
                    raise ValueError('No entry has been made yet.')
        return data_dict
    
    def get_weekly_values(self, column):
        
        # Description:
        # Weekly values for a particular column.
        # Just call the previous function with duration = 7
        
        # Input:
        # column (STRING): For example 'Cals' for diet or 'Minutes or CaloriesBurned' for fitness
        
        # Output:
        # Returns a dictionary with the keys as the dates of the last week and the corresponding 
        # column values as the dictionary values.
        
        try:
            return self.get_values_range(column, date.today(), 28)
        except ValueError:
            print('Week has not yet been completed.')
            
            
    # This could be the change which people want in IH. So this may not be a part of our App.
    def get_monthly_values(self, column):
        
        # Description:
        # Weekly values for a particular column.
        # Just call the previous function with duration = 8
        
        # Input:
        # column (STRING):
        
        # Output:
        # Returns a dictionary with the keys as the dates of the last week and the corresponding 
        # column values.
        
        try:
            return self.get_values_range(column, date.today(), 28)
        except ValueError:
            print('Month has not yet been completed.')
    
    # Inserts the user goals data into the goals database.
    # Common function across all the three features as the goals table is also common.
    # Goals table will have columns: UserID, Type (corresponding to D, F, S) and Value (Float) which
    # corresponds to Calories for diet, Active time for fitness and a
    
    def set_goals(self, goal_dict):
        # Description: 
        # Makes a new entry in the goal table. We will receive Type and the Value from the goal_dict
        # and the Date and UserID will be manually added in this file.
        # 
        # Input:
        # Dictionary with keys: Type (which corresonds to D, F, S), and the Value
        # So for diet we will have calories, fitness we have active time and for sleep we have duration.
        #
        # Output:
        # Returns True if we set the goal correctly otherwise False
        
        input_key_list = ['Type', 'Value']
        ct = 0
        for k in goal_dict.keys():
            if k not in input_key_list:
                ct += 1
        assert ct == 0
        
        # Add Date and UserID to the dictionary before saving it in the database.
        goal_dict['Datetime'] = datetime.now()
        goal_dict['UserID'] = self.__user_id
        
        try:
            self.__database.insert_row(self.__goal_table_name, goal_dict)
            return True
        except:
            return False 
        
    def get_goals(self, Type):
    
    # Description:
    # Returns the latest goal of Type Type from the goal database.
    #
    # Input:
    # Type (CHAR): D,F,S
    #
    # Output:
    # Dictionary with key: Type and the corresponding value.
        
        query = f"SELECT Value FROM {self.__goal_table_name}\
        join Users on Users.id={self.__goal_table_name}.UserID\
        WHERE Type = {Type} ORDER BY Date DESC LIMIT 1"

        try:
            records = self.__database.select_date(query)
            goal_out_dict = {Type: records[0][0]}
            return goal_out_dict
        except ValueError:
            print(f"{Type} Goal not yet set")