import os
import sys

from data_unification.items_data_manager import search, is_data_already_created
from providers.bahia_construcciones.bahia_construcciones_provider import BahiaConstruccionesProvider
from providers.carrefour.carrefour_provider import CarrefourProvider
from providers.changomas.changomas_provider import ChangomasProvider
from providers.coope.coope_provider import CooperativaProvider
from providers.fravega.fravega_provider import FravegaProvider
from providers.garbarino.garbarino_provider import GarbarinoProvider
from providers.gili.gili_provider import GiliProvider
from providers.hipertehuelche.hipertehuelche_provider import HipertehuelcheProvider
from utils import console_input

# aca vamos a listar los proveedores y las categorias

providers = [
    GiliProvider(),
    FravegaProvider(),
    GarbarinoProvider(),
    ChangomasProvider(),
    CooperativaProvider(sleep=20),
    CarrefourProvider(timeout=4, sleep=4, use_selenium=True, scroll=1200),
    HipertehuelcheProvider(),
    BahiaConstruccionesProvider()
]

# aca vamos a levantar las categorias
categories_folder = "categories/"

# leemos de la folder todos los archivos que terminen en .txt y los metemos en un diccionario con el nombre del archivo
categories = {}
provider_for_category = {}


def initialize_categories():
    for file in os.listdir(categories_folder):
        if file.endswith(".txt"):
            with open(categories_folder + file, 'r', encoding='utf-8') as f:
                batch = f.read().splitlines()
                key = file.replace('.txt', '')
                categories[key] = batch
                provider_for_category[key] = []
    for category in categories.keys():
        for provider in providers:
            if provider.can_handle_category(category):
                provider_for_category[category].append(provider)

    for category in categories.keys():
        print(category.capitalize())
        print("Providers:")
        for provider in provider_for_category[category]:
            print(f" - {provider.provider_id().capitalize()}")
        print("")


def get_all_categories():
    return categories.keys()


def get_initial_info_for_category(category):
    category_items = categories[category]
    category_providers = provider_for_category[category]
    return category_items, category_providers


def make_a_search(category_items, category_providers):
    skip_created = "--skip-existing" in sys.argv

    if skip_created:
        print("Will skip created data")
    else:
        print("Will override and search all data")
    amount_of_requests = len(category_items) * len(category_providers)

    def search_items(skip=0):
        counter = 0
        amount_skipped = 0
        only_amount_search = "--only-amount-search" in sys.argv
        if only_amount_search:
            continue_only = console_input("Only amount search mode, press enter to continue or type NO to cancel")
            if continue_only.lower() == "no":
                only_amount_search = False

        for search_term in category_items:
            for provider in category_providers:
                if amount_skipped < skip:
                    amount_skipped += 1
                    continue
                counter += 1
                counter_label = F"({counter} / {amount_of_requests})"
                search_label = f"{search_term.capitalize()} in {provider.provider_id().capitalize()} {counter_label}"

                if skip_created and is_data_already_created(provider, search_term):
                    if not only_amount_search:
                        yield counter_label + "(skipped)"
                    else:
                        yield f"- found, will skip: {search_label}"
                else:
                    if not only_amount_search:
                        yield counter_label
                    else:
                        yield f"+ searching: {search_label}"
                    search(provider, search_term)
            yield "done"

    return search_items, amount_of_requests
