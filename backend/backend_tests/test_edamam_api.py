import sys
sys.path.append("../")
from edamam_api import EdamamAPI
import unittest

class TestEdamamAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.api = EdamamAPI()
        self.query_list = ['apple', \
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
        Test single option. Best match.
        """
        k = 1
        for query in self.query_list:
            result, success = self.api.get_top_matches(query=query, upc=False, k=k)
            self.assertTrue(success)
            self.assertEqual(len(result.keys()), 1)

    def test_barcode(self):
        """
        Test single option. Best match.
        """
        k = 1
        query = '016000275287'
        result, success = self.api.get_top_matches(query=query, upc=True, k=k)
        self.assertTrue(success)
        self.assertEqual(len(result.keys()), 1)
        self.assertEqual(result[0]['Label'],'Cheerios Cheerios Cereal')


    def test_multiple(self):
        """
        Test multiple options. Top k matches.
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
        Test the similarity metric. This query also has 16, 28 fl oz variants.
        """
        query = 'jamba juice orange carrot karma smoothie, 22 fl oz'
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=False, k=k)
        self.assertTrue(success)
        self.assertEqual(result[0]['Label'], 'Jamba Juice Orange Carrot Karma Smoothie, 22 fl oz')

    def test_caps_invariance(self):
        """
        Test the query invariance to caps lock.
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
        Test the keys of the dictionary returned by the API
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
        Test for incorrect spelling.
        """
        query = 'upple'
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=False, k=k)
        self.assertFalse(success)

    def test_incorrect_query(self):
        """
        Test for incorrect query. Something random.
        """
        query = 'asdfghjkl'
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=False, k=k)
        self.assertFalse(success)

    def test_incorrect_wrong_query_type(self):
        """
        Test for incorrect query type.
        """
        query = 3.5
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=False, k=k)
        self.assertFalse(success)

    def test_incorrect_wrong_upc_type(self):
        """
        Test for incorrect upc type.
        """
        query = 'apple'
        upc = 'apple'
        k = 1
        result, success = self.api.get_top_matches(query=query, upc=upc, k=k)
        self.assertFalse(success)

    def test_incorrect_wrong_k_type(self):
        """
        Test for incorrect k type.
        """
        query = 'apple'
        k = 'apple'
        upc = False
        result, success = self.api.get_top_matches(query=query, upc=upc, k=k)
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()