import datetime

# 10 manipulating stateful objects

from typedb.driver import TypeDB, SessionType, TransactionType
from typedb.api.connection.credential import TypeDBCredential

from typing import Iterator
from typedb.api.answer.concept_map import ConceptMap
from typedb.api.concept.thing.entity import Entity
from typedb.api.concept.thing.relation import Relation
from typedb.api.connection.transaction import TypeDBTransaction

# 10.1 retrieving objects

ADDRESS = "localhost:1730"
USERNAME = "username"
DATABASE = "bookstore"

password = input("Enter password: ")
credential = TypeDBCredential(USERNAME, password, tls_enabled=True)

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            results: Iterator[ConceptMap] = transaction.query.get("""
                match
                $user isa user;
                $execution ($user, $action) isa action-execution;
                get;
            """)

            for result in results:
                user: Entity = result.get("user").as_entity()
                action: Entity = result.get("action").as_entity()
                execution: Relation = result.get("execution").as_relation()


def get_books_in_genre(transaction: TypeDBTransaction, genre: str) -> Iterator[Entity]:
    results = transaction.query.get(f"""
        match
        $book isa book, has genre "{genre}";
        get;
    """)

    for result in results:
        book = result.get("book").as_entity()

        yield book


def get_orders_with_multiple_copies(transaction: TypeDBTransaction) -> Iterator[Entity]:
    results = transaction.query.get("""
        match
        $order isa order;
        $book isa book;
        ($order, $book) isa order-line, has quantity > 1;
        get;
    """)

    for result in results:
        order = result.get("order").as_entity()

        yield order


def get_discounted_books(transaction: TypeDBTransaction) -> Iterator[Entity]:
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

    results = transaction.query.get(f"""
        match
        $book isa book;
        $promotion isa promotion,
            has start-timestamp <= {current_timestamp},
            has end-timestamp >= {current_timestamp};
        ($book, $promotion) isa promotion-inclusion;
        get $book;
    """)

    for result in results:
        book = result.get("book").as_entity()

        yield book
