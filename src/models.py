class Book:
    genre: str

    def __init__(
        self,
        title: str | None,
        author: str | None,
        price: str | None,
        rating: str | None,
        limited_stock: str | None,
        discount: str | None,
        page_count: str | None,
        weight: str | None,
        isbn: str | None,
        language: str | None,
        related_genres: list[str] | list,
        sub_genres: list[str] | list,
        synopsis: str | None,
        url: str
    ) -> None:
        self.title = title
        self.author = author
        self.price = price
        self.rating = rating
        self.limited_stock = limited_stock
        self.discount = discount
        self.number_of_pages = page_count
        self.weight = weight
        self.isbn = isbn
        self.language = language
        self.related_genres = related_genres
        self.sub_genres = sub_genres
        self.synopsis = synopsis
        self.url = url

    def __str__(self) -> str:
        string = f"""Title: {self.title}\nAuthor: {self.author}\nPrice: {self.price}\nRating: {self.rating}\nLimited Stock: {self.limited_stock}\nDiscount: {self.discount}\nNo. of pages: {self.number_of_pages}\nWeight: {self.weight}\nISBN: {self.isbn}\nLanguage: {self.language}\nRelated Genres: {self.related_genres}\nSub-genres: {self.sub_genres}\nSynopsis: {self.synopsis}\nURL: {self.url}"""
        return string
