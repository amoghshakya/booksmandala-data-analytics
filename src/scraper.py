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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
actions = ActionChains(driver)


def scrape_genre_page(url: str) -> set[str]:
    logging.info(f"Starting {scrape_genre_page.__name__}")
    urls: set[str] = set()
    driver.get(url)
    logging.info(f"Navigating to {url}")

    for _ in range(5):
        try:
            # wait for and locate the 'Load More' button
            next_button = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button.btn.load-more__btn.false")))
            next_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btn.load-more__btn.false")))

            # wait for all book cards to load
            articles = wait.until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "book-card")))

            for article in articles:
                anchor = article.find_element(By.TAG_NAME, "a")
                logging.info(f"Found anchor element {anchor}")
                book_url = anchor.get_attribute("href")

                if book_url is not None:
                    urls.add(book_url)

            if next_button:
                # click
                driver.execute_script("arguments[0].click();", next_button)
                logging.info("Clicked the 'Load More' button.")
            else:
                logging.info("No more pages to load")
                break

        except Exception as e:
            print(e)
            continue

    logging.info(f"Found {len(urls)} books")
    logging.info(f"Finished {scrape_genre_page.__name__}")
    return urls


def scrape_book_details(book_url: str) -> Book | None:
    logging.info(f"Starting {scrape_book_details.__name__} on {book_url}")
    driver.get(book_url)
    try:
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "h1")))
    except TimeoutException:
        logging.error(f"Timeout while waiting for page: {book_url}")
        return None

    # Get elements
    title = driver.find_element(
        By.CSS_SELECTOR, ".book-content__header__title").text  # h1
    try:
        author = driver.find_element(
            By.CSS_SELECTOR, ".book-content__header__author > a").text
    except NoSuchElementException:
        logging.warning(f"Author not found for {book_url}")
        author = "Unknown"

    price = driver.find_element(
        By.CSS_SELECTOR, ".book-aside__cart__price").get_attribute("innerText")  # div
    rating = driver.find_element(
        By.CSS_SELECTOR, ".book-content__header__stats__rating").get_attribute("innerText")  # div
    synopsis = driver.find_element(
        By.ID, "sypnosis-content").text or None

    other_info = driver.find_elements(
        By.CSS_SELECTOR, ".book-content__other-info__card__wrapper")  # divs
    related_genres = driver.find_elements(
        By.CSS_SELECTOR, "span.genres-wrap__genres__genre__name.genres-wrap__genres__main")

    try:
        limited_stock = driver.find_element(
            By.CSS_SELECTOR, ".book-content__header__stock.head-stock").get_attribute("innerText")
    except NoSuchElementException:
        limited_stock = None

    try:
        discount_value = driver.find_element(
            By.CSS_SELECTOR, ".book-aside__cart__price__discount").text
    except NoSuchElementException:
        discount_value = None

    # Extract Info
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

    logging.info(
        f"Extracted {title}, {author}, \
            {price}, {rating}, ... and more metadata!")

    logging.info(f"Finished {scrape_book_details.__name__}")
    return Book(
        title=title,
        author=author,
        price=price,
        rating=rating,
        limited_stock=limited_stock,
        discount=discount_value,
        page_count=other_info_dict.get("Page Count", "N/A"),
        weight=other_info_dict.get("Weight", "N/A"),
        isbn=other_info_dict.get("ISBN", "N/A"),
        language=other_info_dict.get("Language", "N/A"),
        related_genres=related_genres_list,
        synopsis=synopsis,
        url=book_url
    )
