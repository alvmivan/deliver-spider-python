from data_unification.item_data_sanitization import validate_field, sanitize_item


class ItemsProvider:
    def find_items(self, search_term):
        raise NotImplementedError()

    def provider_id(self):
        raise NotImplementedError()

    def update_item_data(self, item_url):
        raise NotImplementedError()

    def get_categories(self):
        return []

    def can_handle_category(self, category):
        categories = self.get_categories()
        return category in categories

    def __init__(self, timeout=10, sleep=10, scroll=0, use_selenium=False):
        self.timeout = timeout
        self.sleep = sleep
        self.scroll = scroll
        self.use_selenium = use_selenium

    def get_items_and_validation_errors(self, search_term):
        items = self.find_items(search_term)
        # validate items
        valid_items = []
        invalid_items = []
        for item in items:
            is_valid, error = validate_field(item)
            if is_valid:
                valid_items.append(sanitize_item(item))
            else:
                invalid_items.append((item, error))
        return valid_items, invalid_items
