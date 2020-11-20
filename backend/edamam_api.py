import requests
import numpy as np
from difflib import SequenceMatcher

class EdamamAPI():
    def __init__(self):
        self._url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
        self._key = "de414b4bedmsh907dea7bd3b009dp13afd1jsnee0e8e17539c"
        self._host = "edamam-food-and-grocery-database.p.rapidapi.com"

        self.headers = {'x-rapidapi-host': self._host,
                        'x-rapidapi-key': self._key}

        self.transform_dict =  {
                                'ENERC_KCAL': 'Cals',
                                'PROCNT': 'Protein',
                                'FAT': 'Fat',
                                'CHOCDF': 'Carbs',
                                'FIBTG': 'Fiber',
                            }
        
    def get_similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def get_food_information(self, query, upc=False):

        # Check UPC code or Ingredient
        # UPC are barcodes and Ingredients are all other foods.
        if upc:
            query_key = "upc"
        else:
            query_key = "ingr"
        querystring = {query_key:query}
    
        # Get response from request
        response = requests.request("GET", self._url, headers=self.headers, params=querystring)

        return response.json()
    
    def get_nutrient_information(self, query, upc=False):
        return self.get_top_matches(query, upc, k=1)

    def get_top_matches(self, query, upc=False, k=5):
        food_json = self.get_food_information(query, upc)
        success = False
        food_options_dict = {}
    
        if "error" not in food_json.keys() and len(food_json['hints']) > 0:        
            similarity_list = []
        
            for i,f in enumerate(food_json['hints']):
                f_food = f['food']
                if 'brand' in f_food.keys():
                    label_str = f_food['brand'] + " " + f_food['label']
                else:
                    label_str = f_food['label']
                similarity = 1 - self.get_similar(query, label_str)
                similarity_list.append(similarity)

            similarity_list = np.array(similarity_list)
            sorted_loc = np.argsort(similarity_list)
            k = min(k, len(similarity_list))
        
            for i in range(k):
                matched_item_info = food_json['hints'][sorted_loc[i]]['food']
            
                food_options_dict[i] = {}
                if 'brand' in matched_item_info.keys():
                    food_options_dict[i]['Label'] = matched_item_info['brand'] + " " + matched_item_info['label']
                else:
                    food_options_dict[i]['Label'] = matched_item_info['label']
                food_options_dict[i]['Nutrients'] = {}
                for k in matched_item_info['nutrients'].keys():
                    food_options_dict[i]['Nutrients'][self.transform_dict[k]] = matched_item_info['nutrients'][k]
                
            success = True
    
        return food_options_dict, success
