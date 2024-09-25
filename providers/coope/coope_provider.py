# https://www.lacoopeencasa.coop/listado/busqueda-avanzada/fideos_lucchetti

from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper
from data_unification.items_provider import ItemsProvider
from providers.coope.coope_item_page_scrapper import CoopeItemScrapper
from utils import get_html


def create_search_url(search_term):
    search_term = search_term.replace(' ', '_')
    return f'https://www.lacoopeencasa.coop/listado/busqueda-avanzada/{search_term}'


def get_items(soup):
    # Encuentra todos los elementos que contienen información del producto
    return soup.find_all('div', class_='card hoverable')


def find_name(item):
    # <p _ngcontent-wpv-c58="" class="text-capitalize"> fideos lucchetti ave maría 500grs... </p>
    name_tag = item.find('p', class_='text-capitalize')
    name = name_tag.text.strip() if name_tag else 'No name found'
    return name.replace('...', '')


def find_price(item):
    # <div _ngcontent-wpv-c57="" class="precio-entero"><small _ngcontent-wpv-c57="">$</small>1.109 </div>
    price_tag = item.find('div', class_='precio-entero')
    price = price_tag.text.strip() if price_tag else "0"
    return price


def find_photo(item):
    # find an image tag
    img_tag = item.find('img')
    # get the src attribute
    photo = img_tag['src'] if img_tag else 'No photo found'
    return photo


def find_url(item):
    a_tag = item.find('a')  # the href is the photo
    url = a_tag['href'] if a_tag else 'No url found'
    # esto es una url parcial, que termina en /{id}
    # extraigamos ese id
    parts = url.split('/')
    id = parts[-1]
    # luego la anteultima parte es el tipo de producto
    type = parts[-2]
    # then return the full url
    url = f'https://www.lacoopeencasa.coop/producto/{type}/{id}'
    # https: // www.lacoopeencasa.coop / producto / a / 233573
    return url


def extract_item_info(item):
    name = find_name(item)
    price = find_price(item)
    photo = find_photo(item)
    url = find_url(item)
    details = 'No details found'
    brand = 'No brand found'

    return {
        'name': name,
        'price': money_tools.money_parser.round_price(price),
        'photo': photo,
        'details': details,
        'url': url,
        'brand': brand,
    }


class CooperativaProvider(ItemsProvider):

    def find_items(self, search_term):
        search_url = create_search_url(search_term)
        html = get_html(search_url, use_selenium=True, timeout=self.timeout, sleep=self.sleep, scroll=1200)

        soup = BeautifulSoup(html, 'html.parser')
        html_items = get_items(soup)

        return [extract_item_info(item) for item in html_items]

    def provider_id(self):
        return 'coope'

    def update_item_data(self, item_url):
        item_scrapper: ItemScrapper =CoopeItemScrapper()
        html = get_html(item_url, use_selenium=True, timeout=self.timeout, sleep=self.sleep)
        return item_scrapper.scrap_item_data(html)

    def get_categories(self):
        return ["almacen"]
