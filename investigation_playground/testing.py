import requests

from html_tools.html_unpacker import fetch_dynamic_html

page_file = "html_page_example.html"


def create_search_url_carefour(search_term):
    search_term = search_term.replace(' ', '%20')
    return f'https://www.carrefour.com.ar/{search_term}?_q={search_term}&map=ft'


def save_page():
    url = "https://www.carrefour.com.ar/televisor%20de%2093%20pulgadas?_q=televisor%20de%2093%20pulgadas&map=ft"
    url = create_search_url_carefour("smart tv samsung")
    print(url)
    content = fetch_dynamic_html(url)

    with open(page_file, "w+", encoding="utf-8") as f:
        f.write(content)


# save_page()

# print("Page saved in", page_file)


def read_page():
    with open(page_file, "r", encoding="utf-8") as f:
        html = f.read()

    # levanto un beautiful soup con este html

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")

    #dame todos los img
    imgs = soup.find_all("img")
    # hacer una funcion para filtrarlos, revisando 2 niveles de parent y buscando la class a
    # si no tiene class a, entonces false
    def filter_img(img):
        if img.parent.parent.find("a") is not None:
            return True
        return False


if __name__ == '__main__':
    read_page()
