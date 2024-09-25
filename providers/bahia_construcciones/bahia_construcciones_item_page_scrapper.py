from pprint import pprint

from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper
from utils import debug_log


def get_price(soup):
    # the price is <p class="product__price">$147520.01</p>
    price_tag = soup.find('p', {'class': 'product__price'})
    if price_tag is None:
        return "No price found"

    price = price_tag.text
    price = money_tools.money_parser.round_price(price)
    price = price or 'No price found'
    return price


def get_photo(soup):
    # the photo is in <div class="esige-producto-gallery"><div class="col-12 esige-producto-gallery-primary"><img
    # class="img-fluid" alt="Imagen Actual" src="https://esige.paradigma.com.ar/static/bahiaconstrucciones/imagenes
    # /articulos/14958.jpg"></div><ul class="col-12 d-none d-md-flex p-0 esige-producto-gallery-list"><li
    # class="hover"><img class="img-fluid cursor-pointer" alt=""
    # src="https://esige.paradigma.com.ar/static/bahiaconstrucciones/imagenes/articulos/14958.jpg"></li></ul></div>
    photo_wrapper = soup.find('div', class_='esige-producto-gallery')
    # the photo has the alt="Imagen Actual" attribute

    photo = photo_wrapper.find('img', alt='Imagen Actual')['src']
    photo = photo or 'No photo found'
    return photo


class BahiaConstruccionesItemScrapper(ItemScrapper):
    def scrap_item_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        price = get_price(soup)
        product_updated_data = {
            'price': price,
        }
        return product_updated_data
