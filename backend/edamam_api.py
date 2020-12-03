import requests
import numpy as np
from difflib import SequenceMatcher
from typing import Any, Tuple, List, Dict, Optional

class EdamamAPI():
    """
    The Edamam food API. 
    
    Provides the nutrient information for a food item when provided with the food name or the barcode number.

    ...

    Attributes
    ----------
    _url : str
        The API url.
    _key : str
        The API key.
    _host : str
        The API host.
    headers : str
        The API headers.
    transform_dict : Dict
        Dictionary which transforms the API nutrient labels to our apps nutrient labels. For instance
        the API uses ENER_KCAL for the calories while we use Cals.
        
    Methods
    -------
    get_similar(a: str, b: str) -> float
        The computes the similarity score between two strings.
    get_food_information(query: str, upc: bool) -> Dict
        Get the nutrient information from the food API given a query item.
    get_top_matches(query: str, upc: bool, k: int, serving_size: float) -> (Dict[int, Any], bool)
        Given a query, obtains the top k matches from the Food API. For each match, the function returns the total nutrients 
        after taking the serving size into account.
    """
    def __init__(self) -> None:
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
        
    def get_similar(self, a: str, b: str) -> float:
        """
        Computes the similarity metric between two strings.
        
        Parameters
        ----------
        a : str
            The first string.
        b : str
            The second string.
        
        Returns
        -------
        similarity_score : float
            The similarity score for the two strings. Useful while computing the top k matches for a given query.
        
        """
        return SequenceMatcher(None, a, b).ratio()

    def get_food_information(self, query: str, upc: Optional[bool] = False) -> Dict:
        """
        Computes the nutrient information for a given query from the Edamam Food API.
        
        Parameters
        ----------
        query : str
            The input query, for instance 'Apple', 'Orange' or a barcode number.
        upc : Optional[bool]
            True if query is a barcode number, otherwise False. Defaulted to False.
            
        Returns
        -------
        response : Dict
            Returns a dictionary of the nutrients for a given query.
        """

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
    
    def get_top_matches(self, query: str, upc: Optional[bool] = False, k: Optional[int] = 5, serving_size: Optional[float] = 1.0) -> Tuple[Dict[int, Any], bool]:
        """
        Returns the top k matches from the Edamam Food APi for a given query. For each match it returns the total nutrients consumed
        after taking the serving size into account.

        Parameters
        ----------
        query : string
            The input query which can either be a food item name like "Apple" or the barcode number in str.
        upc : Optional[bool]
            True if query is a barcode number, otherwise False. Defaulted to False.
        k : Optional[int]
            The number of top matches, defaults to 5 closest matches.
        serving_size : Optional[float]
            The serving size for that food item, defaults to 1.0.

        Returns
        -------
        results : Tuple[Dict[int, Any], bool]
            Returns a dictionary of the top k matches ranked, and the second part of the Tuple is True if food API query is successful,
            False otherwise.

        Notes
        -----
            An Example:
                {0:
                  {'Label' : 'Jamba Juice Orange Carrot Karma Smoothie, 22 fl oz',
                   'Nutrients' : {'Cals' : 41.499027861352765, 'Protein' : 0.6148004127607817,
                                  'Fat' : 0.15370010319019542, 'Carbs' : 10.144206810552898, 'Fiber': 0.6148004127607817}},
                 1: 
                  {'Label' : 'Jamba Juice Orange Carrot Karma Smoothie, 28 fl oz',
                   'Nutrients' : {'Cals' : 37.43695370561189, 'Protein' : 0.6038218339614821, 'Fat' : 0.12076436679229642,
                   'Carbs' : 9.178091876214529, 'Fiber' : 0.6038218339614821}}}

        """
        if not isinstance(query, str) or not isinstance(upc, bool) or not isinstance(k, int) or ((isinstance(k, int)) and k < 0):
            return {}, False

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
                    food_options_dict[i]['Nutrients'][self.transform_dict[k]] = serving_size * matched_item_info['nutrients'][k]
                
            success = True
    
        return food_options_dict, success
