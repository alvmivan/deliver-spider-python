from flask import request, jsonify

from api.endpoint import BadRequest, EndPoint
from data_unification.item_repository import get_items_for_search_terms


def _validate_json(request_json):
    #validate order_by
    if 'order_by' in request_json:
        if not isinstance(request_json['order_by'], dict):
            raise BadRequest("The 'order_by' field must be a json")
        if 'field' not in request_json['order_by']:
            raise BadRequest("The 'order_by' field must have a 'field' field")
        if not isinstance(request_json['order_by']['field'], str):
            raise BadRequest("The 'field' field in 'order_by' must be a string")
        if 'descending' in request_json['order_by']: #it's optional
            if not isinstance(request_json['order_by']['descending'], bool):
                raise BadRequest("The 'descending' field in 'order_by' must be a bool")


    if 'search_terms' not in request_json:
        raise BadRequest("The request must have a 'search_terms' field")
    if not isinstance(request_json['search_terms'], list):
        raise BadRequest("The 'search_terms' field must be a list")
    for term in request_json['search_terms']:
        if not isinstance(term, str):
            raise BadRequest("The 'search_terms' field must be a list of strings")
    # count es opcional pero tiene que ser un int
    if 'count' in request_json and not isinstance(request_json['count'], int):
        raise BadRequest("The 'count' field must be an int")


def _search():
    try:
        request_json = request.json
        _validate_json(request_json)

        search_terms = request_json['search_terms']
        order_by = None
        if 'order_by' in request_json:
            order_by = request_json['order_by']



        max_elements = 400
        # si el json tiene un campo count lo uso como max_elements
        if 'count' in request_json:
            max_elements = min(request_json['count'], max_elements)

        json = get_items_for_search_terms(search_terms, max_elements, order_by)


        json_wrapper = {
            "data": json
        }
        return jsonify(json_wrapper), 200

    except BadRequest as e:
        return jsonify({'errore': str(e)}), 400
    except Exception as e:
        #print stacktrace
        import traceback
        traceback.print_exc()

        return jsonify({'errore': str(e)}), 500


class Searches(EndPoint):
    def method(self):
        return 'POST'

    def path(self):
        return "/search"

    def function(self):
        return _search()

    def doc(self):
        return {
            'method': 'POST',
            'description': 'Search for items in all providers',
            'parameters': {
                'search_terms': {
                    'type': 'list of strings',
                    'description': 'The search terms to look for in the providers'
                },
                'count': {
                    'type': 'int',
                    'description [OPTIONAL, DEFAULT=400]': 'The maximum number of items to return'
                },
                'order_by': {
                    'type': {
                        'field': 'string',
                        'descending': 'bool'
                    },
                    'description [OPTIONAL]': 'The field to order the results by and if it is descending [OPTIONAL, DEFAULT=False] or not'
                }
            }
        }
