import threading
import time
from tkinter import ttk
from data_updater.data_updater_core import update_data
import tkinter as tk

from html_tools.html_unpacker import close_driver, initialize_driver, config_selenium_speed
from utils import debug_log, debug_error

if __name__ == '__main__':
    config_selenium_speed(1.5, 3)
    initialize_driver((960, 1080))

    function, total = update_data()

    iterator = function()

    item_index = 0
    for item in iterator:
        try:
            item_index += 1
            debug_log(repr(["Updating item", item_index, "of", total]))
            debug_log(repr(item))
            debug_log("Updated")
        except StopIteration:
            debug_log("Item updated")
        except Exception as e:
            debug_log("\n\n ENVIAME ESTO:  \n\n" * 4)

            debug_error(e)
            debug_error("\n\n REVISAR ERRORES! \n\n" * 4)
    close_driver()
