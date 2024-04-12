from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Optional, Self


class Place(ABC):
    def __init__(self, name: str):
        self.name = name


class Country(Place):
    def __init__(self, name: str):
        super().__init__(name)


class State(Place):
    def __init__(self, name: str, location: Country):
        super().__init__(name)
        self.location = location

    @property
    def country(self) -> Country:
        return self.location


class City(Place):
    def __init__(self, name: str, location: State | Country):
        super().__init__(name)
        self.location = location

    @property
    def state(self) -> Optional[State]:
        if type(self.location) is State:
            return self.location

    @property
    def country(self) -> Country:
        match self.location:
            case State():
                return self.location.country
            case Country():
                return self.location


class Address:
    def __int__(self, street: str, city: City):
        self.street = street
        self.city = city

    @property
    def state(self) -> State:
        return self.city.state

    @property
    def country(self) -> Country:
        return self.city.country


class Company(ABC):
    def __init__(self, name: str):
        self.name = name


class Publisher(Company):
    def __init__(self, name: str):
        super().__init__(name)


class Courier(Company):
    def __init__(self, name: str):
        super().__init__(name)


class Contributor:
    def __init__(self, name: str):
        self.name = name


class Book(ABC):
    def __init__(
        self,
        isbn_13: str,
        isbn_10: Optional[str],
        title: str,
        authors: set[Contributor],
        editors: set[Contributor],
        illustrators: set[Contributor],
        other_contributors: set[Contributor],
        publisher: Publisher,
        year: int,
        location: City,
        page_count: str,
        genres: set[str],
        price: float,
    ):
        self.isbn_13 = isbn_13
        self.isbn_10 = isbn_10
        self.title = title
        self.authors = authors
        self.editors = editors
        self.illustrators = illustrators
        self.other_contributors = other_contributors
        self.publisher = publisher
        self.year = year
        self.location = location
        self.page_count = page_count
        self.genres = genres
        self.price = price

    @property
    def isbns(self) -> set[str]:
        if self.isbn_10 is None:
            return {self.isbn_13}
        else:
            return {self.isbn_13, self.isbn_10}

    @property
    def contributors(self) -> set[Contributor]:
        return self.authors | self.editors | self.illustrators | self.other_contributors


class Paperback(Book):
    def __init__(
        self,
        isbn_13: str,
        isbn_10: Optional[str],
        title: str,
        authors: set[Contributor],
        editors: set[Contributor],
        illustrators: set[Contributor],
        other_contributors: set[Contributor],
        publisher: Publisher,
        year: int,
        location: City,
        page_count: str,
        genres: set[str],
        price: float,
        stock: int,
    ):
        super().__init__(
            isbn_13,
            isbn_10,
            title,
            authors,
            editors,
            illustrators,
            other_contributors,
            publisher,
            year,
            location,
            page_count,
            genres,
            price,
        )

        self.stock = stock


class Hardback(Book):
    def __init__(
        self,
        isbn_13: str,
        isbn_10: Optional[str],
        title: str,
        authors: set[Contributor],
        editors: set[Contributor],
        illustrators: set[Contributor],
        other_contributors: set[Contributor],
        publisher: Publisher,
        year: int,
        location: City,
        page_count: str,
        genres: set[str],
        price: float,
        stock: int,
    ):
        super().__init__(
            isbn_13,
            isbn_10,
            title,
            authors,
            editors,
            illustrators,
            other_contributors,
            publisher,
            year,
            location,
            page_count,
            genres,
            price,
        )

        self.stock = stock


class Ebook(Book):
    def __init__(
        self,
        isbn_13: str,
        isbn_10: Optional[str],
        title: str,
        authors: set[Contributor],
        editors: set[Contributor],
        illustrators: set[Contributor],
        other_contributors: set[Contributor],
        publisher: Publisher,
        year: int,
        location: City,
        page_count: str,
        genres: set[str],
        price: float,
    ):
        super().__init__(
            isbn_13,
            isbn_10,
            title,
            authors,
            editors,
            illustrators,
            other_contributors,
            publisher,
            year,
            location,
            page_count,
            genres,
            price,
        )


class Promotion:
    def __init__(self, code: str, name: str, start_timestamp: datetime, end_timestamp: datetime):
        self.code = code
        self.name = name
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self._inclusions: dict[Book, float] = dict()

    @property
    def inclusions(self) -> list[tuple[Book, float]]:
        return [(book, discount) for book, discount in self._inclusions.items()]

    def add_or_update_book(self, book: Book, discount: float):
        if discount == 0:
            self._inclusions.pop(book, None)
        else:
            self._inclusions[book] = discount


class User:
    def __init__(self, id: str, name: str, birth_date: datetime, location: City):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.location = location


class Status(Enum):
    PENDING = "pending"
    PAID = "paid"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    RETURNED = "returned"
    CANCELED = "canceled"


class UserAction(ABC):
    def __init__(self, user: User, timestamp: datetime):
        self.user = user
        self.timestamp = timestamp


class Order(UserAction):
    def __init__(self, id: str, user: User, timestamp: datetime):
        super().__init__(user, timestamp)
        self.id = id
        self.status = Status.PENDING
        self._order_lines: dict[Book, int] = dict()

    @property
    def order_lines(self) -> list[tuple[Book, int]]:
        return [(book, quantity) for book, quantity in self._order_lines.items()]

    def add_or_remove_book(self, book: Book, quantity: int):
        self._order_lines.setdefault(book, 0)
        self._order_lines[book] += quantity

        if self._order_lines[book] <= 0:
            del self._order_lines[book]


class Review(UserAction):
    def __init__(self, id: str, reviewed: Book, user: User, timestamp: datetime, score: int):
        super().__init__(user, timestamp)
        self.id = id
        self.reviewed = reviewed
        self.score = score


class Login(UserAction):
    def __init__(self, user: User, timestamp: datetime, success: bool):
        super().__init__(user, timestamp)
        self.success = success


class Delivery:
    def __init__(self, delivered: Order, deliverer: Courier, destination: Address):
        self.delivered = delivered
        self.deliverer = deliverer
        self.destination = destination


class Recommendation:
    def __init__(self, recommended: Book, recipient: User):
        self.recommended = recommended
        self.recipient = recipient
