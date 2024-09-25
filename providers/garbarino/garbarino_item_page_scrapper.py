from bs4 import BeautifulSoup

import money_tools.money_parser

from data_unification.item_scrapper import ItemScrapper


def get_photo(soup):
    # the photo is in <div class="ratio-box ratio-image product-images-carousel__image" style="width:100%;"
    # data-v-536d58b2="" data-v-6a796a72="" data-v-de5595f6=""><div class="ratio-box__sizer"
    # style="padding-bottom:100%;" data-v-536d58b2=""></div><div class="ratio-box__slot"
    # data-v-536d58b2=""><!----><img alt="Caloventor Estufa BKF 2000W BF-FH2000 Gris Resistencia"
    # src="https://d2eebw31vcx88p.cloudfront.net/garbarino/uploads/e52add50e7104724d4511efbda292ac7d652e229.jpg.webp"
    # class="ratio-image__image" style="object-fit:contain;object-position:center;" data-v-536d58b2=""
    # data-v-6a796a72=""><div class="ratio-image__content" data-v-536d58b2="" data-v-6a796a72=""></div></div></div>
    photo = soup.find('div', {'class': 'ratio-box ratio-image product-images-carousel__image'}).find('img')['src']
    photo = photo or 'No photo found'
    return photo


def get_price(soup):
    # the price is in <div class="text-no-wrap mr-2 price text-start font-8" data-v-592c7530=""
    # data-v-ace2f122=""><span data-v-592c7530=""></span><span class="mr-1" data-v-592c7530="">$</span><span
    # data-v-592c7530="">41.200</span><!----></div>
    price_wrapper = soup.find('div', {'class': 'text-no-wrap mr-2 price text-start font-8'})
    # the real price is in the span with class="mr-1" data-v-592c7530="". Search it by class
    price = price_wrapper.find('span', {'class': 'mr-1'}).find_next_sibling('span').text
    price = money_tools.money_parser.round_price(price)
    price = price or 'No price found'
    return price


class GarbarinoItemScrapper(ItemScrapper):
    def scrap_item_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        price = get_price(soup)
        product_updated_data = {
            'price': price,
        }
        return product_updated_data
