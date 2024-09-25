from pprint import pprint

import requests
from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper
from data_unification.items_provider import ItemsProvider
from providers.carrefour.carrefour_item_scrapper import CarrefourItemScrapper
from utils import get_html


def create_search_url(search_term):
    # https://www.carrefour.com.ar/televisor%20de%2093%20pulgadas?_q=televisor%20de%2093%20pulgadas&map=ft
    # for "smart tv", the search url will be https://www.carrefour.com.ar/smart%20tv?_q=smart%tv&map=ft
    search_term = search_term.replace(' ', '%20')
    return f'https://www.carrefour.com.ar/{search_term}?_q={search_term}&map=ft'


# def get_items(soup):
#     items = soup.find('div', class_='valtech-carrefourar-product-summary-status-0-x-container')
#     return items


# def extract_item_info(item):
#     # print the item html data
#     print("Item html data:")
#     pprint(item)
#     name = get_name(item) or 'No name found'
#     price = get_price(item) or 'No price found'
#     photo = get_photo(item) or 'No photo found'
#     url = get_url(item) or 'No url found'
#     item_data = {
#         'name': name,
#         'price': price,
#         'photo': photo,
#         'url': url,
#         'details': 'No details found',
#         'brand': 'No brand found',
#     }
#     return item_data


# def get_url(item):
#     url = item.find('a')['href']
#     # append the base url to the url found
#     url = f'https://www.carrefour.com.ar{url}'
#     return url


# def get_photo(item):
#     photo = item.find('img')['src']
#     return photo


# def get_price(item):
#     # find the selling price of the product with element <span
#     # class="valtech-carrefourar-product-price-0-x-currencyContainer"><span
#     # class="valtech-carrefourar-product-price-0-x-currencyCode">$</span><span
#     # class="valtech-carrefourar-product-price-0-x-currencyLiteral">&nbsp;</span><span
#     # class="valtech-carrefourar-product-price-0-x-currencyInteger">99</span><span
#     # class="valtech-carrefourar-product-price-0-x-currencyGroup">.</span><span
#     # class="valtech-carrefourar-product-price-0-x-currencyInteger">000</span><span
#     # class="valtech-carrefourar-product-price-0-x-currencyDecimal">,</span><span
#     # class="valtech-carrefourar-product-price-0-x-currencyFraction">00</span></span>
#     selling_price = item.find('span', class_='valtech-carrefourar-product-price-0-x-currencyContainer')
#     # find all the price pieces and concatenate them
#     # <span class="valtech-carrefourar-product-price-0-x-currencyInteger">99</span>
#     price_pieces = selling_price.find_all('span', class_='valtech-carrefourar-product-price-0-x-currencyInteger')
#     price = ''.join([piece.text for piece in price_pieces])
#     return price


# def get_name(item):
#     # the name container is an element with html like this: <h3 class="vtex-product-summary-2-x-productNameContainer
#     # vtex-product-summary-2-x-productNameContainer--citrusProductName mv0 vtex-product-summary-2-x-nameWrapper
#     # vtex-product-summary-2-x-nameWrapper--citrusProductName overflow-hidden c-on-base f5"><span
#     # class="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-productBrand--citrusProductName
#     # vtex-product-summary-2-x-brandName vtex-product-summary-2-x-brandName--citrusProductName t-body">Convector
#     # Liliana convectory 2000W CNG17 </span></h3>
#     name_container = item.find('h3', class_='vtex-product-summary-2-x-productNameContainer')
#     # the name is in the span with class vtex-product-summary-2-x-productBrand
#     name = name_container.find('span', class_='vtex-product-summary-2-x-productBrand').text
#     return name


def soup_to_carrefour_items_info(soup):
    return [extract_info_from_product_image(item) for item in (get_product_images(soup))]


def inspect_html_node(img_node, parent_moves_up=2):
    current_node = img_node
    for i in range(parent_moves_up):
        current_node = current_node.parent


def get_product_images(soup):
    all_images = soup.find_all('img')
    # solo retornar las imagenes que tienen src y su src contiene el string "vtexassets.com"
    correct_images = [image for image in all_images if
                      image.has_attr('src') and ".vtexassets.com/arquivos/ids" in image['src']]
    print(len(correct_images))

    # por cada imagen vamos a inspeccionarla
    for img in correct_images:
        inspect_html_node(img, 6)

    return correct_images


def extract_info_from_product_image(html_image):
    item_info = {
        "name": "",
        "price": "",
        "photo": html_image['src'] if html_image.has_attr('src') else "No photo found",
        "url": "",
    }

    # ahora pedile el parent
    current_node = html_image

    # vamos a empezar a ir al parent del parent hasta que encontremos un href

    def parse_url(partial):
        return f"https://www.carrefour.com.ar{partial}"

    while current_node:
        if current_node.name == "a":
            url = parse_url(current_node['href'])
            item_info["url"] = url
        current_node = current_node.parent

    current_node = html_image

    # ahora vamos hacia arriba y buscamos un h3 con  class_='vtex-product-summary-2-x-productNameContainer')

    while current_node:
        # chequear si un hijo del nodo es h3 y tiene la clase correcta
        result_partial = current_node.find('h3', class_='vtex-product-summary-2-x-productNameContainer')
        if result_partial:
            # print("Found the parent h3")
            # print(result_partial)
            name = result_partial.find('span', class_='vtex-product-summary-2-x-productBrand').text
            # print(name)
            # imprimime el html de ese h3
            # print(result_partial.prettify())
            item_info["name"] = name
            break
        current_node = current_node.parent

    # encontrar precio
    current_node = html_image
    # vamos a ir para arriba hasta que algun elemento matchee con find("span",
    # class="valtech-carrefourar-product-price-0-x-currencyContainer")

    while current_node:
        result = current_node.find("span", class_="valtech-carrefourar-product-price-0-x-currencyContainer")
        if result:
            # print("Found the price")
            # print(result)
            price = ""
            for piece in result.find_all("span", class_="valtech-carrefourar-product-price-0-x-currencyInteger"):
                price += piece.text
            # print(price)
            item_info["price"] = money_tools.money_parser.round_price(price)
            break
        current_node = current_node.parent

    # print(item_info)
    return item_info


class CarrefourProvider(ItemsProvider):
    def find_items(self, search_term):
        search_url = create_search_url(search_term)
        html = get_html(search_url, use_selenium=True, timeout=5, scroll=1200, sleep=3)
        soup = BeautifulSoup(html, 'html.parser')
        return soup_to_carrefour_items_info(soup)

    def update_item_data(self, item_url):
        item_scrapper: ItemScrapper = CarrefourItemScrapper()

        # html = get_html(item_url, scroll=self.scroll, sleep=self.sleep, timeout=self.timeout, use_selenium=False,
        # use_content=True)
        from lxml import html
        content = requests.get(item_url).content

        tree = html.fromstring(content)

        price = tree.xpath('//meta[@property="product:price:amount"]/@content')
        print("The price is:")
        print(price)
        if not price:
            raise Exception('No price found when scraping the item with url: ' + item_url)

        # return a dictionary with the item data
        return {
            'price': money_tools.money_parser.round_price(price[0]),
        }

    def provider_id(self):
        return "carrefour"

    def get_categories(self):
        return ['almacen', 'electronica']
