from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper


def get_photo(soup):
    # the photo is in <img data-vtex-preload="true" class="vtex-store-components-3-x-productImageTag
    # vtex-store-components-3-x-productImageTag--cl-imgProduct vtex-store-components-3-x-productImageTag--main
    # vtex-store-components-3-x-productImageTag--cl-imgProduct--main"
    # src="https://masonlineprod.vtexassets.com/arquivos/ids/283269-800-auto?v=638198806029200000&amp;width=800&amp
    # ;height=auto&amp;aspect=true" srcset="https://masonlineprod.vtexassets.com/arquivos/ids/283269-600-auto?v
    # =638198806029200000&amp;width=600&amp;height=auto&amp;aspect=true 600w,
    # https://masonlineprod.vtexassets.com/arquivos/ids/283269-800-auto?v=638198806029200000&amp;width=800&amp;height
    # =auto&amp;aspect=true 800w,https://masonlineprod.vtexassets.com/arquivos/ids/283269-1200-auto?v
    # =638198806029200000&amp;width=1200&amp;height=auto&amp;aspect=true 1200w"
    # alt="Calefactor-Longvie-Tiro-Balanceado-Eba3s-3000kc-1-43208"
    # title="Calefactor-Longvie-Tiro-Balanceado-Eba3s-3000kc-1-43208" loading="eager" sizes="(max-width: 64.1rem)
    # 100vw, 50vw" crossorigin="anonymous" style="width: 100%; height: 100%; max-height: 600px; object-fit: contain;">
    photo = soup.find('img', class_='vtex-store-components-3-x-productImageTag')
    if photo:
        photo = photo['src']
    photo = photo if photo else 'Not found'
    return photo


def get_price(soup):
    # the price is in <div class="valtech-gdn-dynamic-product-0-x-dynamicProductPrice mb4">$169.499,50</div>
    price = soup.find('div', class_='valtech-gdn-dynamic-product-0-x-dynamicProductPrice')
    if price:
        price = price.text
    price = money_tools.money_parser.round_price(price)
    price = price if price else 'Not found'
    return price


class ChangomasItemScrapper(ItemScrapper):
    def scrap_item_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        price = get_price(soup)
        product_updated_data = {
            'price': price,
        }
        return product_updated_data
