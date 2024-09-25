from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper


def get_price(soup):
    # the price is in <div id="priceContainer" class="veaargentina-store-theme-1dCOMij_MzTzZOCohX1K7w" style="color:
    # rgb(
    # 77, 77, 77); margin-top: 0px;">$1.319.999</div>
    price_container = soup.find('div', {'id': 'priceContainer'})
    price = price_container.text
    price = money_tools.money_parser.round_price(price)
    price = price or "Not found"
    return price


class VeaItemScrapper(ItemScrapper):

    def scrap_item_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        price = get_price(soup)
        product_updated_data = {
            'price': price,
        }
        return product_updated_data
