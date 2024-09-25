from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper
from data_unification.items_provider import ItemsProvider
from providers.bahia_construcciones.bahia_construcciones_item_page_scrapper import BahiaConstruccionesItemScrapper
from utils import get_html


def create_search_url(search_term):
    # if i search for "chapa galvanizada" the url will be
    # https://bahiaconstrucciones.com.ar/tienda/productos/%20?search=chapa%20galvanizada
    search_term = search_term.replace(' ', '%20')
    return f'https://bahiaconstrucciones.com.ar/tienda/productos/%20?search={search_term}'


def get_items(soup):
    try:
        # the items wrapper has the class class="esige-productos-list col-xs-12 col-sm-12 col-md-9 col-lg-9 mt-1-i"
        items_wrapper = soup.find('div', class_='esige-productos-list col-xs-12 col-sm-12 col-md-9 col-lg-9 mt-1-i')
        # each item has the class productItem
        items = items_wrapper.find_all('div', class_='productItem')
        print("found items: ", len(items))
        return items

    except:
        return []


def extract_item_info(item):
    name = get_name(item)
    price = get_price(item)
    photo = get_photo(item)
    url = get_url(item)
    details = "Not found"
    brand = "Not found"

    product_ = {
        'name': name,
        'price': price,
        'photo': photo,
        'url': url,
        'details': details,
        'brand': brand,
    }
    return product_


def get_url(item):
    url = item.find('a')['href']
    # append the url to https://bahiaconstrucciones.com.ar/
    url = f'https://bahiaconstrucciones.com.ar{url}'
    return url


def get_photo(item):
    # the photo is in <a class="productItem__photoContainer" href="/tienda/producto/Zz-TQ5NTgH-Q"><img
    # src="https://esige.paradigma.com.ar/static/bahiaconstrucciones/imagenes/articulos/14958.jpg" alt=""
    # class="productItem__photo"></a>
    photo = item.find('img', class_='productItem__photo')['src']
    photo = photo or 'No photo found'
    return photo


def get_price(item):
    # the price is in <div class="productItem__price"><h3 class="price mx-auto">$ 10.165</h3></div>
    price = item.find('h3', class_='price mx-auto').text
    price = money_tools.money_parser.round_price(price)
    price = price or 'No price found'
    return price


def get_name(item):
    # the name is in <h2 class="productItem__title">CHAPAS CUMBRERA GALVANIZADA 0,40 X 1,10 MTS</h2>
    name = item.find('h2', class_='productItem__title').text
    name = name or 'No name found'
    return name


class BahiaConstruccionesProvider(ItemsProvider):

    def find_items(self, search_term):
        search_url = create_search_url(search_term)
        html = get_html(search_url, use_selenium=True, timeout=4, sleep=4)
        soup = BeautifulSoup(html, 'html.parser')
        html_items = get_items(soup)
        return [extract_item_info(item) for item in html_items]

    def update_item_data(self, item_url):
        item_scrapper: ItemScrapper = BahiaConstruccionesItemScrapper()
        html = get_html(item_url, True)
        return item_scrapper.scrap_item_data(html)

    def provider_id(self):
        return 'bahia_construcciones'

    def get_categories(self):
        return ['obra']
