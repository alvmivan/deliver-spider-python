# TestCooperativaProvider class
import unittest

from providers.gili.gili_provider import GiliProvider
from scrap_test.update_item_data.base_update_item_data_test import BaseProviderTest


class TestGiliProvider(BaseProviderTest):

    def test_gili(self):
        items_urls = [
            'https://giliycia.com.ar/catalog/product/view/id/17495/s/estufa-vertical-chapa-con-2-cuarzos-1-tec-mozart/category/2/',
            'https://giliycia.com.ar/catalog/product/view/id/13441/s/estufa-nuke-eco-puelo/category/2/',
            'https://giliycia.com.ar//estufa-uke-wichi-50-plata.html',
        ]
        provider = GiliProvider(timeout=4, sleep=4)
        self.run_update_item_data_test(provider, items_urls)


if __name__ == '__main__':
    unittest.main()
