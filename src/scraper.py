"""
requires `chromedriver` if you're using Google Chrome

Download from [here](https://googlechromelabs.github.io/chrome-for-testing/).

Choose the version that matches with your browser version then add to PATH

```
import os
os.environ["PATH"] += r"/path/to/chromedriver"
```

OR manually add to your system PATH
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

import logging

from config.settings import WAIT_TIME
from models import Book

# Configuring logging
logging.basicConfig(
    filename="logs/scrape.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

opts = webdriver.ChromeOptions()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver=driver, timeout=WAIT_TIME)


def scrape_genre_page(url: str) -> list[str]:
    logging.info(f"Starting {scrape_genre_page.__name__}")
    urls: list[str] = []
    driver.get(url)
    logging.info(f"Navigating to {url}")

    # wait for all elements to load
    articles = wait.until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "book-card")))

    for article in articles:
        anchor = article.find_element(By.TAG_NAME, "a")
        logging.info(f"Found anchor element {anchor}")
        book_url = anchor.get_attribute("href")

        if book_url is not None:
            urls.append(book_url)

    logging.info(f"Finished {scrape_genre_page.__name__}")
    return urls


def scrape_book_details(book_url: str) -> Book:
    driver.get(book_url)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h1")))

    # Get elements
    title = driver.find_element(
        By.CSS_SELECTOR, ".book-content__header__title")  # h1
    author = driver.find_element(
        By.CSS_SELECTOR, ".book-content__header__author > a")
    price = driver.find_element(
        By.CSS_SELECTOR, ".book-aside__cart__price")  # div
    rating = driver.find_element(
        By.CSS_SELECTOR, ".book-content__header__stats__rating")  # div

    other_info = driver.find_elements(
        By.CSS_SELECTOR, ".book-content__other-info__card__wrapper")  # divs
    related_genres = driver.find_elements(
        By.CSS_SELECTOR, "span.genres-wrap__genres__genre__name.genres-wrap__genres__main")

    # Extract Info
    title_text = title.get_attribute("innerText")
    author_text = author.get_attribute("innerText")
    price_text = price.get_attribute("innerText")
    rating_text = rating.get_attribute("innerText")
    other_info_dict = {
        div.find_element(
            By.CLASS_NAME,
            "book-content__other-info__card__title"
        ).get_attribute("innerText"): div.find_element(
            By.CLASS_NAME,
            "book-content__other-info__card__value"
        ).get_attribute("innerText")
        for div in other_info
    }
    related_genres_list = [span.get_attribute(
        "innerText") for span in related_genres]

    return Book(
        title=title_text,
        author=author_text,
        price=price_text,
        rating=rating_text,
        page_count=other_info_dict["Page Count"],
        weight=other_info_dict["Weight"],
        isbn=other_info_dict["ISBN"],
        language=other_info_dict["Language"],
        related_genres=related_genres_list,
        url=book_url
    )
