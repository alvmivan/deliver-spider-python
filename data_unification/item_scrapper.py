from html_tools.html_unpacker import close_driver, config_selenium_speed
from utils import get_html


class ItemScrapper:

    def scrap_item_data(self, html):
        raise NotImplementedError('This method should be implemented by subclasses')
