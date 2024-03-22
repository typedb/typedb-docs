# 11 manipulating stateful objects

from typedb.driver import TypeDB, SessionType, TransactionType
from typedb.api.connection.credential import TypeDBCredential

from typing import Iterator
from typedb.api.connection.transaction import TypeDBTransaction
from typedb.api.answer.concept_map import ConceptMap
from typedb.api.concept.thing.entity import Entity
from typedb.api.concept.thing.relation import Relation
from typedb.api.concept.thing.attribute import Attribute
from typedb.api.concept.thing.thing import Thing
from typedb.api.concept.type.entity_type import EntityType
from typedb.api.concept.type.relation_type import RelationType
from typedb.api.concept.type.attribute_type import AttributeType
from typedb.api.concept.type.role_type import RoleType

# not shown

import datetime

ADDRESS = "localhost:1730"
USERNAME = "username"
DATABASE = "bookstore"

password = input("Enter password: ")
credential = TypeDBCredential(USERNAME, password, tls_enabled=True)


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


# 11.2 operating on objects

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            book_type: EntityType
            contribution_type: RelationType
            page_count_type: AttributeType

            book: Entity = book_type.create(transaction).resolve()
            contribution: Relation = contribution_type.create(transaction).resolve()
            page_count: Attribute = page_count_type.put(transaction, 200).resolve()

            transaction.commit()


def decrement_stock(transaction: TypeDBTransaction, book: Entity) -> None:
    stock_type = transaction.concepts.get_attribute_type("stock").resolve()
    stock_old = next(book.get_has(transaction, stock_type))

    if stock_old.get_value() == 0:
        raise ValueError("Already out of stock.")
    else:
        stock_new = stock_type.put(transaction, stock_old.get_value() - 1).resolve()
        book.unset_has(transaction, stock_old).resolve()
        book.set_has(transaction, stock_new).resolve()


def create_promotion(
        transaction: TypeDBTransaction,
        code_value: str,
        name_value: str,
        start_timestamp_value: datetime,
        end_timestamp_value: datetime
) -> Entity:
    promotion_type = transaction.concepts.get_entity_type("promotion").resolve()
    code_type = transaction.concepts.get_attribute_type("code").resolve()
    name_type = transaction.concepts.get_attribute_type("name").resolve()
    start_timestamp_type = transaction.concepts.get_attribute_type("start-timestamp").resolve()
    end_timestamp_type = transaction.concepts.get_attribute_type("end-timestamp").resolve()
    promotion = promotion_type.create(transaction).resolve()
    code = code_type.put(transaction, code_value).resolve()
    name = name_type.put(transaction, name_value).resolve()
    start_timestamp = start_timestamp_type.put(transaction, start_timestamp_value).resolve()
    end_timestamp = end_timestamp_type.put(transaction, end_timestamp_value).resolve()
    promotion.set_has(transaction, code).resolve()
    promotion.set_has(transaction, name).resolve()
    promotion.set_has(transaction, start_timestamp).resolve()
    promotion.set_has(transaction, end_timestamp).resolve()
    return promotion


def add_to_promotion(transaction: TypeDBTransaction, book: Entity, promotion: Entity, discount_value: float) -> None:
    inclusion_type = transaction.concepts.get_relation_type("promotion-inclusion").resolve()
    item_role = inclusion_type.get_relates(transaction, "item").resolve()
    promotion_role = inclusion_type.get_relates(transaction, "promotion").resolve()
    discount_type = transaction.concepts.get_attribute_type("discount").resolve()
    inclusion = inclusion_type.create(transaction).resolve()
    inclusion.add_player(transaction, item_role, book).resolve()
    inclusion.add_player(transaction, promotion_role, promotion).resolve()
    discount = discount_type.put(transaction, discount_value).resolve()
    inclusion.set_has(transaction, discount)


def remove_from_promotion(transaction: TypeDBTransaction, book: Entity, promotion: Entity) -> None:
    inclusion_type = transaction.concepts.get_relation_type("promotion-inclusion").resolve()
    item_role = inclusion_type.get_relates(transaction, "item").resolve()
    promotion_role = inclusion_type.get_relates(transaction, "promotion").resolve()
    inclusions = book.get_relations(transaction, item_role)

    for inclusion in inclusions:
        promotion_players = inclusion.get_players_by_role_type(transaction, promotion_role)

        for player in promotion_players:
            if player == promotion:
                inclusion.delete(transaction).resolve()
                break


def create_review(transaction: TypeDBTransaction, user: Entity, book: Entity, score_value: int) -> Entity:
    review_type = transaction.concepts.get_entity_type("review").resolve()
    action_execution_type = transaction.concepts.get_relation_type("action-execution").resolve()
    rating_type = transaction.concepts.get_relation_type("rating").resolve()
    score_type = transaction.concepts.get_attribute_type("score").resolve()
    action_role = action_execution_type.get_relates(transaction, "action").resolve()
    executor_role = action_execution_type.get_relates(transaction, "executor").resolve()
    review_role = rating_type.get_relates(transaction, "review").resolve()
    rated_role = rating_type.get_relates(transaction, "rated").resolve()
    review = review_type.create(transaction).resolve()
    action_execution = action_execution_type.create(transaction).resolve()
    action_execution.add_player(transaction, executor_role, user).resolve()
    action_execution.add_player(transaction, action_role, review).resolve()
    rating = rating_type.create(transaction).resolve()
    rating.add_player(transaction, review_role, review).resolve()
    rating.add_player(transaction, rated_role, book).resolve()
    score = score_type.put(transaction, score_value).resolve()
    review.set_has(transaction, score).resolve()
    return review
