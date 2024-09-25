# BaseProviderTest class
import unittest


class BaseProviderTest(unittest.TestCase):

    def run_update_item_data_test(self, provider, items_urls):
        # let's make a variable to store the results
        results = []

        print("checkpoint 1")
        for item_url in items_urls:
            result = provider.update_item_data(item_url)
            self.assertIsInstance(result, dict)
            self.assertIn('price', result)
            # store the result for later use
            results.append(result)
        print("checkpoint 2")

        # print all the item data
        for result in results:
            print(result)

        print("checkpoint 3 finished")
