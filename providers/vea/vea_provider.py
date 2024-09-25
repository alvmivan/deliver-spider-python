from pprint import pprint

from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper
from data_unification.items_provider import ItemsProvider
from providers.vea.vea_item_page_scrapper import VeaItemScrapper
from utils import get_html


def create_search_url(search_term):
    # si busco smart tv https://www.vea.com.ar/smart%20tv?_q=smart%20tv&map=ft
    search_term = search_term.replace(' ', '%20')
    return f'https://www.vea.com.ar/{search_term}?_q={search_term}&map=ft'


def get_items(soup):
    # the items container has the id gallery-layout-container
    items_container = soup.find('div', id='gallery-layout-container')
    # each child of the container is an item and has classes vtex-search-result-3-x-galleryItem
    # vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--grid pa4
    if items_container is None:
        print("No items found")
    else:
        print("Items container found")
    items = items_container.find_all('div',
                                     class_='vtex-search-result-3-x-galleryItem '
                                            'vtex-search-result-3-x-galleryItem--normal '
                                            'vtex-search-result-3-x-galleryItem--grid pa4')
    return items


def get_name(item):
    # the name is in <h2 class="vtex-product-summary-2-x-productNameContainer mv0 vtex-product-summary-2-x-nameWrapper
    # overflow-hidden c-on-base f5"><span class="vtex-product-summary-2-x-productBrand
    # vtex-product-summary-2-x-brandName
    # t-body">Led 65 Crystal Uhd Samsung 4k Smart Tv </span></h2>
    name = item.find('h2',
                     class_='vtex-product-summary-2-x-productNameContainer mv0 vtex-product-summary-2-x-nameWrapper '
                            'overflow-hidden c-on-base f5').text
    name = name or 'Not found'
    return name


def get_price(item):
    # the price is in <div id="priceContainer" class="veaargentina-store-theme-1dCOMij_MzTzZOCohX1K7w" style="color:
    # rgb(
    # 77, 77, 77); margin-top: 0px;">$1.319.999</div>
    price = item.find('div', class_='veaargentina-store-theme-1dCOMij_MzTzZOCohX1K7w').text
    price = money_tools.money_parser.round_price(price)
    price = price or 'Not found'
    return price


