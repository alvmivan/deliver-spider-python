# TestCooperativaProvider class
import unittest

from providers.gili.gili_provider import GiliProvider
from providers.hipertehuelche.hipertehuelche_provider import HipertehuelcheProvider
from scrap_test.update_item_data.base_update_item_data_test import BaseProviderTest


class TestHipertehuelcheProvider(BaseProviderTest):

    def test_hipertehuelche(self):
        items_urls = [
            'https://www.hipertehuelche.com/productos/estufa-electrica-1600w/',
            'https://www.hipertehuelche.com/productos/estufa-electrica-1200w/',
            'https://www.hipertehuelche.com/productos/estufa-movil-4000-kcal/',
        ]
        provider = HipertehuelcheProvider()
        self.run_update_item_data_test(provider, items_urls)


if __name__ == '__main__':
    unittest.main()
