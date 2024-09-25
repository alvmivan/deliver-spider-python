from bs4 import BeautifulSoup

import money_tools.money_parser
from data_unification.item_scrapper import ItemScrapper


def get_photo(soup):
    # the photo is in <a href="//acdn.mitiendanube.com/stores/003/564/648/products
    # /lyectn_product_img_att4210821340186624646-957df0341af92c257717157060650434-1024-1024.webp"
    # data-fancybox="product-gallery" class="js-product-slide-link d-block position-relative" style="padding-bottom:
    # 100%;">
    # <img src="//acdn.mitiendanube.com/assets/themes/toluca/static/images/empty-placeholder.png"
    # data-srcset="//acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-480-0.webp 480w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-640-0.webp 640w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-1024-1024.webp 1024w" data-sizes="auto" class="js-product-slide-img
    # product-slider-image img-absolute img-absolute-centered lazyautosizes lazyloaded" alt="Estufa eléctrica 1600W"
    # sizes="540px" srcset="//acdn.mitiendanube.com/stores/003/564/648/products
    # /lyectn_product_img_att4210821340186624646-957df0341af92c257717157060650434-480-0.webp 480w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-640-0.webp 640w,
    # //acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-1024-1024.webp 1024w">
    # <img src="//acdn.mitiendanube.com/stores/003/564/648/products/lyectn_product_img_att4210821340186624646
    # -957df0341af92c257717157060650434-50-0.webp" class="js-product-slide-img product-slider-image img-absolute
    # img-absolute-centered blur-up" alt="Estufa eléctrica 1600W">
    # </a>
    # the photo is in the scr of the a tag
    photo = soup.find('a', class_='js-product-slide-link d-block position-relative')['href']
    # add https: to the photo and change the extension from tmp to webp
    photo = photo or 'Not found'
    photo = 'https:' + photo.replace('.tmp', '.webp')
    return photo


def get_price(soup):
    # the price is in <div class="price-container" data-store="product-price-212595593">
    # <div class="mb-3">
    # <span class="d-inline-block">
    # <div class="js-price-display h3" id="price_display" data-product-price="4959000">$49.590,00</div>
    # </span>
    # <span class="d-inline-block h3 font-weight-normal">
    # <div id="compare_price_display" class="js-compare-price-display price-compare" style="display:none;"></div>
    # </span>
    # </div>
    # <div data-toggle="#installments-modal" data-modal-url="modal-fullscreen-payments" class="js-modal-open
    # js-fullscreen-modal-open js-product-payments-container mb-3">
    # <div class="js-max-installments-container js-max-installments mb-2">
    # <div class="js-max-installments product-installments">
    # <span class="js-installment-amount product-installment-amount">18</span>
    # <span>
    # <span class="installment-short-separator">
    # x
    # </span>
    # </span>
    # <span class="js-installment-price product-installment-value">$6.512,82</span>
    # </div>
    # </div>
    # <a id="btn-installments" class="btn-link font-small">
    # Ver más detalles
    # </a>
    # </div>
    # </div>
    price = soup.find('div', class_='js-price-display h3').text
    price = money_tools.money_parser.round_price(price)
    price = price or 'Not found'
    return price


class HipertehuelcheItemScrapper(ItemScrapper):
    def scrap_item_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        price = get_price(soup)
        product_updated_data = {
            'price': price,
        }
        return product_updated_data
