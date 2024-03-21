import datetime
from typedb.api.concept.type.role_type import RoleType
from typedb.api.connection.credential import TypeDBCredential

ADDRESS = "localhost:1730"
USERNAME = "username"
DATABASE = "bookstore"

password = input("Enter password: ")
credential = TypeDBCredential(USERNAME, password, tls_enabled=True)

# 11 manipulating stateful objects

from typedb.driver import TypeDB, SessionType, TransactionType

from typing import Iterator
from typedb.api.connection.transaction import TypeDBTransaction
from typedb.api.answer.concept_map import ConceptMap
from typedb.api.concept.thing.entity import Entity
from typedb.api.concept.thing.relation import Relation
from typedb.api.concept.thing.attribute import Attribute
from typedb.api.concept.type.entity_type import EntityType
from typedb.api.concept.type.relation_type import RelationType
from typedb.api.concept.type.attribute_type import AttributeType
from typedb.api.concept.thing.thing import Thing

# 11.1 retrieving objects

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            results: Iterator[ConceptMap] = transaction.query.get("""
                match
                $user isa user;
                $execution ($user, $action) isa action-execution,
                    has timestamp $timestamp;
                $action isa $action-type;
                get;
            """)

            for result in results:
                user: Entity = result.get("user").as_entity()
                action: Entity = result.get("action").as_entity()
                execution: Relation = result.get("execution").as_relation()
                timestamp: Attribute = result.get("timestamp").as_attribute()
                action_type: EntityType = result.get("action-type").as_entity_type()


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


with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            book_type: EntityType = transaction.concepts.get_entity_type("book").resolve()
            contribution_type: RelationType = transaction.concepts.get_relation_type("contribution").resolve()
            page_count_type: AttributeType = transaction.concepts.get_attribute_type("page-count").resolve()


with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            book_type: EntityType
            contribution_type: RelationType
            page_count_type: AttributeType

            books: Iterator[Entity] = book_type.get_instances(transaction)
            contributions: Iterator[Relation] = contribution_type.get_instances(transaction)
            page_counts: Iterator[Attribute] = page_count_type.get_instances(transaction)


def get_users(transaction: TypeDBTransaction) -> Iterator[Entity]:
    results = transaction.query.get("""
        match
        $user isa user;
        get;
    """)

    for result in results:
        user = result.get("user").as_entity()

        yield user


def get_users(transaction: TypeDBTransaction) -> Iterator[Entity]:
    user_type = transaction.concepts.get_entity_type("user").resolve()
    users = user_type.get_instances(transaction)
    return users


with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            book: Entity
            attributes: Iterator[Attribute] = book.get_has(transaction)
            relations: Iterator[Relation] = book.get_relations(transaction)


def cast_thing(thing: Thing) -> Entity | Relation:
    if thing.is_entity():
        return thing.as_entity()
    if thing.is_relation():
        return thing.as_relation()


with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            book: Entity
            work_role: RoleType
            contributions = book.get_relations(transaction, work_role)


def get_related_entities(transaction: TypeDBTransaction, entity: Entity) -> Iterator[Entity]:
    for relation in entity.get_relations(transaction):
        for player in relation.get_players_by_role_type(transaction):
            if not player.is_entity():
                continue
            elif player == entity:
                continue
            else:
                yield player.as_entity()

