from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper
from data_unification.items_provider import ItemsProvider
from providers.garbarino.garbarino_item_page_scrapper import GarbarinoItemScrapper
from utils import get_html


def create_search_url(search_term):
    search_term = search_term.replace(' ', '%20')
    return f'https://www.garbarino.com/shop?search={search_term}'


def get_items(soup):
    # Encuentra todos los elementos que contienen información del producto
    return soup.find_all('div', class_='product-card-design6-vertical-wrapper')


def extract_item_info(item):
    # Extrae el nombre del producto
    name_tag = item.find('a', class_='card-anchor')
    name = name_tag.text.strip() if name_tag else 'No name found'

    # Extrae el precio del producto
    price_tag = item.find('div', class_='product-card-design6-vertical__price')
    price = price_tag.text.strip().replace('$', '').replace(',', '') if price_tag else "0"

    # Extrae la URL de la imagen del producto
    img_tag = item.find('img', class_='ratio-image__image')
    photo = img_tag['src'] if img_tag else 'No image found'

    # Extrae el URL del producto
    url_tag = item.find('a', class_='card-anchor')
    url = url_tag['href']
    # Si el URL no es completo, lo completa
    url = f'https://www.garbarino.com{url}'
    url = url or 'No url found'

    # Información adicional, si está disponible
    details_tag = item.find('div', class_='product-card-design6-vertical__name')
    details = details_tag.text.strip() if details_tag else 'No details found'

    # Marca del producto, si está disponible
    brand_tag = item.find('div', class_='product-card-design6-vertical__brand')
    brand = brand_tag.text.strip() if brand_tag else 'No brand found'
    return {
        'name': name,
        'price': money_tools.money_parser.round_price(price),
        'photo': photo,
        'details': details,
        'url': url,
        'brand': brand,
    }


class GarbarinoProvider(ItemsProvider):
    def find_items(self, search_term):
        search_url = create_search_url(search_term)
        html = get_html(search_url)
        soup = BeautifulSoup(html, 'html.parser')
        html_items = get_items(soup)
        return [extract_item_info(item) for item in html_items]

    def update_item_data(self, item_url):
        item_scrapper: ItemScrapper = GarbarinoItemScrapper()
        html = get_html(item_url, use_selenium=True, timeout=self.timeout, sleep=self.sleep)
        return item_scrapper.scrap_item_data(html)

    def provider_id(self):
        return 'garbarino'

    def get_categories(self):
        return ['electronica']
