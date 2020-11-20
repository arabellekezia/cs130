from Health import Health
from datetime import datetime, date, timedelta
# API function call for StayWell

class Fitness(Health):
    
    def __init__(self, table_name, goal_table_name, database, user_id):
        self.__table_name = table_name
        self.__goal_table_name = goal_table_name
        self.__database = database
        self.__user_id = user_id
        
    def get_value_given_date(self, column, given_date):
        
        # Description: 
        # Takes exercise/workout type as input for instance running and a date and returns the
        # total active time for that workout type.
        
        # Input:
        # column (STRING): Minutes, CaloriesBurned
        # given_date(DATE): python date, not datetime
        
        # Output:
        # Float value
        
        next_date = given_date + timedelta(days=1)
        
        query = f"SELECT {column} FROM {self.__table_name}\
                join Users on Users.id={self.__table_name}.UserID\
                WHERE Datetime >= '{str(given_date)} 00:00:00' AND\
                Datetime <= '{str(next_date)} 00:00:00' AND UserID = {self.__user_id}"

        try:
            # If you can find the corresponding date in the database return the total 
            # active time for the exercise, otherwise just return 0
            records = self.__database_manager.select_data(query)
            active_time = 0
            for r in records:
                active_time += r[0] 
            return active_time
        except ValueError:
            print(f"No entry for {given_date} {ex_type}")
            # TODO
            # OR SHOULD WE RAISE AN ERROR INSTEAD OF RETURNING 0?
#             return 0
            
    def get_daily_decomposition(self, column): 
        
        # Description:
        # Useful for the fitness page where we show the daily percentage breakup.
        # So basically we could give the percentage of the exercises the user performed that day.
        # Unlike diet, we dont fix the nutrient list. Instead we scan throught all the exercise
        # done in a particular day and look for the unique entries and just return the total for each
        # in the form of a dictionary.
        
        # Input:
        # column (STRING): Minutes, CaloriesBurned
        
        # Output:
        # Returns a dictionary with keys as the the exercise type and the corresponding active time as the value.
        
        
        todays_date = date.today()
        next_date = todays_date + timedelta(days=1)
        
        query = f"SELECT WorkoutType, {column} FROM {self.__table_name}\
                join Users on Users.id={self.__table_name}.UserID\
                WHERE Datetime >= '{str(todays_date)} 00:00:00' AND\
                Datetime <= '{str(next_date)} 00:00:00' AND UserID = {self.__user_id}"

        try:
            ex_type_list = []
            active_time_list = []
            # If you can find the corresponding date in the database return the total 
            # active time for the exercise, otherwise just return 0
            records = self.__database_manager.select_data(query)
            active_time = 0
            for r in records:
                ex_type_list.append(r[0])
                active_time_list.append(r[1])
                
            ex_type_set = set(ex_type_list)
            ex_decom = {}
            for ex in ex_type_set:
                at = 0
                for  e,a in zip(ex_type_list, active_time_list):
                    if ex == e:
                        at += a
                ex_decom[ex] = at
                    
            total = sum([ex_decom[k] for k in ex_decom.keys()])
            for ex in ex_decom.keys():
                ex_decom[ex]/=total
            return ex_decom

        except ValueError:
            print(f"No entry for today")
            
    def get_daily_workout_list(self):
        # Description: 
        # Returns a dictionary with all the workouts for today. See FrontEnd Outline point 5, c, iii
        # This can then be just displaed with cards.
        # 
        # Input:
        #
        # Output: 
        # Returns a dictionary with first level keys: 0,1,2 corresponding to the number of 
        # workouts done for the day. Second level keys: WorkoutType, Minutes, CaloriesBurned
        # and Time. As mentioned in the FrontEnd Outline diagram.
        
        todays_date = date.today()
        next_date = todays_date + timedelta(days=1)
        
        query = f"SELECT WorkoutType, Minutes, CaloriesBurned, Date, FROM {self.__table_name}\
                join Users on Users.id={self.__table_name}.UserID\
                WHERE Datetime >= '{str(todays_date)} 00:00:00' AND\
                Datetime <= '{str(next_date)} 00:00:00' AND UserID = {self.__user_id}"

        try:
            todays_dict = {}
            records = self.__database_manager.select_data(query)
            for i,r in enumerate(records):
                todays_dict[i] = {}
                todays_dict[i]['WorkoutType'] = r[0]
                todays_dict[i]['Minutes'] = r[1]
                todays_dict[i]['CaloriesBurned'] = r[2]
                todays_dict[i]['Time'] = datetime.strptime(r[3], "%m/%j/%y %H:%M")
                
                return todays_dict
            
        except ValueError:
            print(f"No entry for today")       
        
    def get_from_API(self):
        # TODO
        return calories_burnt
    
    
    # The input dictionary should having keys: WorkoutType, Minutes. Before storing we compute
    # the calories burned from the api and then store it in the database.
    
    def insert_in_database(self, input_dict):
        
        # Description:
        # Inserts the input from the front end in the table.
        # 
        # Input:
        # input_dict (Dictionary): input dictionary from the user, described above
        #
        # Output:
        # Returns True if the entry is correctly made
        # Else returns False
        
        input_key_list = ['WorkoutType', 'Minutes']
    
        ct = 0
        for k in input_dict.keys():
            if k not in input_key_list():
                ct+=1
        assert ct == 0
        
        data_dict = input_dict
        date_dict['UserID'] = self.__user_id
        data_dict['Date'] = datetime.now()
        data_dict['CaloriesBurnt'] = get_from_API()

        try:
            self.__database_manager.insert_row(self.__table_name,data_dict)
            return True
        except ValueError:
            print(f'Could not make an entry in {self.__table_name}')