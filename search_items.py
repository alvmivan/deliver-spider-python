from html_tools.html_unpacker import close_driver
from scrapping_creator.scrapping_creator_core import initialize_categories
from scrapping_creator.scrapping_creator_headless import headless_search
import sys

simulated_commands = ["--skip-existing", "--only-amount-search", "--yes-to-all"]

print("vamos a simular que lo llamamos con los comandos ", simulated_commands)

sys.argv = [sys.argv[0]] + simulated_commands  # [0] es el nombre del archivo


def print_arguments():
    print("Arguments:")
    print("--help: muestra los argumentos")
    print("--skip-existing: no busca los archivos ya creados")
    print("--mute-search: no muestra los resultados de la busqueda mientras se va realizando")
    print("--only-amount-search: solo muestra cuantos items van")
    print("--yes-to-all: envia un OK a todas las preguntas de la consola para ascelerar el proceso")
    print("[category_name_1 category_name_2 ...] : search only in the specified categories")


def main_search_program():
    try:
        if "--help" in sys.argv:
            print_arguments()
            return
        initialize_categories()
        headless_search()
    except Exception as e:

        print("\n\n ENVIAME ESTO:  \n\n" * 4)
        import traceback
        print(traceback.format_exc())
        print("\n" * 3)
        print(e)
        print("\n\n REVISAR ERRORES! \n\n" * 4)
    finally:
        close_driver()


if __name__ == '__main__':
    main_search_program()
