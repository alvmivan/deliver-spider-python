import sys

import pandas as pd

from data_unification import items_data_manager
from providers.bahia_construcciones.bahia_construcciones_provider import BahiaConstruccionesProvider
from providers.carrefour.carrefour_provider import CarrefourProvider
from providers.changomas.changomas_provider import ChangomasProvider
from providers.coope.coope_provider import CooperativaProvider
from providers.fravega.fravega_provider import FravegaProvider
from providers.garbarino.garbarino_provider import GarbarinoProvider
from providers.gili.gili_provider import GiliProvider
from providers.hipertehuelche.hipertehuelche_provider import HipertehuelcheProvider
from utils import debug_error, debug_log

_providers = [
    GiliProvider(),
    FravegaProvider(),
    GarbarinoProvider(),
    ChangomasProvider(),
    CooperativaProvider(),
    CarrefourProvider(),
    HipertehuelcheProvider(),
    BahiaConstruccionesProvider()
]

# a set with the names of the providers as keys
product_providers = {provider.provider_id(): provider for provider in _providers}


def _get_provider(item):
    return product_providers[item['provider_id']]


def _update_item_data(item):
    provider = _get_provider(item)
    return provider.update_item_data(item['url'])


def _update_items(time_stamp):
    # get the file names
    files_and_dataframes = items_data_manager.get_items_file_names_and_df()
    dfs = [df for _, df in files_and_dataframes]

    # let's calculate how much rows are in total
    total_rows = 0
    for df in dfs:
        total_rows += len(df)

    def _internal_update_items():
        for (file_name, df) in files_and_dataframes:
            items = items_data_manager.load_items_from_file(file_name)
            updated_items = []
            for item in items:
                item_url = item['url']
                item_name = item['name']
                yield item_name
                try:
                    updated_item = _update_item_data(item)

                    # if updated_item is int
                    if type(updated_item) is int:
                        updated_item = {'price': updated_item, 'url': item_url}
                    else:
                        updated_item = {'price': updated_item['price'], 'url': item_url}
                    updated_items.append(updated_item)
                except Exception as e:
                    debug_error(e)
                    debug_error(f"Error updating item {item}: {e}")

            debug_log("SAVE FILE!!! Updated items: " + repr(updated_items))
            items_data_manager.log_updated_info(updated_items, file_name, time_stamp)

        yield "end"

    return _internal_update_items, total_rows


def update_data():
    # create timestamp with format DD_MM_YYYY__HH_MM_SS
    time_stamp = pd.Timestamp.now().strftime("%d_%m_%Y__%H_%M_%S")
    # update the items
    return _update_items(time_stamp)
