import time
import tkinter as tk
from tkinter import ttk

from scrapping_creator.scrapping_creator_core import get_all_categories, get_initial_info_for_category, make_a_search

selected_category = None
selected_category_items = []
selected_providers = []
all_categories = get_all_categories()


def update_view(items_frame, providers_frame):
    for widget in items_frame.winfo_children():
        widget.destroy()
    for widget in providers_frame.winfo_children():
        widget.destroy()

    def _remove_item(i):
        selected_category_items.remove(i)
        update_view(items_frame, providers_frame)

    def _remove_provider(p):
        selected_providers.remove(p)
        update_view(items_frame, providers_frame)

    for item in selected_category_items:
        label = tk.Label(items_frame, text=item)
        label.pack()
        # y una X para borrarlo
        button = tk.Button(items_frame, text="X", command=lambda i=item: _remove_item(i))
        button.pack()

    for provider in selected_providers:
        label = tk.Label(providers_frame, text=provider.provider_id().replace('_',' ').capitalize())
        label.pack()
        # y una X para borrarlo de la lista
        button = tk.Button(providers_frame, text="X", command=lambda p=provider: _remove_provider(p))
        button.pack()


def select_category(category, providers_frame, items_frame):
    global selected_category
    global selected_category_items
    global selected_providers

    selected_category = category
    selected_category_items, selected_providers = get_initial_info_for_category(category)

    print("category selected", selected_category)
    print("items selected", selected_category_items)
    print("providers selected", selected_providers)

    update_view(items_frame, providers_frame)


def search_with(selected_category_items, selected_providers):
    root = tk.Tk()
    root.title("Search Items")
    root.geometry("600x300")

    # vamos a hacer una barra de progreso para mostrar el progreso de la busqueda
    progress = tk.DoubleVar()
    progress.set(0)
    progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=600, mode='determinate', variable=progress)
    progress_bar.pack(pady=20)

    # vamos a hacer una etiqueta para mostrar el progreso de la busqueda
    label = ttk.Label(root, text="Ready to start searching", font=("Helvetica", 16))
    label.pack(pady=24)

    # la busqueda ya se inicio asique pedimos el make a search
    search_items, amount_of_requests = make_a_search(selected_category_items, selected_providers)

    # iteramos el generador
    iterator = search_items()
    for item_index in range(amount_of_requests):
        status_label = next(iterator)
        time.sleep(0.1)
        completed = item_index
        progress.set(completed / amount_of_requests * 100)
        label.config(text=f"Searching {completed + 1} of {amount_of_requests} \n {status_label}")
        root.update_idletasks()

    label.config(text="Items searched successfully")
    progress.set(100)

    root.mainloop()


def config_providers_frame(providers_frame):
    # will have 600 width and 300 height with a scroll bar, also a title providers

    providers_frame.config(width=600, height=300)
    providers_frame.pack_propagate(False)

    providers_label = tk.Label(providers_frame, text="Providers")
    providers_label.pack()

    providers_frame.pack()


def config_items_frame(items_frame):
    # will have 600 width and 300 height with a scroll bar also a title items
    items_frame.config(width=600, height=300)
    items_frame.pack_propagate(False)

    items_label = tk.Label(items_frame, text="Items")
    items_label.pack()

    items_frame.pack()


def draw_searching_view():
    # vamos a hacer una app TK
    root = tk.Tk()
    root.title("Search Items")

    # Create a canvas and add a scrollbar
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold all content
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Pack the scrollbar and canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Update the scrollregion of the canvas
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Create and pack the provider and item frames inside the content_frame
    providers_frame = tk.Frame(content_frame)
    items_frame = tk.Frame(content_frame)

    # Create buttons for categories
    for category in all_categories:
        category_button = tk.Button(content_frame, text=category,
                                    command=lambda c=category: select_category(c, providers_frame, items_frame))
        category_button.pack()

    category_button = tk.Button(content_frame, text="Search",
                                command=lambda: search_with(selected_category_items, selected_providers))
    category_button.pack()

    config_providers_frame(providers_frame)
    config_items_frame(items_frame)

    # Update scroll region after adding frames
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    root.mainloop()
