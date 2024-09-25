import unittest

from providers.changomas.changomas_provider import ChangomasProvider
from scrap_test.update_item_data.base_update_item_data_test import BaseProviderTest


class TestChangomasProvider(BaseProviderTest):
    def test_changomas(self):
        items_urls = [
            'https://www.masonline.com.ar/calefactor-longvie-tiro-balanceado-eba3s-3000kc/p',
            'https://www.masonline.com.ar/caloventor-liliana-forzahot-ptc617/p',
            # 'https://www.masonline.com.ar/calefactor-electrico-liliana-tecnohot/p',
        ]
        provider = ChangomasProvider(timeout=4, sleep=4)
        self.run_update_item_data_test(provider, items_urls)


if __name__ == '__main__':
    unittest.main()
