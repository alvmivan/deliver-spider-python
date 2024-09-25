import os
import random
from datetime import datetime

from data_unification.fail_searches import add_fail_search, is_fail_searches
from data_unification.items_provider import ItemsProvider

import pandas as pd

from utils import debug_log, debug_error

errors_file_name = "debug/errors.txt"
data_frames_folder = "data_frames/specific/"
updates_folder = "data_frames/updates/"
general_data_frame = "data_frames/general_data_frame.csv"
search_counter_data_frame = "data_frames/search_history.csv"


# will make sure we can create the file with pandas (if any directory is missing, create it)
def ensure_location(file_location):
    directory = os.path.dirname(file_location)
    if not os.path.exists(directory):
        os.makedirs(directory)


def report_errors_on_items(invalid_items):
    ensure_location(errors_file_name)
    with open(errors_file_name, "w+") as f:
        for item, error in invalid_items:
            print(f"Error: {error} on item: {item}")
            f.write(f"Error: {error} on item: {item}")
            f.write("\n")
            # write date and hour example "Sunday 13/October/2019 at 3:14PM"
            data_time = datetime.now().strftime("%A %d/%B/%Y at %I:%M%p")
            f.write(f"Date and hour: {data_time}")
            f.write("\n\n--------------------------------------------------\n\n")
    debug_error(f" {len(invalid_items)} Errors reported on file {errors_file_name}")


def is_data_already_created(provider, search_term):
    if is_fail_searches(f"{provider.provider_id()}_{search_term}"):
        return True

    file_name = f"{data_frames_folder}{provider.provider_id()}_{search_term}.csv"
    result = os.path.exists(file_name)
    return result


def search(provider: ItemsProvider, search_term: str):
    # first let's get the items
    valid_items, invalid_items = provider.get_items_and_validation_errors(search_term)

    # let's report the errors
    if invalid_items:
        report_errors_on_items(invalid_items)

    keys_order = [
        "search_term",
        "name",
        "url",
        "price",
        "provider_id",
        "photo",
        "details",
        "brand",
    ]

    df = pd.DataFrame(valid_items)
    df['provider_id'] = provider.provider_id()
    df['search_term'] = search_term

    # let's order the columns # but remember some columns may not be found in the data frame, then complete with None

    for key in keys_order:
        if key not in df:
            df[key] = ""

    df = df[keys_order]

    search_on_provider = f"{provider.provider_id()}_{search_term}"

    # if is empty then calladd_fail_search
    if df.empty:
        add_fail_search(search_on_provider)
        debug_log("No items found for search term: " + search_term)
        return

    file_location = f"{data_frames_folder}{search_on_provider}.csv"
    ensure_location(file_location)

    df.to_csv(file_location, index=False)
    debug_log(f"Data frame saved on {file_location}")


def update_general():
    # will load the general data frame
    general_df = pd.DataFrame()

    for file in os.listdir(data_frames_folder):
        if file.endswith(".csv"):
            df = pd.read_csv(data_frames_folder + file)
            general_df = pd.concat([general_df, df])

    ensure_location(general_data_frame)
    general_df.to_csv(general_data_frame, index=False)


def load_items_from_file(file_name):
    df = pd.read_csv(data_frames_folder + file_name)
    return df.to_dict(orient='records')


def _get_base_df(file):
    df = pd.read_csv(data_frames_folder + file)
    return df


def get_items_file_names():
    files = os.listdir(data_frames_folder)
    return [file for file in files if file.endswith(".csv")]


def get_items_file_names_and_df():
    files = os.listdir(data_frames_folder)
    return [(file, _get_base_df(file)) for file in files if file.endswith(".csv")]


def log_updated_info(updated_items, file_name, log_id):
    if not updated_items:
        debug_log(f"No updated items for {file_name}")
        return

    full_file_name = f"{updates_folder}log_{log_id}/{file_name}"
    ensure_location(full_file_name)
    try:
        df = pd.DataFrame(updated_items)

        df.to_csv(full_file_name, index=False)
    except ValueError as e:
        raise ValueError(f"Error creating the data frame with {updated_items} for {file_name} also error: {e}")


def folder_name_to_timestamp(folder_name):
    return datetime.strptime(folder_name[4:], '%d_%m_%Y__%H_%M_%S')


def _get_latest_log_folder(main_folder, file_target):
    """Gets the latest log folder within a main folder,
    searching for those starting with 'log_' and having a date format
    'DD_MM_AAAA__HH_MM_SS' in their name.

    Args:
      main_folder: The path to the main directory.

    Returns:
      The full path of the latest folder, or None if not found.
    """

    log_folders = []
    folder_items = os.listdir(main_folder)
    subfolders = [subfolder for subfolder in folder_items if
                  os.path.isdir(main_folder + subfolder) and subfolder.startswith("log_")]

    if not subfolders:
        return None

    for folder in subfolders:
        if folder.startswith("log_"):
            try:
                # Try to parse the date and time from the folder name
                date_time = folder_name_to_timestamp(folder)
                log_folders.append((date_time, folder))
            except ValueError:
                # If there's an error parsing, skip the folder

                pass

    if log_folders:
        latest_date, latest_folder = log_folders[0]
        # iterate and find the latest
        for date, folder in log_folders:
            # as a contition file_target should be in the folder
            if file_target not in os.listdir(main_folder + folder):
                continue
            if date > latest_date:
                latest_date = date
                latest_folder = folder

        full_path = os.path.join(main_folder, latest_folder)
        return full_path
    else:
        return None


def get_test_past_date(seed):
    # ayer a las 18:30
    # fixed date 3 de agosto de 2024 a las 12:31
    # para testear cuando aun no tienen una actualizacion guardada
    random.seed(seed)
    if random.choice([True, False]):
        return pd.Timestamp(year=2024, month=8, day=3, hour=12, minute=31)
    else:
        return pd.Timestamp.now().replace(hour=18, minute=30) - pd.Timedelta(days=1)


def load_source_csv(file_name):
    return pd.read_csv(data_frames_folder + file_name)


def load_csv_with_updated_data(file_name):
    # Cargar el archivo CSV en un DataFrame
    base_df = pd.read_csv(data_frames_folder + file_name)

    # Obtener la ruta completa del archivo
    file_path = os.path.join(data_frames_folder, file_name)

    # Obtener la fecha de creación del archivo
    creation_time = os.path.getctime(file_path)

    # Convertir la fecha de creación a un formato legible
    formatted_time = datetime.fromtimestamp(creation_time).strftime("%d_%m_%Y__%H_%M_%S")

    # Agregar la columna ["updated_at"] con la fecha de creación
    base_df["updated_at"] = datetime.strptime(formatted_time, '%d_%m_%Y__%H_%M_%S')

    print(formatted_time)
    # ahora vamos a buscar las carpetas que están en updates

    log_folder = _get_latest_log_folder(updates_folder, file_target=file_name)

    if log_folder is None:
        return base_df
    full_file_name = f"{log_folder}/{file_name}"
    if not os.path.exists(full_file_name):
        return base_df

    updated_df = pd.read_csv(full_file_name)

    base_df['price'] = updated_df['price']

    timestamp = folder_name_to_timestamp(log_folder.split("/")[-1])

    base_df['updated_at'] = timestamp
    print("cool", timestamp)
    return base_df

    # add a column called "is_updated" y en todas las rows que tenga true
    updated_df["is_updated"] = True

    # update the base_df with the updated_df
    return final_df
