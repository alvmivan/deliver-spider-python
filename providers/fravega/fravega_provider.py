from bs4 import BeautifulSoup

from data_unification.item_scrapper import ItemScrapper
from data_unification.items_provider import ItemsProvider
from money_tools.money_parser import round_price
from providers.fravega.fravega_item_page_scrapper import FravegaItemScrapper
from utils import get_html


def create_search_url(search_term):
    # if i search for "smart tv" the url will be https://www.fravega.com/l/?keyword=smart+tv
    search_term = search_term.replace(' ', '+')
    return f'https://www.fravega.com/l/?keyword={search_term}'


def get_items(soup):
    li_elements = soup.find_all('li')
    articles = [li.find('article', {'data-test-id': 'result-item'}) for li in li_elements if
                li.find('article', {'data-test-id': 'result-item'})]
    return articles


def extract_item_info(item):
    name = item.find('span', class_='sc-ca346929-0').text
    price = item.find('span', class_='sc-1d9b1d9e-0').text
    photo = item.find('img', class_='sc-1362d5fd-0')['src']
    url = item.find('a', class_='sc-812c6cb5-0')['href']
    # append the base url to the url found
    url = f'https://www.fravega.com{url}'
    details = [detail.text.strip() for detail in item.find_all('li', class_='sc-47d33c80-1')]
    # details must be string or None if empty
    details = ', '.join(details) if details else "No details found"
    product_ = {
        'name': name,
        'price': round_price(price),
        'photo': photo,
        'url': url,
        'details': details,
        'brand': "Cant find brands for fravega product",
    }
    return product_


class FravegaProvider(ItemsProvider):

    def find_items(self, search_term):
        search_url = create_search_url(search_term)
        html = get_html(search_url, True)
        soup = BeautifulSoup(html, 'html.parser')
        html_items = get_items(soup)
        items = [extract_item_info(item) for item in html_items]
        print(items)
        return items

    def update_item_data(self, item_url):
        item_scrapper: ItemScrapper = FravegaItemScrapper()
        html = get_html(item_url, use_selenium=True, timeout=self.timeout, sleep=self.sleep)
        return item_scrapper.scrap_item_data(html)

    def provider_id(self):
        return 'fravega'

    def get_categories(self):
        return ['electronica']
