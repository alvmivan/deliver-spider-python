# TestCooperativaProvider class
import unittest

from providers.coope.coope_provider import CooperativaProvider
from scrap_test.update_item_data.base_update_item_data_test import BaseProviderTest


class TestCooperativaProvider(BaseProviderTest):

    def test_coope(self):
        items_urls = [
            'https://www.lacoopeencasa.coop/producto/salsa-lista-knorr-pizza-200grs/312090',
            'https://www.lacoopeencasa.coop/producto/salsa-lista-arcor-pizza-doypack-340grs/285391',
            'https://www.lacoopeencasa.coop/producto/salsa-lista-knorr-pizza-340grs/312091',
        ]
        provider = CooperativaProvider(timeout=6, sleep=6)
        self.run_update_item_data_test(provider, items_urls)


if __name__ == '__main__':
    unittest.main()
