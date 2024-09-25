import gc
import os
from datetime import datetime

from data_unification.items_data_manager import search
from html_tools.html_unpacker import initialize_driver, close_driver
from providers.bahia_construcciones.bahia_construcciones_provider import BahiaConstruccionesProvider
from providers.carrefour.carrefour_provider import CarrefourProvider
from providers.changomas.changomas_provider import ChangomasProvider
from providers.coope.coope_provider import CooperativaProvider
from providers.fravega.fravega_provider import FravegaProvider
from providers.garbarino.garbarino_provider import GarbarinoProvider
from providers.hipertehuelche.hipertehuelche_provider import HipertehuelcheProvider
from providers.vea.vea_provider import VeaProvider
from utils import console_input

providers = [
    # GiliProvider(),
    # FravegaProvider(),
    # GarbarinoProvider(),
    # ChangomasProvider(),
    # CooperativaProvider(sleep=20),
    # CarrefourProvider(timeout=4, sleep=4, use_selenium=True, scroll=1200)
    # HipertehuelcheProvider()
    # BahiaConstruccionesProvider()
    VeaProvider()
]

search_batches_folder = "categories/"
search_batches = {}

for file in os.listdir(search_batches_folder):
    if file.endswith(".txt"):
        with open(search_batches_folder + file, 'r') as f:
            batch = f.read().splitlines()
            search_batches[file.replace('.txt', '')] = batch


def perform_search(provider, item):
    try:
        search(provider, item)
        print("- ", end='')
    except Exception:
        print("X ", end='')


def perform_many_searches_single_thread(items):
    for item_index in range(len(items)):
        item = items[item_index]
        print(f"\nSearching for {item} ({item_index + 1}/{len(items)})")
        print("" + ("_ " * len(providers)))
        gc.collect()
        for provider in providers:
            perform_search(provider, item)


def search_batch(batch_key):
    input(f"Searching for batch {batch_key}, with {len(search_batches[batch_key])} items. Press enter to continue...")
    perform_many_searches_single_thread(search_batches[batch_key])


if __name__ == '__main__':
    testing_batch = console_input("Are you running a batch? (y/n): ")
    if testing_batch == 'y':
        initial_time = datetime.now()
        search_batch("almacen")
        final_time = datetime.now()
        exit()
    else:
        search_term = console_input('Enter a product name: ') or 'herramienta'
        list_of_providers = [provider.provider_id() for provider in providers]
        msj = "will search in " + ", ".join(list_of_providers)
        print(msj)
        for provider in providers:
            search(provider, search_term)

    close_driver()
