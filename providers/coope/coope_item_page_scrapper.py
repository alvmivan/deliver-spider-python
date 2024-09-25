from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper


class CoopeItemScrapper(ItemScrapper):
    def scrap_item_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        # <div
        #    _ngcontent-krt-c94=""
        #    class="articulo-detalle-imagen-contenedor articulo-detalle-imagen-contenedor-galeria"
        # >
        #
        #    <img _ngcontent-krt-c94=""
        #         class="articulo-detalle-imagen-ppal responsive-img zoom"
        #         data-caption="Fideos lucchetti tallarín n°5 500grs - $1.109,00"
        #         alt="Fideos lucchetti tallarín n°5 500grs - $1.109,00"
        #         title="Fideos lucchetti tallarín n°5 500grs - $1.109,00"
        #         src="https://www.lacoopeencasa.coop/media/lcec/publico/articulos/c/a/9
        #         /ca925d227b9d33515e083a6544762984"
        #    >
        # </div>
        # img_div = soup.find('div',
        #                     class_='articulo-detalle-imagen-contenedor articulo-detalle-imagen-contenedor-galeria')
        # img_tag = img_div.find('img')

        #   <div _ngcontent-krt-c57="" class="precio precio-detalle"> $1.109,00 <span _ngcontent-krt-c57="" class
        #   ="descripcion_precio" > < /span > < /div >
        price_div = soup.find('div', class_='precio precio-detalle')
        price = price_div.text
        price = money_tools.money_parser.round_price(price)
        # return item data inside a tuple
        product_updated_data = {
            'price': price,
        }
        return product_updated_data
