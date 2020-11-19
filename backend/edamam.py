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

transform_dict =  {
    'ENERC_KCAL': 'Cals',
    'PROCNT': 'Protein',
    'FAT': 'Fat',
    'CHOCDF': 'Carbs',
    'FIBTG': 'Fiber',
}

def get_nutrient_information(query, upc=False, k=5):
    
    # Description: 
    # Returns the top k=5 closest matches from the API in the form of nested dictionaries.
    
    # Inputs:
    # query (STRING): the input query which could be the name of the item or its barcode number.
    # upc (BOOL): True when query is the barcode number otherwise false
    # k (INT): Number of top matches to return
    
    # Outputs:
    
    # food_options_dict: Returns a nested dictionary.
    #
    # query = 'jamba juice orange carrot karma smoothie, 22 fl oz'
    # upc = False
    # get_nutrient_information(query, upc)
    #
    # Sample Output: Just showing the first two entries of the dictionary.
    #
    # 0
    # 	Label
    # 		Jamba Juice Orange Carrot Karma Smoothie, 22 fl oz
    # 	Nutrients
    # 		Cals
    # 			41.499027861352765
    # 		Protein
    # 			0.6148004127607817
    # 		Fat
    # 			0.15370010319019542
    # 		Carbs
    # 			10.144206810552898
    # 		Fiber
    # 			0.6148004127607817
    # 1
    # 	Label
    # 		Jamba Juice Orange Carrot Karma Smoothie, 28 fl oz
    # 	Nutrients
    # 		Cals
    # 			37.43695370561189
    # 		Protein
    # 			0.6038218339614821
    # 		Fat
    # 			0.12076436679229642
    # 		Carbs
    # 			9.178091876214529
    # 		Fiber
    # 			0.6038218339614821
    
    # First level of keys are just: 0,1,2,3,4
    # Second level of keys: Label, Nutrients
    #                       Label corresponds to the name of the food item in the API
    #                       Nutrients is another dictionary with keys Cals, Proteins, Fat, Carbs, Fiber
    #
    # success: returns True when we are able to find the 
    #          product in the API otherwise return False and we ask the
    #          user to enter manually.
    
    food_json = get_food_information(query, upc)
    
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
            similarity = 1 - get_similar(query, label_str)
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
                food_options_dict[i]['Nutrients'][transform_dict[k]] = matched_item_info['nutrients'][k]
                
        success = True
    
    return food_options_dict, success