def get_photo(item):
    # the item photo is in <div class="vtex-stack-layout-0-x-stackContainer
    # vtex-stack-layout-0-x-stackContainer--stack-shelf-main relative"><div class="vtex-stack-layout-0-x-stackItem
    # vtex-stack-layout-0-x-stackItem--stack-shelf-main vtex-stack-layout-0-x-stackItem--first
    # vtex-stack-layout-0-x-stackItem--stack-shelf-main--first " style="z-index: 5;"><div
    # class="vtex-product-summary-2-x-imageContainer vtex-product-summary-2-x-imageWrapper db w-100 center"><div
    # class="dib relative vtex-product-summary-2-x-imageContainer vtex-product-summary-2-x-imageStackContainer"><img
    # src="https://veaargentina.vtexassets.com/arquivos/ids/812908-500-auto?v=638440522426000000&amp;width=500&amp
    # ;height
    # =auto&amp;aspect=true" loading="eager" alt="Led 65 Crystal Uhd Samsung 4k Smart Tv"
    # class="vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image" fetchpriority="high"
    # crossorigin="anonymous"></div></div></div><div class="vtex-stack-layout-0-x-stackItem
    # vtex-stack-layout-0-x-stackItem--stack-shelf-main absolute top-0 left-0 w-auto h-auto
    # vtex-stack-layout-0-x-stackItem vtex-stack-layout-0-x-stackItem--stack-shelf-main
    # vtex-stack-layout-0-x-stackItem--box-cucarda vtex-stack-layout-0-x-stackItem--stack-shelf-main--box-cucarda"
    # style="z-index: 6;"><div class="vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--box-cucarda"><div
    # class="flex mt0 mb0 pt0 pb0    justify-start vtex-flex-layout-0-x-flexRowContent
    # vtex-flex-layout-0-x-flexRowContent--box-cucarda items-stretch w-100"><div class="pr0 items-stretch
    # vtex-flex-layout-0-x-stretchChildrenWidth   flex" style="width: 33%;"><div class="flagsContainer"><div
    # class="cuadrante1"><div class="cucardaContainer"><img
    # src="https://veaargentina.vtexassets.com/arquivos/cucarda_vea_rpa12csitcfds16al18sar.png"
    # alt="cucarda_vea_rpa12csitcfds16al18sar" class="vtex-cucarda" crossorigin="anonymous"></div></div><div
    # class="cuadrante3"><div class="cucardaContainer"><img
    # src="https://veaargentina.vtexassets.com/arquivos/cucarda_vea_rpa12cuotassimple16al18sar.png"
    # alt="cucarda_vea_rpa12cuotassimple16al18sar" class="vtex-cucarda"
    # crossorigin="anonymous"></div></div></div></div></div></div></div><div class="vtex-stack-layout-0-x-stackItem
    # vtex-stack-layout-0-x-stackItem--stack-shelf-main absolute top-0 left-0 w-auto h-auto
    # vtex-stack-layout-0-x-stackItem vtex-stack-layout-0-x-stackItem--stack-shelf-main
    # vtex-stack-layout-0-x-stackItem--shelf-main-hover-actions
    # vtex-stack-layout-0-x-stackItem--stack-shelf-main--shelf-main-hover-actions" style="z-index: 7;"><div
    # class="vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--shelf-main-hover-actions"><div class="flex mt0
    # mb0 pt0 pb0    justify-start vtex-flex-layout-0-x-flexRowContent
    # vtex-flex-layout-0-x-flexRowContent--shelf-main-hover-actions items-stretch w-100"><div class="pr0 items-stretch
    # vtex-flex-layout-0-x-stretchChildrenWidth   flex" style="width: 50%;"><div tabindex="0" role="button"
    # class="vtex-modal-layout-0-x-triggerContainer vtex-modal-layout-0-x-triggerContainer--shelf-main-quickview
    # bg-transparent pa0 bw0 dib"><div class="vtex-rich-text-0-x-container vtex-rich-text-0-x-container--buy-fast
    # flex tl
    # items-start justify-start t-body c-on-base"><div class="vtex-rich-text-0-x-wrapper
    # vtex-rich-text-0-x-wrapper--buy-fast"><p class="lh-copy vtex-rich-text-0-x-paragraph
    # vtex-rich-text-0-x-paragraph--buy-fast">Compra rápida</p></div></div></div></div><div class="pr0 items-stretch
    # vtex-flex-layout-0-x-stretchChildrenWidth   flex" style="width: 50%;"><button tabindex="0" class="vtex-button bw1
    # ba fw5 v-mid relative pa0 lh-solid br2 min-h-regular t-action bg-action-primary b--action-primary
    # c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer w-100 "
    # type="button"><div class="vtex-button__label flex items-center justify-center h-100 ph6 w-100 border-box "
    # style="padding-top: 0.25em; padding-bottom: 0.32em;"><div class="vtex-add-to-cart-button-0-x-buttonDataContainer
    # flex justify-center"><span class="vtex-add-to-cart-button-0-x-buttonText">Ver
    # Producto</span></div></div></button></div></div></div></div></div>
    photo = item.find('img', class_='vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image')['src']
    photo = photo or 'Not found'
    return photo


def get_url(item):
    # the url is in the a tag with classes vtex-product-summary-2-x-clearLink h-100 flex flex-column
    url = item.find('a', class_='vtex-product-summary-2-x-clearLink h-100 flex flex-column')['href']
    # we need to append the base url
    url = 'https://www.vea.com.ar' + url
    url = url or 'Not found'
    return url


def extract_item_info(item):
    name = get_name(item)
    price = get_price(item)
    photo = get_photo(item)
    url = get_url(item)
    details = "Not found"
    brand = "Not found"

    product_ = {
        'name': name,
        'price': price,
        'photo': photo,
        'url': url,
        'details': details,
        'brand': brand,
    }
    return product_


class VeaProvider(ItemsProvider):

    def find_items(self, search_term):
        search_url = create_search_url(search_term)
        html = get_html(search_url, use_selenium=True)
        soup = BeautifulSoup(html, 'html.parser')
        html_items = get_items(soup)
        return [extract_item_info(item) for item in html_items]

    def update_item_data(self, item_url):
        item_scrapper: ItemScrapper = VeaItemScrapper()
        html = get_html(item_url, use_selenium=True)
        return item_scrapper.scrap_item_data(html)

    def provider_id(self):
        return "vea"

    def get_categories(self):
        return ["almacen, electronica"]
