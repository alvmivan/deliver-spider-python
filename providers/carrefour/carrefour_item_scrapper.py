from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper


def get_photo(soup):
    # the photo is in <div class="vtex-store-components-3-x-productImage
    # vtex-store-components-3-x-productImage--product-view-images-selector"><div class="relative"><div
    # style="transform-origin: 0px 0px; font-size: 0px; transform: scale(1, 1) translate3d(0px, 0px, 0px);"><img
    # data-vtex-preload="true" class="vtex-store-components-3-x-productImageTag
    # vtex-store-components-3-x-productImageTag--product-view-images-selector
    # vtex-store-components-3-x-productImageTag--main
    # vtex-store-components-3-x-productImageTag--product-view-images-selector--main"
    # src="https://carrefourar.vtexassets.com/arquivos/ids/169374-800-auto?v=637468496694400000&amp;width=800&amp
    # ;height=auto&amp;aspect=true" srcset="https://carrefourar.vtexassets.com/arquivos/ids/169374-600-auto?v
    # =637468496694400000&amp;width=600&amp;height=auto&amp;aspect=true 600w,
    # https://carrefourar.vtexassets.com/arquivos/ids/169374-800-auto?v=637468496694400000&amp;width=800&amp;height
    # =auto&amp;aspect=true 800w,https://carrefourar.vtexassets.com/arquivos/ids/169374-1200-auto?v
    # =637468496694400000&amp;width=1200&amp;height=auto&amp;aspect=true 1200w" alt="7798118962329_01_a"
    # title="7798118962329_01_a" loading="eager" sizes="(max-width: 64.1rem) 100vw, 50vw" crossorigin="anonymous"
    # style="width: 100%; height: 100%; max-height: 600px; object-fit: contain;"></div></div></div>
    photo_wrapper = soup.find('div',
                              class_='vtex-store-components-3-x-productImage '
                                     'vtex-store-components-3-x-productImage--product-view-images-selector')
    photo = photo_wrapper.find('img')['src']
    photo = photo or 'No photo found'
    return photo


def get_price(soup):
    # encontrar esto:<meta property="product:price:amount" content="3795" data-react-helmet="true">
    price = soup.find('meta', property='product:price:amount')['content']

    if not price:
        raise 'No price found'

    return money_tools.money_parser.round_price(price)


def old_get_price(soup):
    # find all the price pieces and concatenate them
    # <span class="valtech-carrefourar-product-price-0-x-currencyInteger">99</span>

    selling_price = soup.find('span', class_='valtech-carrefourar-product-price-0-x-currencyContainer')
    price_pieces = selling_price.find_all('span', class_='valtech-carrefourar-product-price-0-x-currencyInteger')
    price = ''.join([piece.text for piece in price_pieces])
    price = price or 'No price found'
    return price


class CarrefourItemScrapper(ItemScrapper):
    def scrap_item_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # price = get_price(soup)

        product_updated_data = {
            'price': price,
        }
        return product_updated_data
