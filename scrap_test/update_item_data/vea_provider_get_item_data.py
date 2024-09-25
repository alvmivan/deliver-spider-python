import unittest

from providers.vea.vea_provider import VeaProvider
from scrap_test.update_item_data.base_update_item_data_test import BaseProviderTest


class TestVeaProvider(BaseProviderTest):

    def test_vea(self):
        items_urls = [
            'https://www.vea.com.ar/led-65-crystal-uhd-samsung-4k-smart-tv/p',
            'https://www.vea.com.ar/led-43-samsung-43t5300a-full-hd-smart/p',
            'https://www.vea.com.ar/led-noblex-65-smart-dk65x6550-2/p',
        ]
        provider = VeaProvider()
        self.run_update_item_data_test(provider, items_urls)


if __name__ == '__main__':
    unittest.main()