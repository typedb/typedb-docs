import copy
from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Optional


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


class ContributorRole(Enum):
    AUTHOR = "author"
    EDITOR = "editor"
    ILLUSTRATOR = "illustrator"
    CONTRIBUTOR = "contributor"


class Book(ABC):
    def __init__(
        self,
        isbn_13: str,
        isbn_10: Optional[str],
        title: str,
        contributors: set[tuple[Contributor, ContributorRole]],
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
        self._contributors = contributors
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
        return {contributor for contributor, role in self._contributors}

    @property
    def authors(self) -> set[Contributor]:
        return {contributor for contributor, role in self._contributors if role is ContributorRole.AUTHOR}

    @property
    def editors(self) -> set[Contributor]:
        return {contributor for contributor, role in self._contributors if role is ContributorRole.EDITOR}

    @property
    def illustrators(self) -> set[Contributor]:
        return {contributor for contributor, role in self._contributors if role is ContributorRole.ILLUSTRATOR}

    @property
    def other_contributors(self) -> set[Contributor]:
        return {contributor for contributor, role in self._contributors if role is ContributorRole.CONTRIBUTOR}


class Paperback(Book):
    def __init__(
        self,
        isbn_13: str,
        isbn_10: Optional[str],
        title: str,
        contributors: set[tuple[Contributor, ContributorRole]],
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
            contributors,
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
        contributors: set[tuple[Contributor, ContributorRole]],
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
            contributors,
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
        contributors: set[tuple[Contributor, ContributorRole]],
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
            contributors,
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
        self._discounts: dict[Book, float] = dict()

    @property
    def discounts(self) -> dict[Book, float]:
        return copy.copy(self._discounts)

    def put_discount(self, item: Book, discount: float):
        if discount == 0:
            self._discounts.pop(item, None)
        else:
            self._discounts[item] = discount


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
        self._lines: dict[Book, int] = dict()

    @property
    def items(self) -> list[tuple[Book, int]]:
        return [(book, quantity) for book, quantity in self._lines.items()]

    def add_or_remove_items(self, item: Book, quantity: int):
        self._lines.setdefault(item, 0)
        self._lines[item] += quantity

        if self._lines[item] <= 0:
            del self._lines[item]


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
