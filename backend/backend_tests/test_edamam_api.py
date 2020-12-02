from backend.edamam_api import EdamamAPI
import unittest

class TestEdamamAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.api = EdamamAPI()
        self.query_list = ['apple',\
                           'jamba juice orange carrot karma smoothie, 22 fl oz', \
                           'salmon', \
                           'chicken teriyaki', \
                           'burrito bowl', \
                           'orange juice' \
                           'almonds', \
                           'avocado', \
                           'carls junior burger']

    def test_single(self):
        """
        Test get_top_matches() with k=1, i.e. the best match.
        """
        k = 1
        for query in self.query_list:
            result, success = self.api.get_top_matches(query=query, upc=False, k=k)
            self.assertTrue(success)
            self.assertEqual(len(result.keys()), 1)
            
    def test_serving(self): 
        """
        Test the total nutrient computation after taking the serving size into account.
        """
        k = 1
        query = 'Apple'
        serving_size = 2.5
        result, success = self.api.get_top_matches(query=query, upc=False, k=k, serving_size=serving_size)
        self.assertTrue(success)
        self.assertEqual(len(result.keys()), 1)
        self.assertEqual(result[0]['Nutrients']['Cals'], 52.0 * serving_size)
        self.assertEqual(result[0]['Nutrients']['Protein'], 0.26 * serving_size)
        self.assertEqual(result[0]['Nutrients']['Fat'], 0.17 * serving_size)
        self.assertEqual(result[0]['Nutrients']['Carbs'], 13.81 * serving_size)
        self.assertEqual(result[0]['Nutrients']['Fiber'], 2.4 * serving_size)


    def test_barcode(self):
        """
        Test barcode query, i.e. with the input to API is a barcode number.
        """
        k = 1
        query = '016000275287'
        result, success = self.api.get_top_matches(query=query, upc=True, k=k)
        self.assertTrue(success)
        self.assertEqual(len(result.keys()), 1)
        self.assertEqual(result[0]['Label'],'Cheerios Cheerios Cereal')


    def test_multiple(self):
        """
        Test get_top_matches() for k>1. It should correctly return the top k matches.
        """
        k = 5
        for query in self.query_list:
            result, success = self.api.get_top_matches(query=query, upc=False, k=k)
            self.assertTrue(success)
            self.assertEqual(len(result.keys()), 5)

    def test_multiple_limit(self):
        """
        Test the maximum number of options. If you want top 100 options but the
        API only contains 22 then it should return 22 options.
        """
        query = 'apple'
        k = 100
        result, success = self.api.get_top_matches(query=query, upc=False, k=k)
        self.assertTrue(success)
        self.assertEqual(len(result.keys()), 22)

    def test_similarity_metric(self):
        """
        Test the similarity metric. We will use this query:
        'jamba juice orange carrot karma smoothie, 22 fl oz'
        This query also has 16, 28 fl oz variants. So the method get_top_matches()
        should be able to correctly return the 22 fl oz variant.
        """
        query = 'jamba juice orange carrot karma smoothie, 22 fl oz'
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=False, k=k)
        self.assertTrue(success)
        self.assertEqual(result[0]['Label'], 'Jamba Juice Orange Carrot Karma Smoothie, 22 fl oz')

    def test_caps_invariance(self):
        """
        Test the query invariance to caps lock. 'apple' and 'ApPlE' should give the same nutrients.
        """
        k = 1
        query_1 = 'apple'
        query_2 = 'ApPlE'
        result_1, success_1 = self.api.get_top_matches(query=query_1, upc=False, k=k)
        result_2, success_2 = self.api.get_top_matches(query=query_2, upc=False, k=k)
        self.assertTrue(success_1)
        self.assertTrue(success_2)
        self.assertEqual(result_1[0]['Label'], result_2[0]['Label'])
        self.assertEqual(result_1[0]['Nutrients'], result_2[0]['Nutrients'])

    def test_nutrient_dict_keys(self):
        """
        Test the keys of the dictionary returned by the API. Since we change the
        keys of the nutrients dictionary used in Edamam Food APi, we check if the
        keys are correctly transformed.
        """
        keys = ['Cals', 'Carbs', 'Protein', 'Fiber', 'Fat']
        k = 5
        for query in self.query_list:
            result, success = self.api.get_top_matches(query=query, upc=False, k=k)
            self.assertTrue(success)
            ct = 0
            for i in range(k):
                for key in result[0]['Nutrients'].keys():
                    if key not in keys:
                        ct += 1
            self.assertEqual(ct, 0)

    def test_incorrect_spelling(self):
        """
        Test for incorrect query spelling. 'upple' is not a food item, so the method
        should return False.
        """
        query = 'upple'
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=False, k=k)
        self.assertFalse(success)

    def test_incorrect_query(self):
        """
        Test for incorrect query. Something random. The API should return False.
        """
        query = 'asdfghjkl'
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=False, k=k)
        self.assertFalse(success)

    def test_incorrect_wrong_query_type(self):
        """
        Test for incorrect query type. The query data type should be correct.
        """
        query = 3.5
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=False, k=k)
        self.assertFalse(success)

    def test_incorrect_wrong_upc_type(self):
        """
        Test for incorrect upc type. The upc data type should be correct.
        """
        query = 'apple'
        upc = 'apple'
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=upc, k=k)
        self.assertFalse(success)

    def test_incorrect_wrong_k_type(self):
        """
        Test for incorrect k type. k should be an integer.
        """
        query = 'apple'
        k = 'apple'
        upc = False
        result, success = self.api.get_top_matches(query=query, upc=upc, k=k)
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()
