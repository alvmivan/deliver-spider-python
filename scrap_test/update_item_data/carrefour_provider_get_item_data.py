import unittest

from providers.carrefour.carrefour_provider import CarrefourProvider
from scrap_test.update_item_data.base_update_item_data_test import BaseProviderTest


class TestCarrefourProvider(BaseProviderTest):
    def test_carrefour(self):
        items_urls = [
            'https://www.carrefour.com.ar/vitroconvector-axel-2000w-ax-vitroco-blanco/p',
            'https://www.carrefour.com.ar/aceite-de-girasol-pureza-1500-cc/p',
            'https://www.carrefour.com.ar/convector-liliana-convectory-2000w-cng17/p',
        ]
        provider = CarrefourProvider(timeout=4, sleep=4, use_selenium=True, scroll=1200)
        self.run_update_item_data_test(provider, items_urls)


if __name__ == '__main__':
    unittest.main()
