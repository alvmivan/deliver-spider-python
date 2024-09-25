from pprint import pprint

from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper


def get_photo(soup):
    print("Starting to get photo...")
    # the photo is in <div class="gallery-placeholder _block-content-loading" data-gallery-role="gallery-placeholder">
    #     <img
    #         alt="main product photo"
    #         class="gallery-placeholder__image"
    #         src="https://giliycia.com.ar/media/catalog/product/cache/99c3ac325871812be19f74bdf645f821/1/0/106310_01
    #         .jpg"
    #     />
    # </div>
    photo_wrapper = soup.find('div', class_='gallery-placeholder _block-content-loading')
    photo = photo_wrapper.find('img')['src']
    print("photo" + photo)
    photo = photo or 'Not found'
    return photo


def get_price(soup):
    # the price is in <span id="product-price-17495" data-price-amount="20421.76" data-price-type="finalPrice"
    # class="price-wrapper " itemprop="price"><span class="price">$20.421,76</span></span>
    price = soup.find('span', class_='price').text
    price = money_tools.money_parser.round_price(price)
    price = price or 'Not found'
    return price


class GiliItemScrapper(ItemScrapper):
    def scrap_item_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        price = get_price(soup)
        product_updated_data = {
            'price': price,
        }
        return product_updated_data
