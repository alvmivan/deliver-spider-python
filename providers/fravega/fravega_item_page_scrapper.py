from pprint import pprint

from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper


def get_price(soup):
    # the price is in <div data-test-id="price-wrapper" style="flex-direction:row;margin-bottom:5px"
    # class="sc-f0afe095-1 erTCGK"><span style="font-weight:500;font-size:24px" class="sc-1d9b1d9e-0 sc-441c2f70-3
    # OZgQ pqRaC">$649.999</span><div class="sc-f0afe095-0 kKNApQ"><span class="sc-66d25270-0 sc-441c2f70-4 eiLwiO
    # jMUdfR">$741.999</span><span style="height:0;width:4px"></span><span class="sc-e2aca368-0 sc-441c2f70-5 juwGno
    # jokVgg">12</span></div></div>
    price = soup.find('div', {'data-test-id': 'price-wrapper'}).find('span', {
        'class': 'sc-1d9b1d9e-0 sc-441c2f70-3 OZgQ pqRaC'}).text
    price = price or 'No price found'
    if price == 'No price found':
        return price
    else:
        price = money_tools.money_parser.round_price(price)
    return price


def get_photo(soup):
    # the photo is in <li class="sc-237b4ecc-1 sc-4e9ea34a-9 brHJQg gtYzCc"><img
    # src="https://images.fravega.com/f300/0cf4634e5c484932c4af438899a8dd22.jpg.webp" width="300" height="300"
    # class="sc-4e9ea34a-8 gUZZBo imagenSeleccionada" alt="Smart tv qled 50 tcl l50c645 f  - 0" style="cursor:
    # pointer; border: none;"></li>
    # catch the item with class="sc-237b4ecc-1 sc-4e9ea34a-9 brHJQg gtYzCc" and get the img
    photo = soup.find('li', {'class': 'sc-237b4ecc-1 sc-4e9ea34a-9 brHJQg gtYzCc'}).find('img')['src']
    photo = photo or 'No photo found'
    return photo


class FravegaItemScrapper(ItemScrapper):
    def scrap_item_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        price = get_price(soup)
        product_updated_data = {
            'price': price,
        }
        return product_updated_data
