#
# Copyright (C) 2024 Vaticle
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from enum import Enum
from typing import Iterator, Optional, Any
from typedb.api.connection.session import TypeDBSession
from typedb.api.connection.transaction import TypeDBTransaction
from typedb.driver import TypeDB, SessionType, TransactionType

ADDRESS = "localhost:1730"
DATABASE = "bookstore"


class BookFormat(Enum):
    PAPERBACK = "paperback"
    HARDBACK = "hardback"
    EBOOK = "ebook"


class BookNotFoundException(Exception):
    pass


def filter_books(
    transaction: TypeDBTransaction,
    format: Optional[BookFormat],
    genres: Optional[list[str]],
    contributor_names: Optional[list[str]],
    publisher_name: Optional[str],
    publication_year: Optional[int],
) -> Iterator[str]:
    if format is None:
        query = f"""match $book isa book;"""
    else:
        query = f"""match $book isa {format.value};"""

    if genres is not None:
        for genre in genres:
            query += f""" $book has genre "{genre}";"""

    if contributor_names is not None:
        for i, name in enumerate(contributor_names):
            query += f""" $contributor-{i} isa contributor, has name "{name}"; ($book, $contributor-{i}) isa contribution;"""

    if publisher_name is not None:
        query += f""" $publisher isa publisher, has name "{publisher_name}"; ($book, $publisher) isa publishing;"""

    if publication_year is not None:
        query += f""" $publication isa publication, has year {publication_year}; ($book, $publication) isa publishing;"""

    query += f""" fetch $book: isbn-13;"""

    for result in transaction.query.fetch(query):
        yield result["book"]["isbn-13"][0]["value"]


def get_book_details(transaction: TypeDBTransaction, isbn: str) -> list[tuple[str, Any]]:
    book_query = f"""
        match
        $book isa! $book-type, has isbn "{isbn}";
        fetch
        $book-type;
        $book: attribute;
    """

    try:
        result = next(transaction.query.fetch(book_query))
    except StopIteration:
        raise BookNotFoundException()

    details = list()

    details.append(("format", result["book-type"]["label"]))

    for attribute in result["book"]["attribute"]:
        details.append((attribute["type"]["label"], attribute["value"]))

    contributing_query = f"""
        match
        $book isa book, has isbn "{isbn}";
        $contributor isa contributor;
        ($book, $contributor-role: $contributor) isa! $contribution-type;
        $contribution-type relates $contributor-role;
        fetch
        $contributor: name;
        $contributor-role;
    """

    for result in transaction.query.fetch(contributing_query):
        contributor_name = result["contributor"]["name"][0]["value"]
        contributor_role = result["contributor-role"]["label"].split(":")[1]
        details.append((contributor_role, contributor_name))

    publishing_query = f"""
        match
        $book isa book, has isbn "{isbn}";
        $publisher isa publisher;
        $publication isa publication;
        ($book, $publisher, $publication) isa publishing;
        fetch
        $publisher: name;
        $publication: year;
    """

    result = next(transaction.query.fetch(publishing_query))
    publisher_name = result["publisher"]["name"][0]["value"]
    details.append(("publisher", publisher_name))
    publication_year = result["publication"]["year"][0]["value"]
    details.append(("year", publication_year))

    return details


def format_book_details(details: list[tuple[str, Any]]) -> str:
    output = ""

    for detail in details:
        field_name = detail[0].replace("-", " ").title().replace("Isbn ", "ISBN-")
        field_value = detail[1]
        output += f"""\n{field_name}: {field_value}"""

    return output


def retrieve_book(session: TypeDBSession) -> None:
    isbn = input("""Enter ISBN-13 or ISBN-10: """).strip()

    with session.transaction(TransactionType.READ) as transaction:
        try:
            details = get_book_details(transaction, isbn)
            print(format_book_details(details))
        except BookNotFoundException:
            print(f"""No book found with ISBN: "{isbn}" """)


def search_books(session: TypeDBSession) -> None:
    print("""Available filters:""")
    print(""" - Format.""")
    print(""" - Genres.""")
    print(""" - Contributor names.""")
    print(""" - Publisher name.""")
    print(""" - Publication year.""")

    if input("""Filter on format? (Y/N): """).strip().upper() == "Y":
        try:
            format_ = BookFormat(input("""Enter format: """).strip())
        except ValueError:
            print("""Not a valid book format.""")
            return
    else:
        format_ = None

    if input("""Filter on genres? (Y/N): """).strip().upper() == "Y":
        genres = list()

        while True:
            genres.append(input("""Enter genre: """).strip())

            if input("""Filter on another genre? (Y/N): """).strip().upper() != "Y":
                break
    else:
        genres = None

    if input("""Filter on contributors? (Y/N): """).strip().upper() == "Y":
        contributor_names = list()

        while True:
            contributor_names.append(input("""Enter contributor name: """).strip())

            if input("""Filter on another contributor? (Y/N): """).strip().upper() != "Y":
                break
    else:
        contributor_names = None

    if input("""Filter on publisher? (Y/N): """).strip().upper() == "Y":
        publisher_name = input("""Enter publisher name: """)
    else:
        publisher_name = None

    if input("""Filter on publication year? (Y/N): """).strip().upper() == "Y":
        publication_year = input("""Enter year: """)
    else:
        publication_year = None

    with session.transaction(TransactionType.READ) as transaction:
        isbns = filter_books(transaction, format_, genres, contributor_names, publisher_name, publication_year)
        book_found = False

        for isbn in isbns:
            try:
                details = get_book_details(transaction, isbn)
                print(format_book_details(details))
                book_found = True
            except BookNotFoundException:
                pass

        if not book_found:
            print("""\nNo results found.""")


if __name__ == "__main__":
    with TypeDB.core_driver(ADDRESS) as driver:
        with driver.session(DATABASE, SessionType.DATA) as session:
            while True:
                print("""Available commands:""")
                print(""" - R: Retrieve book details by ISBN.""")
                print(""" - S: Search for books.""")
                print(""" - Q: Quit.""")

                command = input("""Enter command: """).strip().upper()

                if command == "R":
                    retrieve_book(session)
                elif command == "S":
                    search_books(session)
                elif command == "Q":
                    break
                else:
                    print(f"""Unrecognised command: "{command}" """)

                print()
