import pandas as pd

from data_unification import items_data_manager
import os

from data_unification.items_data_manager import load_csv_with_updated_data, load_source_csv, ensure_location
from utils import debug_log


def _match_with_seach_terms(search_terms: list, token):
    for search_term in search_terms:
        if search_term in token.lower():
            return True
    return False


def _get_matching_rows(search_terms: list, file_name):
    # si no es un csv return data frame vacio
    if not file_name.endswith(".csv"):
        return None




    # si el search_term no esta en el nombre del archivo return lista vacia
    # levantar el archivo csv como un data frame
    df = load_csv_with_updated_data(file_name)
    # si el search_term coincide con la busqueda retornar todo el dataframe

    if _match_with_seach_terms(search_terms, file_name):
        return df

    # si no, retornar solo las filas que tengan el search_term en el campo name

    # iter rows
    rows = df.iterrows()
    matching_rows = []

    for index, row in rows:
        if _match_with_seach_terms(search_terms, row['name']):
            matching_rows.append(row)

    return pd.DataFrame(matching_rows)


# same but take a list of search terms
def get_items_for_search_terms(search_terms: list, max_elements=1000, order_by=None,
                               columns=("search_term", "name", "url", "price", "provider_id", "photo", "updated_at")):

    data_frames_folder = items_data_manager.data_frames_folder

    # vamos a levantar de aca todos los archivos que tengan el search_term en el nombre (pero terminen en {search_term}.csv)

    # creamos un nuevo dataframe para ir agregando los datos
    # if there is an order by and the field is not in the columns, add it

    columns = list(columns)
    if order_by and order_by['field'] not in columns:
        columns.append(order_by['field'])

    result_rows = []
    for file in os.listdir(data_frames_folder):
        df = _get_matching_rows(search_terms, file)
        # si está vacio o None continuar
        if df is None or df.empty:
            continue
        result_rows.append(df[columns])

    # result rows solo tiene las rows, los headers son la lista columns
    # crear un data frame con los headers y las rows
    if not result_rows:
        return []

    general_df = pd.concat(result_rows, ignore_index=True)
    general_df.columns = columns

    # if dataframe is empty return empty
    if general_df.empty:
        return []

    if order_by:
        is_asc = not order_by.get('descending', False)
        general_df = general_df.sort_values(by=order_by['field'], ascending=is_asc)

    # clamp max elements
    return general_df.head(max_elements).to_dict(orient='records')


def get_all_dataframes_for_provider(provider_id):
    data_frames_folder = items_data_manager.data_frames_folder

    for file in os.listdir(data_frames_folder):
        if file.startswith(provider_id):
            yield load_source_csv(file), data_frames_folder + file

