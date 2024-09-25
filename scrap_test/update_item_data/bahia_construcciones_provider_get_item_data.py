# TestCooperativaProvider class
import unittest

from providers.bahia_construcciones.bahia_construcciones_provider import BahiaConstruccionesProvider
from providers.hipertehuelche.hipertehuelche_provider import HipertehuelcheProvider
from scrap_test.update_item_data.base_update_item_data_test import BaseProviderTest


class TestBahiaConstruccionesProvider(BaseProviderTest):

    def test_bahia_construcciones(self):
        items_urls = [
            'https://bahiaconstrucciones.com.ar/tienda/producto/Zz-TQ5NTgH-Q',
            'https://bahiaconstrucciones.com.ar/tienda/producto/Zz-DAzZz-zk1',
            'https://bahiaconstrucciones.com.ar/tienda/producto/Zz-DAzZz-TY3',
            'https://bahiaconstrucciones.com.ar/tienda/producto/VlIx'
        ]
        provider = BahiaConstruccionesProvider(use_selenium=True, sleep=4, timeout=4)
        self.run_update_item_data_test(provider, items_urls)


if __name__ == '__main__':
    unittest.main()
