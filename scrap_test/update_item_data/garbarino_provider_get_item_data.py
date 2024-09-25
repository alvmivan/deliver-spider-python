# TestCooperativaProvider class
import unittest

from providers.garbarino.garbarino_provider import GarbarinoProvider
from scrap_test.update_item_data.base_update_item_data_test import BaseProviderTest


class TestGarbarinoProvider(BaseProviderTest):

    def test_garbarino(self):
        items_urls = [
            'https://www.garbarino.com/p/caloventor-estufa-bkf-2000w-bf-fh2000-gris-resistencia/b3f468fa-dd0e-437d'
            '-a306-e3d1033d2c76',
            'https://www.garbarino.com/p/estufa-electrica-infrarroja-axel-ax-ci1000-blanca/698204ff-b67a-4481-af8c'
            '-212331cbc7d5',
            'https://www.garbarino.com/p/estufa-calefactor-electrico-halogeno-ken-brown-kb-22-blanco/713601b1-f07f'
            '-4461-be1b-2e79bf360109',
        ]
        provider = GarbarinoProvider(timeout=4, sleep=4)
        self.run_update_item_data_test(provider, items_urls)


if __name__ == '__main__':
    unittest.main()
