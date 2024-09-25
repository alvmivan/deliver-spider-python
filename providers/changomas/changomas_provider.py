import requests
from bs4 import BeautifulSoup
import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper
from data_unification.items_provider import ItemsProvider
from providers.changomas.changomas_item_scrapper import ChangomasItemScrapper
from utils import get_html, debug_error, debug_log


def create_search_url(search_term):
    search_term = search_term.replace(' ', '%20')
    return f'https://www.masonline.com.ar/{search_term}?_q={search_term}&map=ft'


def get_items(soup):
    # Encuentra todos los elementos que contienen información del producto
    return soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')


def extract_item_info(item):
    try:
        price_span = item.find('div', class_='valtech-gdn-dynamic-product-0-x-dynamicProductPrice')
        price = price_span.text

        img_tag = item.find('img')
        photo = img_tag['src'] if img_tag else ''

        # el alt de la imagen tambien es el nombre, sino tiene esta clase vtex-product-summary-2-x-productBrand
        name = img_tag['alt'] if img_tag else item.find('span',
                                                        class_='vtex-product-summary-2-x-productBrand').text.strip()

        # el url está en el href de un 'a' con la clase vtex-product-summary-2-x-clearLink
        a_item = item.find('a', class_='vtex-product-summary-2-x-clearLink')
        url = a_item['href'] if a_item else '_blank'

        url = f'https://www.masonline.com.ar{url}'

        price = money_tools.money_parser.round_price(price)

    except Exception as e:
        return None

    if len(photo) < 5:
        return None

    return {
        'name': name,
        'price': price,
        'photo': photo,
        'url': url,
        'brand': "",
    }


class ChangomasProvider(ItemsProvider):
    def find_items(self, search_term):
        search_url = create_search_url(search_term)
        try:
            html = get_html(search_url, use_selenium=True)
        except requests.RequestException as e:
            debug_error(f"Error en la solicitud HTTP: {e}")
            return []
        debug_log(search_url)
        soup = BeautifulSoup(html, 'html.parser')
        html_items = get_items(soup)
        debug_log(f"Encontrados {len(html_items)} productos.")
        return [extract_item_info(item) for item in html_items if item is not None]

    def update_item_data(self, item_url):
        item_scrapper: ItemScrapper = ChangomasItemScrapper()
        html = get_html(item_url, use_selenium=True, timeout=self.timeout, sleep=self.sleep)
        return item_scrapper.scrap_item_data(html)

    def provider_id(self):
        return 'changomas'

    def get_categories(self):
        return ['almacen', 'electronica']
