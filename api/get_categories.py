import os
from flask import jsonify
from api.endpoint import EndPoint, BadRequest


class GetCategoriesEndpoint(EndPoint):
    def path(self):
        return '/get-categories'

    def method(self):
        return 'GET'

    def function(self):
        categories_dir = os.path.join(os.getcwd(), 'categories')
        if not os.path.exists(categories_dir):
            raise BadRequest("Categories directory does not exist.")

        categories = []
        for filename in os.listdir(categories_dir):
            if filename.endswith('.txt'):
                category_name = os.path.splitext(filename)[0]
                with open(os.path.join(categories_dir, filename), 'r', encoding='utf-8') as file:
                    items = [line.strip() for line in file.readlines()]
                    categories.append({category_name: items})

        return jsonify({'categories': categories})

    def doc(self):
        return {
            'description': 'Fetches all categories from the server.',
            'response': {
                'categories': 'A list of categories, where each category is a dictionary with the category name as the key and a list of items as the value.'
            }
        }
