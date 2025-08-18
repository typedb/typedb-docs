# 6.1 driver setup

from typing import Iterator
from typedb.driver import TypeDB, TransactionType, Credentials, DriverOptions
from typedb.api.user.user import User
from typedb.api.connection.database import Database

# 6.2 managing users and databases

ADDRESS = "localhost:1729"
USERNAME = "admin"
PASSWORD = "password"
credentials = Credentials(USERNAME, PASSWORD)
options = DriverOptions(is_tls_enabled=False, tls_root_ca_path=None)

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    pass

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    # Creates a new user with the specified username and password.
    driver.users.create("username", "password")

    # Checks if a user with the specified username exists.
    user_exists: bool = driver.users.contains("username")

    # Retrieves a user object by specified username.
    specific_user: User = driver.users.get("username")

    # Retrieves a list of user objects for every user.
    all_users: list[User] = driver.users.all()

    # Deletes a user with the specified username.
    driver.users.delete("username")

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    # Retrieves a user object corresponding to the current user,
    # according to the credentials provided to the driver object.
    current_user: User = driver.user()

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    user: User

    # Retrieves the username of a given user.
    username: str = user.username()
    # Updates the password of a given user.
    user.password_update("old-password", "new-password")


def create_new_user(driver: TypeDBDriver, username: str, password: str) -> None:
    if driver.users.contains(username):
        raise ValueError(f"User already exists with username: {username}")
    else:
        driver.users.create(username, password)


def update_current_user_password(driver: TypeDBDriver, password_old: str, password_new: str) -> None:
    current_user = driver.user()
    current_user.password_update(password_old, password_new)


def print_usernames(driver: TypeDBDriver) -> None:
    for user in driver.users.all():
        print(user.username())


with TypeDB.driver(ADDRESS, credentials, options) as driver:
    # Creates a new database with the specified name.
    driver.databases.create("database-name")

    # Checks if a database with the specified name exists.
    database_exists: bool = driver.databases.contains("database-name")

    # Retrieves a database object by specified name.
    specific_database: Database = driver.databases.get("database-name")

    # Retrieves a list of database objects for every database.
    all_databases: list[Database] = driver.databases.all()

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    database: Database

    # Retrieves the name of a given database.
    name: str = database.name

    # Retrieves the schema of a given database.
    schema: str = database.schema()

    # Deletes a given database.
    database.delete()


def force_create_database(driver: TypeDBDriver, database_name: str) -> None:
    if driver.databases.contains(database_name):
        driver.databases.get(database_name).delete()

    driver.databases.create(database_name)


def print_database_details(driver: TypeDBDriver) -> None:
    for database in driver.databases.all():
        print(database.name)
        print(database.schema())


# 6.3 transactions

DB = "database-name"

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.READ) as tx:
        pass

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.WRITE) as tx:
        # write queries
        tx.commit()

# 6.4 executing queries

DATABASE = "bookstore"

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.READ) as tx:
        docs = tx.query(
            """
            match $book isa book;
            fetch { "title": $book.title, "page-count": $book.page-count };
            """
        ).resolve().as_concept_documents()
        for doc in docs:
            print(doc)

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.READ) as tx:
        promise = tx.query(
            """
            match $book isa book;
            fetch { "title": $book.title, "page-count": $book.page-count };
            """
        )
        documents = promise.resolve().as_concept_documents()
        for doc in documents:
            print(doc)

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.WRITE) as tx:
        tx.query(
            """
            insert $new_user isa user,
                   has id "u0014",
                   has name "Jaiden Hurst",
                   has birth-date 1950-03-03;
            """
        ).resolve()
        tx.commit()

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.WRITE) as tx:
        tx.query(
            """
            match $retracted_review isa review, has id "r0001";
                  $relation ($retracted_review) isa relation;
            delete $relation;
            """
        ).resolve()
        tx.query(
            """
            match $retracted_review isa review, has id "r0001";
            delete $retracted_review;
            """
        ).resolve()
        tx.commit()

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.WRITE) as tx:
        tx.query(
            """
            match $dispatched_order isa order, has id "o0008";
                  $paid = "paid";
            update delete $dispatched_order has status $paid; insert $dispatched_order has status "dispatched";
            """
        ).resolve()
        tx.commit()


def create_user(tx, id: str, name: str, birth_date: str) -> None:
    tx.query(
        f"""
        insert $new_user isa user,
               has id "{id}",
               has name "{name}",
               has birth-date {birth_date};
        """
    ).resolve()


def delete_review(tx, id: str) -> None:
    tx.query(
        f"""
        match $retracted_review isa review, has id "{id}";
              $relation ($retracted_review) isa relation;
        delete $relation;
        """
    ).resolve()
    tx.query(
        f"""
        match $retracted_review isa review, has id "{id}";
        delete $retracted_review;
        """
    ).resolve()


def update_order_status(tx, id: str, status_old: str, status_new: str) -> None:
    tx.query(
        f"""
        match $order isa order, has id "{id}";
              $old = "{status_old}";
        update delete $order has status $old; insert $order has status "{status_new}";
        """
    ).resolve()


DB = "social-network"

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    try:
        driver.databases.create(DB)
    except Exception:
        pass
    with driver.transaction(DB, TransactionType.SCHEMA) as tx:
        tx.query(
            """
            define
            entity person,
                owns first-name,
                owns last-name,
                owns birth-date,
                plays friendship:friend,
                plays relationship:partner,
                plays marriage:spouse;
            relation friendship,
                relates friend;
            relation relationship,
                relates partner;
            relation marriage sub relationship,
                relates spouse as partner;
            attribute name @abstract, value string;
            attribute first-name sub name;
            attribute last-name sub name;
            attribute birth-date, value datetime;
            """
        ).resolve()
        tx.commit()

# 6.5 processing results

DB = "bookstore"

with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.READ) as tx:
        docs = tx.query(
            """
            match $book isa hardback;
            fetch { "title": $book.title, "genre": [$book.genre], "page-count": $book.page-count };
            """
        ).resolve().as_concept_documents()
        for doc in docs:
            print(doc)
            print(doc.keys())
            print(list(doc.keys()))


def print_hardback_isbns(tx) -> None:
    docs = tx.query(
        """
        match $book isa hardback;
        fetch { "title": $book.title, "isbn": [$book.isbn-13, $book.isbn-10] };
        """
    ).resolve().as_concept_documents()
    for doc in docs:
        print(f"Title: {doc['title']}")
        for v in doc["isbn"]:
            print(v)
        print()


def get_orders_of_book(tx, isbn: str) -> Iterator[tuple[str, int]]:
    docs = tx.query(
        f"""
        match $book isa book, has isbn \"{isbn}\";
              $line (order: $order, item: $book) isa order-line;
        fetch {{ "order": $order.id, "quantity": $line.quantity }};
        """
    ).resolve().as_concept_documents()
    for doc in docs:
        yield doc["order"], doc["quantity"]


with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.READ) as tx:
        for order in get_orders_of_book(tx, "9780446310789"):
            print(order)


def get_books_in_genre(tx, genre: str) -> Iterator[tuple[str, str]]:
    docs = tx.query(
        f"""
        match $book isa book, has genre \"{genre}\";
        fetch {{ "isbn-13": $book.isbn-13, "title": $book.title }};
        """
    ).resolve().as_concept_documents()
    for doc in docs:
        yield doc["isbn-13"], doc["title"]


with TypeDB.driver(ADDRESS, credentials, options) as driver:
    with driver.transaction(DB, TransactionType.READ) as tx:
        for book in get_books_in_genre(tx, "science fiction"):
            print(book)
