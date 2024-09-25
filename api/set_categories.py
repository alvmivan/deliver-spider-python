import os
from flask import request, jsonify
from api.endpoint import EndPoint, BadRequest


class SetCategoriesEndpoint(EndPoint):
    def path(self):
        return '/set-categories'

    def method(self):
        return 'POST'

    def function(self):
        data = request.json
        if 'categories' not in data:
            raise BadRequest("Invalid payload: missing 'categories' key.")

        categories_dir = os.path.join(os.getcwd(), 'categories')
        if not os.path.exists(categories_dir):
            os.makedirs(categories_dir)

        for category in data['categories']:
            for category_name, items in category.items():
                file_path = os.path.join(categories_dir, f'{category_name}.txt')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(items))

        return jsonify({'status': 'success', 'message': 'Categories updated successfully.'})

    def doc(self):
        return {
            'description': 'Updates the categories on the server.',
            'parameters': {
                'categories': 'A list of categories to update, where each category is a dictionary with the category name as the key and a list of items as the value.'
            },
            'response': {
                'status': 'success or failure',
                'message': 'A message indicating the result of the operation.'
            }
        }
