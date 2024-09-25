import sys
from pprint import pprint

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

cache_html = False
cache_folder = "cache_html/"
driver: webdriver.Chrome = None  # Instancia global del driver

min_wait_time = 1.5
scroll_steps = 6


def url_to_cache_filename(url):
    return url.replace("/", "_").replace(":", "_").replace("?", "_").replace("=", "_") + ".html"


def get_cache_for_url(url):
    file_name = url_to_cache_filename(url)
    with open(cache_folder + file_name, "r", encoding="utf-8") as f:
        return f.read()


def save_cache_for_url(url, content):
    file_name = url_to_cache_filename(url)
    with open(cache_folder + file_name, "w+", encoding="utf-8") as f:
        f.write(content)


def has_cache_for_url(url):
    file_name = url_to_cache_filename(url)
    try:
        with open(cache_folder + file_name, "r"):
            return True
    except FileNotFoundError:
        return False


def initialize_driver(size=(1920, 2160)):
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size= " + str(size[0]) + "," + str(size[1]))
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)


def config_selenium_speed(wait_time_, scrolls):
    global min_wait_time, scroll_steps
    min_wait_time = wait_time_
    scroll_steps = scrolls


def fetch_dynamic_html(url):
    global driver, min_wait_time, scroll_steps
    initialize_driver()

    driver.get(url)

    time.sleep(min_wait_time + 1)

    # if url contains "coope" take another sleep of 1 seconds
    if "coope" in url:
        time.sleep(1)

    for i in range(scroll_steps):
        driver.execute_script(f"window.scrollTo(0, {i * 160})")
        time.sleep(.2)

    html = driver.page_source
    return html


def close_driver():
    global driver
    if driver is not None:
        driver.quit()
        driver = None
