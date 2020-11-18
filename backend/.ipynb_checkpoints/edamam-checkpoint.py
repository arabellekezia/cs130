import requests
from difflib import SequenceMatcher

def get_similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_food_information(query, upc=False):

    # API URL
    url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
    
    # Check UPC code or Ingredient
    # UPC are barcodes and Ingredients are all other foods.
    if upc:
        query_key = "upc"
    else:
        query_key = "ingr"
    querystring = {query_key:query}

    key = "de414b4bedmsh907dea7bd3b009dp13afd1jsnee0e8e17539c"
    host = "edamam-food-and-grocery-database.p.rapidapi.com"

    headers = {
        'x-rapidapi-host': host,
        'x-rapidapi-key': key
        }
    
    # Get response from request
    response = requests.request("GET", url, headers=headers, params=querystring)

#     print(response.json())
    return response.json()

# Given the query and the upc, this function will return the nutrient information in a 
# dictionary, along with food label from the api and the success i.e. if it was able to 
# find the food item in the api.
def get_nutrient_information(query, upc=False):
    
    food_json = get_food_information(query, upc)
    
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
            similarity = get_similar(query, f['food']['label'])
            if similarity > curr_similarity:
                most_similar_id = i
                curr_similarity = similarity
                
        top_matched_item_info = food_json['hints'][most_similar_id]['food']
        food_label = top_matched_item_info['label']
        nutrients_dict = top_matched_item_info['nutrients']
        success = True
    
    return food_label, nutrients_dict, success