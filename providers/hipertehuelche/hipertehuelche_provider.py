from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper
from data_unification.items_provider import ItemsProvider
from providers.hipertehuelche.hipertehuelche_item_page_scrapper import HipertehuelcheItemScrapper
from utils import get_html


def create_search_url(search_term):
    # if i search for "smart tv" the url will be https://www.hipertehuelche.com/search/?q=smart+tv
    search_term = search_term.replace(' ', '+')
    return f'https://www.hipertehuelche.com/search/?q={search_term}'


def get_items(soup):
    items = soup.find_all('div', class_='js-item-product col-6 col-md-2-4 item-product col-grid')
    return items


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


def get_name(item):
    # the name is in <div class="js-item-name item-name mt-1 mb-3 font-small opacity-80"
    # data-store="product-item-name-212595593">Estufa eléctrica 1600W</div>
    name = item.find('div', class_='js-item-name item-name mt-1 mb-3 font-small opacity-80').text or 'Not found'
    print(name)
    return name


def get_price(item):
    # the price is in <div class="item-price-container" data-store="product-item-price-212595593">
    # <span class="js-price-display item-price mr-1 h5 font-weight-bold">
    # $49.590,00
    # </span>
    # <span class="js-compare-price-display price-compare mt-1 ml-0" style="display:none;">
    # $0,00
    # </span>
    # </div>
    price = item.find('span', class_='js-price-display item-price mr-1 h5 font-weight-bold').text
    price = money_tools.money_parser.round_price(price)
    price = price or 'Not found'
    print(price)
    return price


def get_url(item):
    url = item.find('a')['href']
    return url


def get_photo(item):
    # the photo is in <div class="js-image-container  item-image">
    # <div style="padding-bottom: 100%;" class="js-item-image-padding position-relative"
    # data-store="product-item-image-212595593">
    # <a href="https://www.hipertehuelche.com/productos/estufa-electrica-1600w/" title="Estufa eléctrica 1600W"
    # aria-label="Estufa eléctrica 1600W">
    # <img alt="Estufa eléctrica 1600W" data-expand="-10"
    # src="//acdn.mitiendanube.com/assets/themes/toluca/static/images/empty-placeholder.png"
    # data-srcset="//acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-240-0.webp 240w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-320-0.webp 320w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-480-0.webp 480w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-640-0.webp 640w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-1024-1024.webp 1024w" class="js-item-image lazyautosizes img-absolute
    # img-absolute-centered fade-in lazyloaded" width="1080" height="1080" sizes="(max-width: 768px) 50vw,
    # (min-width: 769px) 50vw" srcset="//acdn.mitiendanube.com/stores/003/564/648/products
    # /lyectn_product_img_att4210821340186624646-957df0341af92c257717157060650434-240-0.webp 240w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-320-0.webp 320w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-480-0.webp 480w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-640-0.webp 640w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-1024-1024.webp 1024w">
    # <div class="placeholder-fade">
    # </div>
    # </a>
    # </div>
    # <div class=" labels-absolute mb-2">
    # <div class="js-stock-label label label-default " style="display:none;">Sin stock</div>
    # </div>
    # <span class="hidden" data-store="stock-product-212595593-15"></span> </div>
    img_tag = item.find('img')
    photo = None
    if img_tag and img_tag.has_attr('data-srcset'):
        data_srcset = img_tag['data-srcset']
        # Dividir en los diferentes tamaños de imagen
        urls = [url.split()[0] for url in data_srcset.split(',')]
        photo = urls[0] if urls else None
    # the photo ends in .tmp, we need to remove it and put the correct extension
    if photo:
        photo = photo.replace('.tmp', '.webp')
    # the url starts with //, we need to add https: to the url
    if photo:
        photo = 'https:' + photo
    photo = photo or 'Not found'
    return photo


class HipertehuelcheProvider(ItemsProvider):

    def find_items(self, search_term):
        search_url = create_search_url(search_term)
        html = get_html(search_url)
        soup = BeautifulSoup(html, 'html.parser')
        html_items = get_items(soup)
        return [extract_item_info(item) for item in html_items]

    def update_item_data(self, item_url):
        item_scrapper: ItemScrapper = HipertehuelcheItemScrapper()
        html = get_html(item_url)
        return item_scrapper.scrap_item_data(html)

    def provider_id(self):
        return 'hipertehuelche'

    def get_categories(self):
        return ['obra', 'electronica']
