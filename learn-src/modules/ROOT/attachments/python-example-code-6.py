# 6.1 driver setup

from typedb.driver import TypeDB, SessionType, TransactionType
from typedb.api.connection.credential import TypeDBCredential

from typing import Iterator
from typedb.api.connection.driver import TypeDBDriver
from typedb.api.connection.transaction import TypeDBTransaction
from typedb.api.user.user import User
from typedb.api.connection.database import Database

# 6.2 managing users and databases

ADDRESS = "localhost:1730"
USERNAME = "username"

password = input("Enter password: ")
credential = TypeDBCredential(USERNAME, password, tls_enabled=True)

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    # code goes here
    pass

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
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

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    # Retrieves a user object corresponding to the current user,
    # according to the credentials provided to the driver object.
    current_user: User = driver.user()

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
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


with TypeDB.cloud_driver(ADDRESS, credential) as driver:
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


# 6.3 sessions and transactions

DATABASE = "database-name"

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        # code goes here
        pass

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            # code goes here
            pass

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            # code goes here

            transaction.commit()

# 6.4 executing queries

DATABASE = "bookstore"

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            results: Iterator[dict] = transaction.query.fetch("""
                match
                $book isa book;
                fetch
                $book: title, page-count;
            """)

            for result in results:
                print(result)

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            results: list[dict] = list(transaction.query.fetch("""
                match
                $book isa book;
                fetch
                $book: title, page-count;
            """))

for result in results:
    print(result)

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            transaction.query.insert("""
                insert
                $new-user isa user,
                    has id "u0014",
                    has name "Jaiden Hurst",
                    has birth-date 1950-03-03;
            """)

            transaction.commit()

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            transaction.query.delete("""
                match
                $retracted-review isa review, has id "r0001";
                $relation ($retracted-review) isa relation;
                delete
                $relation isa relation;
            """)

            transaction.query.delete("""
                match
                $retracted-review isa review, has id "r0001";
                delete
                $retracted-review isa review;
            """)

            transaction.commit()

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            transaction.query.update("""
                match
                $dispatched-order isa order, has id "o0008";
                $paid "paid" isa status;
                delete
                $dispatched-order has $paid;
                insert
                $dispatched-order has status "dispatched";
            """)

            transaction.commit()


def create_user(transaction: TypeDBTransaction, id: str, name: str, birth_date: str) -> None:
    transaction.query.insert(f"""
        insert
        $new-user isa user,
            has id "{id}",
            has name "{name}",
            has birth-date {birth_date};
    """)


def delete_review(transaction: TypeDBTransaction, id: str) -> None:
    transaction.query.delete(f"""
        match
        $retracted-review isa review, has id "{id}";
        $relation ($retracted-review) isa relation;
        delete
        $relation isa relation;
    """)

    transaction.query.delete(f"""
        match
        $retracted-review isa review, has id "{id}";
        delete
        $retracted-review isa review;
    """)


def update_order_status(transaction: TypeDBTransaction, id: str, status_old: str, status_new: str) -> None:
    transaction.query.update(f"""
        match
        $dispatched-order isa order, has id "{id}";
        $status-old "{status_old}" isa status;
        delete
        $dispatched-order has $status-old;
        insert
        $dispatched-order has status "{status_new}";
    """)


DATABASE = "social-network"

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    driver.databases.create(DATABASE)

    with driver.session(DATABASE, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            transaction.query.define("""
                define
                person sub entity,
                    owns first-name,
                    owns last-name,
                    owns birth-date,
                    plays friendship:friend,
                    plays relationship:partner,
                    plays marriage:spouse;
                friendship sub relation,
                    relates friend;
                relationship sub relation,
                    relates partner;
                marriage sub relationship,
                    relates spouse as partner;
                name sub attribute, abstract, value string;
                first-name sub name;
                last-name sub name;
                birth-date sub attribute, value datetime;
            """)

            transaction.commit()

# 6.5 processing results

DATABASE = "bookstore"

with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            results: Iterator[dict] = transaction.query.fetch("""
                match
                $book isa hardback;
                fetch
                $book: title, genre, page-count;
            """)

            for result in results:
                print(result)

                print(result.keys())

                print(result["book"].keys())

                for title in result["book"]["title"]:
                    print(f"""Title: {title["value"]}""")

                for genre in result["book"]["genre"]:
                    print(f"""Genre: {genre["value"]}""")

                for page_count in result["book"]["page-count"]:
                    print(f"""Page count: {page_count["value"]}""")

                print()


def print_hardback_isbns(transaction: TypeDBTransaction) -> None:
    results = transaction.query.fetch("""
        match
        $book isa hardback;
        fetch
        $book: title, isbn;
    """)

    for result in results:
        for title in result["book"]["title"]:
            print(f"""Title: {title["value"]}""")

        for isbn in result["book"]["isbn"]:
            print(f"""{isbn["type"]["label"].upper()}: {isbn["value"]}""")

        print()


def get_orders_of_book(transaction: TypeDBTransaction, isbn: str) -> Iterator[tuple[str, int]]:
    results = transaction.query.fetch(f"""
        match
        $book isa book, has isbn "{isbn}";
        $line (order: $order, item: $book) isa order-line;
        fetch
        $order: id;
        $line: quantity;
    """)

    for result in results:
        order_id = result["order"]["id"][0]["value"]
        quantity = result["line"]["quantity"][0]["value"]

        yield order_id, quantity


with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            orders = get_orders_of_book(transaction, "9780446310789")

            for order in orders:
                print(order)


def get_books_in_genre(transaction: TypeDBTransaction, genre: str) -> Iterator[tuple[str, str]]:
    results = transaction.query.fetch(f"""
        match
        $book isa book, has genre "{genre}";
        fetch
        $book: isbn-13, title;
    """)

    for result in results:
        isbn_13 = result["book"]["isbn-13"][0]["value"]
        title = result["book"]["title"][0]["value"]

        yield isbn_13, title


with TypeDB.cloud_driver(ADDRESS, credential) as driver:
    with driver.session(DATABASE, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            scifis = get_books_in_genre(transaction, "science fiction")

            for book in scifis:
                print(book)
