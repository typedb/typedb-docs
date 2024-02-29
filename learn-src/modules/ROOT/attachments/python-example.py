from typedb.api.connection.driver import TypeDBDriver
from typedb.api.connection.database import Database
from typedb.api.user.user import User

DATABASE = "bookstore"

# 6.1 managing users and databases

from typedb.driver import TypeDB
from typedb.api.connection.credential import TypeDBCredential

ADDRESS = "localhost:1730"
USERNAME = "username"

password = input("Enter password: ")
credential = TypeDBCredential(USERNAME, password, tls_enabled=True)

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


# 6.2 sessions and transactions

# 6.3 executing queries

# 6.4 processing results
