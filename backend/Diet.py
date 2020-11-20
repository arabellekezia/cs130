from Health import Health
from datetime import datetime, date, timedelta
from edamam import get_nutrient_information

class Diet(Health):
    
    def __init__(self, table_name, goal_table_name, database, user_id):
        self.__table_name = table_name
        self.__goal_table_name = goal_table_name
        self.__database = database
        self.__user_id = user_id
    
    def get_value_given_date(self, nutrient, given_date):
        
        # Description: 
        # Takes a nutrient as input for instance protein and a date and return the
        # total amount proteins consumed on that date.
        
        # Input:
        # nutrient (STRING): 'Cals, Protein, Fat, Carbs, Fiber'
        # given_date(DATE): python date, not datetime
        
        # Output:
        # Float value
        
        next_date = given_date + timedelta(days=1)
        
        query = f"SELECT ServingSize, {nutrient} FROM {self.__table_name}\
                join Users on Users.id={self.__table_name}.UserID\
                WHERE Datetime >= '{str(given_date)} 00:00:00' AND\
                Datetime <= '{str(next_date)} 00:00:00' AND UserID = {self.__user_id}"

        try:
            # If you can find the corresponding date in the database return the total 
            # nutrient consumed, otherwise just throw error.
            records = self.__database_manager.select_data(query)
            given_date_nutrients = 0
            for r in records:
                given_date_nutrients += r[0] * r[1]
            return given_date_nutrients
        except ValueError:
            print(f"No entry for {given_date}.")
            # TODO
            # OR SHOULD WE RAISE AN ERROR INSTEAD OF RETURNING 0?
#             return 0
    
    def get_topk_foods(self, nutrient, k=2):
        
        # Description:
        # Return the top 2 food items with the higest quantity of a particular nutrient for that date.
        # Returns a dictionary with keys: the names of the two items and the values = nutrient quantity.
        #
        # Input: 
        # nutrient (STRING): 'Cals, Protein, Fat, Carbs, Fiber'
        #
        # Output:
        # top2_dict (Dictionary): keys: names of the top two items
        # values: the corresponding nutrient quantity.
        
        todays_date = date.today()
        next_date = given_date + timedelta(days=1)
        
        query = f"SELECT Item, ServingSize, {nutrient} FROM {self.__table_name}\
                join Users on Users.id={self.__table_name}.UserID\
                WHERE Datetime >= '{str(given_date)} 00:00:00' AND\
                Datetime <= '{str(next_date)} 00:00:00'"
        
        topk_dict = {}
        
        try:
            records = self.__database_manager.select_data(query)
            item_list = []
            nutri_list = []
            for r in records:
                item_list.append(r[0])
                nutri_list.append(r[1] * r[2])
            
            import numpy as np
            nutri_list = -np.array(nutri_list)
            sorted_loc = np.argsort(nutri_list)
            
            k = min(k, len(records))
            
            for i in range(k):
                topk_dict[item_list[i]] = nutri_list[i]
            
            return topk_dict
        except ValueError:
            print('Top k items not found.')
            # TODO
            # OR SHOULD WE RAISE AN ERROR INSTEAD OF RETURNING 0?
#             return 0
    
    def get_daily_decomposition(self, nutrient_list): 
        
        # Description:
        # Useful for the diet page where we show the daily percentage breakup.
        # Look 2 diagram in Figure 1 in report.
        
        # Input:
        # nutrient_list (LIST of STRING): ['Cals, Protein, Fat, Carbs, Fiber']
        # There wont be cals because I think cals is a measure of energy and not a measure
        # of the mass, so we only have 4.
        
        # Output:
        # Returns a nested dictionary:
        # First level keys are the nutrients: 'Cals, Protein, Fat, Carbs, Fiber'
        # Second level keys: for each nutrient we have two keys: percentage corresponding to the daily %
        # and top_2 which is another dictionary with keys as the names of the top2 food items and the values
        # corresponding to the quantity of the nutrient.
        
        try:
            nutri_decom = {}
            for nutri in nutrient_list:
                nutri_decom[nutri] = self.get_daily_value(nutri)

            total = sum([nutri_decom[k] for k in nutri_decom.keys()])

            per_nutri_decom = {}
            for nutri in nutrient_list:
                per_nutri_decom[nutri] = {}
                per_nutri_decom[nutri]['percentage'] = 100.0 * (nutri_decom[nutri]/total)
                per_nutri_decom[nutri]['top_k'] = self.get_top2_foods(nutri)

            return per_nutri_decom
        except ValueError:
            print('No entry has been made for today.')
        
            
    def get_from_API(self, query, upc):
        
        # Description: 
        # Calculates the nutrient values from the API
        
        # Input:
        # query (STRING): user input i.e. the string which user enters.
        # upc (BOOL): True if the query is a barcode number and False otherwise
        
        # Output:
        # api_dict (Dictionary): Nested Dictionary with keys as the nutrient names: 
        # First level keys: 0,1,2,3,4 corresponding to the top 5 choices we return
        # Second level keys: Label and Nutrients. Labels is the name for the ith item
        # and Nutrients is another dictionary with keys: 'Cals, Protein, Fat, Carbs, Fiber'
        #
        # See edamam.py for more details.
        #
        # success (BOOL): return True if an item with the query name is found in the API otherwise returns False.
        
        food_options_dict, success = self.get_nutrient_information(query, upc)
        if success:
            return label, api_dict, success
        else:
            raise ValueError('Could not find the item in the FoodAPI.')
    
    
    # Since we are assuming that we will be providing the user with options to select from, we will let the
    # the input to this function be the following nested dictionary:
    # First level keys: Item (corresponding to the item name which will be either what the api returns
    # or if the user does not choose api then the manual entry), ServingSize (the serving size), Barcode (a 
    # boolean which will be true if the user chooses barcode) and finally nutri_dict (which is the nutrient
    # dictionary with keys: 'Cals, Protein, Fat, Carbs, Fiber' and their corresponding values.)

    # Input dict should have the following keys:
    # 1)Item
    # 2)ServingSize
    # 3)Barcode
    # 4)nutri_dict
    
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
        
        # We can take this as input as well if required.
        nutri_name_list = ['Cals', 'Protein', 'Fat', 'Carbs', 'Fiber']
        input_key_list = ['Item', 'ServingSize', 'Barcode', 'nutri_dict']
    
        ct = 0
        for k in input_dict.keys():
            if k not in input_key_list():
                ct+=1
        if ct == 0:
            for k in input_dict['nutri_dict']:
                if i not in nutri_name_list:
                    ct+=1
        assert ct == 0
        
        data_dict = input_dict
        del data_dict['nutri_dict']
        date_dict['UserID'] = self.__user_id
        data_dict['Datetime'] = datetime.now()
        
        for k in input_dict['nutri_dict'].keys():
            data_dict[k] = input_dict['nutri_dict'][k]

        try:
            self.__database_manager.insert_row(self.__table_name,data_dict)
            return True
        except ValueError:
            print(f'Could not make an entry in {self.__table_name}')