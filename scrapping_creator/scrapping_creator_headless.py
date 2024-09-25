import sys

from scrapping_creator.scrapping_creator_core import get_all_categories, get_initial_info_for_category, make_a_search
from utils import console_input


def headless_search():
    # nos fijamos si en los parameters hay alguna categoria
    categories = get_all_categories()
    categories_in_parameters = []

    for arg in sys.argv:
        if arg in categories:
            categories_in_parameters.append(arg)

    if len(categories_in_parameters) == 0:  # if not category is specified, we search in all categories
        categories_in_parameters = categories

    for category in categories_in_parameters:
        category_items, category_providers = get_initial_info_for_category(category)
        print("will search in category", category.capitalize())
        print("will search the next ", len(category_items), " items : ", category_items)
        print("will search in the next providers: ")
        providers_accepted = []
        # ask with input for each provider
        for provider in category_providers:
            print(f"do you want to search in {provider.provider_id().capitalize()}? (y/n)")
            answer = console_input()
            if answer.lower() in ['y', 'yes', 's', 'si', '']:
                providers_accepted.append(provider)

        # providers names
        providers_names = [p.provider_id().capitalize() for p in providers_accepted]

        print("will search in the next providers: ", providers_names)

        search_items, calculated_amount_of_requests = make_a_search(category_items, providers_accepted)

        amount_of_requests = calculated_amount_of_requests
        # will search (amount) items, do you want to reduce the amount ? (if number clamp else continue)
        print(
            f"will search {amount_of_requests} items, do you want to reduce the amount ? (if number clamp else "
            f"continue)")
        answer = console_input(
            "Set Initial And Amount (or only amount, and initial will be 0 by default), or type cancel to go back")

        # si la respuesta tiene 2 numeros separados por espacio se hace un rango, sino el rango es de 0 al numero
        amount_min = 0

        if len(answer.split()) == 2:
            amount_min, amount_max = answer.split()
            amount_min = int(amount_min)
            amount_of_requests = int(amount_max)
        elif answer.isdigit():
            amount_of_requests = int(answer)
        elif answer.lower() == "cancel":
            return
        else:
            print(f"continuing with the same amount of requests {amount_of_requests}")

        iterator = search_items(skip=amount_min)

        mute_search = "--mute-search" in sys.argv
        only_amount_search = "--only-amount-search" in sys.argv

        calculated_amount_of_requests += 1
        for i in range(calculated_amount_of_requests*2):
            try:
                iter_label = (next(iterator))
                if not mute_search or only_amount_search:
                    print(iter_label)

            except StopIteration:
                break

        print("done")
