class Book:
    genre: str

    def __init__(
        self,
        title: str | None,
        author: str | None,
        price: str | None,
        rating: str | None,
        page_count: str | None,
        weight: str | None,
        isbn: str | None,
        language: str | None,
        related_genres: list[str] | list,
        url: str
    ) -> None:
        self.title = title
        self.author = author
        self.price = price
        self.rating = rating
        self.number_of_pages = page_count
        self.weight = weight
        self.isbn = isbn
        self.language = language
        self.related_genres = related_genres
        self.url = url