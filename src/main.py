import csv
import datetime
import os
import logging

from config.settings import BASE_URL
from models import Book
from scraper import scrape_genre_page, scrape_book_details


def main() -> None:
    books: list[Book] = []
    genre_hrefs: list[str] = [
        "arts-and-photography",
        "business-and-investing",
        "fiction-and-literature",
        "foreign-languages",
        "history-biography-and-social-science",
        "kids-and-teens",
        "learning-and-reference",
        "lifestyle-and-wellness",
        "manga-and-graphic-novels",
        "miscellaneous",
        "nature",
        "nepali",
        "political-science",
        "rare-coffee-table-books",
        "religion",
        "self-improvement-and-relationships",
        "spirituality-and-philosophy",
        "technology",
        "travel"
    ]

    prefix: str = "books/genres/"

    for genre in genre_hrefs:
        urls = scrape_genre_page(
            f"{BASE_URL}{prefix}{genre}?view_mode=all&sort_by=bestsellers")
        for book_url in urls:
            book = scrape_book_details(book_url)
            if book:
                book.genre = genre.replace("-", " ").title()
                books.append(book)

        # write to csv
        write_to_csv(
            books, f"data/books-{datetime.date.today()}.csv", mode="a")
        books.clear()
        logging.info(f"Written {len(books)} books to CSV for genre {genre}")


def write_to_csv(books: list[Book], filename: str, mode: str) -> None:
    headers = [
        "Title", "Author", "Price", "Rating", "Limited Stock", "Discount",
        "Genre", "Number of Pages", "Weight", "ISBN", "Language",
        "Related Genres", "Subgenres", "Synopsis", "URL"
    ]

    write_header = not os.path.exists(filename) or mode == "w"

    with open(filename, mode=mode, newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)

        if write_header:
            writer.writerow(headers)

        for book in books:
            writer.writerow([
                book.title,
                book.author,
                book.price,
                book.rating or "N/A",
                book.limited_stock or "N/A",
                book.discount or "N/A",
                book.genre or "N/A",
                book.number_of_pages or "N/A",
                book.weight or "N/A",
                book.isbn or "N/A",
                book.language or "N/A",
                ', '.join(book.related_genres),
                ', '.join(book.sub_genres),
                book.synopsis,
                book.url
            ])


if __name__ == "__main__":
    main()
