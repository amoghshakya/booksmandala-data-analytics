import csv
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

    prefix: str = "/books/genres/"

    for genre in genre_hrefs:
        urls = scrape_genre_page(f"{BASE_URL}{prefix}{genre}")
        for i, book_url in enumerate(urls):
            book = scrape_book_details(book_url)
            book.genre = genre.replace("-", " ").title()
            books.append(book)

    # write to csv
    write_to_csv(books, "data/books.csv")


def write_to_csv(books: list[Book], filename: str) -> None:
    headers = [
        "Title", "Author", "Price", "Rating", "Genre", "Number of Pages",
        "Weight", "ISBN", "Language", "Related Genres", "URL"
    ]

    with open(filename, mode="w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)

        writer.writerow(headers)
        for book in books:
            writer.writerow([
                book.title,
                book.author,
                book.price,
                book.rating,
                book.genre,
                book.number_of_pages,
                book.weight,
                book.isbn,
                book.language,
                ', '.join(book.related_genres),
                book.url
            ])


if __name__ == "__main__":
    main()
