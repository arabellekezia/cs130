import requests
from difflib import SequenceMatcher

class EdamamAPI():
    def __init__(self):
        self._url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
        self._key = "de414b4bedmsh907dea7bd3b009dp13afd1jsnee0e8e17539c"
        self._host = "edamam-food-and-grocery-database.p.rapidapi.com"

        self.headers = {'x-rapidapi-host': self._host,
                        'x-rapidapi-key': self._key}

    def get_similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def get_food_information(query, upc=False):

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

    # Given the query and the upc, this function will return the nutrient information in a 
    # dictionary, along with food label from the api and the success i.e. if it was able to 
    # find the food item in the api.
    def get_nutrient_information(query, upc=False):
        food_json = self.get_food_information(query, upc)
    
        # food_label: Returns the food label from the API. 
        #             Useful when we want to show the top
        #             2 food items for that nutrient.
    
        # nutrient_dict: Returns the nutrient dictionary.
        #                Keys: ENERC_KCAL(calories in kcal)
        #                      PROCNT (protiens in g)
        #                      FAT (fats in g)
        #                      CHOCDF (carbohydrates in g)
        #                      FIBTF (fibres in g)
    
        # success: returns when we are able to find the 
        #          product in the API or else ask the
        #          user to enter manually.
    
        food_label = None
        food_dict = {}
        nutrients_dict = None
        success = False
    
        curr_similarity = 0
        most_similar_id = 0
    
        # Checks if the food item is actually present in the API
        # otherwise let success be false.
        if "error" not in food_json.keys() and len(food_json['hints']) > 0:
            # Hope that the first entry in the json file
            # is the top match from the API.
        
            # Loops over all the searches and the find the one which
            # has the closest label, using the metric define above.
            for i,f in enumerate(food_json['hints']):
                similarity = self.get_similar(query, f['food']['label'])
                if similarity > curr_similarity:
                    most_similar_id = i
                    curr_similarity = similarity
                
            top_matched_item_info = food_json['hints'][most_similar_id]['food']
            food_label = top_matched_item_info['label']
            nutrients_dict = top_matched_item_info['nutrients']
            success = True
            food_dict = {'food_label': food_label}
            food_dict.update(nutrients_dict)
    
        return food_dict, success
