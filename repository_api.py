# levantame un flask
import json

import flask_cors as cors
from flask import Flask, jsonify

from api.configuration import GetSettings, UpdateSettings
from api.get_categories import GetCategoriesEndpoint
from api.searches import Searches
from api.set_categories import SetCategoriesEndpoint

# inicializa todo y hace un endpoint health
app = Flask(__name__)

# enable CORS
cors.CORS(app)


@app.route('/health')
def health():
    return jsonify({'status': 'UP'})


# este endpoint POST va a recibir un json que tiene un campo "search_terms" con una lista de los search_terms
# vamos a peirle a products_repository que busque esos terminos en todos los providers, basicamente vamos a wrappear
# products_repository.get_searchs (usalo, yo despues lo implemento)


def json_do_dict(json_string):
    return json.loads(json_string)


# @app.route('/search', methods=['POST'])


# make default port 5000 get to display health
@app.route('/')
def default_page():
    # levantar server_fine.html y enviarlo
    with open("server_fine.html", "r+", encoding='utf-8') as file:
        return file.read()


# route endpoints

if __name__ == '__main__':
    Searches(app)
    GetSettings(app)
    UpdateSettings(app)
    GetCategoriesEndpoint(app)
    SetCategoriesEndpoint(app)
    print("Starting API")
    app.run(port=5000, debug=True)
