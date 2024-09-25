from bs4 import BeautifulSoup

from data_unification.item_scrapper import ItemScrapper
from data_unification.items_provider import ItemsProvider
from money_tools.money_parser import round_price
from providers.gili.gili_item_page_scrapper import GiliItemScrapper
from utils import get_html


def create_search_url(search_term):
    search_term = search_term.replace(' ', '+')
    return f'https://giliycia.com.ar/catalogsearch/advanced/result/?name={search_term}&category-search=Busc%C3%A1+por+categor%C3%ADas'


def get_items(soup):
    return soup.find_all('li', class_='item product product-item')


def extract_item_info(item):
    name = item.find('strong', class_='product name product-item-name').text
    price = item.find('span', class_='price').text
    photo = item.find('img', class_='product-image-photo')['src']
    details = item.find('div', class_='product-item-inner').text
    url = item.find('a', class_='product-item-link')['href']
    brand = item.find('span', class_='product-brand').text

    return {
        'name': name,
        'price': round_price(price),
        'photo': photo,
        'details': details,
        'url': url,
        'brand': brand,
    }


class GiliProvider(ItemsProvider):
    def find_items(self, search_term):
        search_url = create_search_url(search_term)
        html = get_html(search_url)
        soup = BeautifulSoup(html, 'html.parser')
        html_items = get_items(soup)
        return [extract_item_info(item) for item in html_items]

    def update_item_data(self, item_url):
        item_scrapper: ItemScrapper = GiliItemScrapper()

        html = get_html(item_url)
        return item_scrapper.scrap_item_data(html)

    def provider_id(self):
        return 'gili'

    def get_categories(self):
        return ['obra']
