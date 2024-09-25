# TestFravegaProvider class
import unittest

from providers.fravega.fravega_provider import FravegaProvider

from scrap_test.update_item_data.base_update_item_data_test import BaseProviderTest


class TestFravegaProvider(BaseProviderTest):

    def test_fravega(self):
        items_urls = [
            'https://www.fravega.com/p/smart-tv-qled-50-tcl-l50c645-f--502496/',
            'https://www.fravega.com/p/smart-tv-65-4k-uhd-qled-noblex-dq65x9500-black-series-502424/',
            'https://www.fravega.com/p/smart-tv-65-4k-hdr-tcl-l65p735-f-502468/',
        ]
        provider = FravegaProvider(timeout=5, sleep=5)
        self.run_update_item_data_test(provider, items_urls)


if __name__ == '__main__':
    unittest.main()
