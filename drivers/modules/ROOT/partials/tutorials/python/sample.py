# tag::code[]
# tag::import[]
from typedb.driver import TypeDB, TransactionType, Credentials, DriverOptions
# end::import[]


# tag::constants[]
DB_NAME = "sample_app_db"
SERVER_ADDR = "127.0.0.1:1729"

USERNAME = "admin"
PASSWORD = "password"
# end::constants[]


# tag::create_new_db[]
def create_database(driver, db_name) -> bool:
    print("Creating a new database", end="...")
    driver.databases.create(db_name)
    print("OK")
    db_schema_setup(driver, db_name)
    db_dataset_setup(driver, db_name)
    return True
# end::create_new_db[]


# tag::replace_db[]
def replace_database(driver, db_name) -> bool:
    print("Deleting an existing database", end="...")
    driver.databases.get(db_name).delete()  # Delete the database if it exists already
    print("OK")
    if create_database(driver, db_name):
        return True
    else:
        print("Failed to create a new database. Terminating...")
        return False
# end::replace_db[]


# tag::db-schema-setup[]
def db_schema_setup(driver, db_name, schema_file='schema.tql'):
    with open(schema_file, 'r') as data:
        define_query = data.read()
    with driver.transaction(db_name, TransactionType.SCHEMA) as tx:
        print("Defining schema", end="...")
        tx.query(define_query).resolve()
        tx.commit()
        print("OK")
# end::db-schema-setup[]


# tag::db-dataset-setup[]
def db_dataset_setup(driver, db_name, data_file='data_small_single_query.tql'):
    with open(data_file, 'r') as data:
        insert_query = data.read()
    with driver.transaction(db_name, TransactionType.WRITE) as tx:
        print("Loading data", end="...")
        tx.query(insert_query).resolve()
        tx.commit()
        print("OK")
# end::db-dataset-setup[]


# tag::test-db[]
def validate_data(driver, db_name) -> bool:
    with driver.transaction(db_name, TransactionType.READ) as tx:
        count_query = "match $u isa user; reduce $count = count;"
        print("Testing the dataset", end="...")
        count = next(tx.query(count_query).resolve().as_concept_rows()).get("count").try_get_integer()
        if count == 3:
            print("Passed")
            return True
        else:
            print("Validation failed, unexpected number of users:", count, "\n Expected result: 3. Terminating...")
            return False
# end::test-db[]


# tag::db-setup[]
def db_setup(driver, db_name, db_reset=False) -> bool:
    print(f"Setting up the database: {db_name}")
    if driver.databases.contains(db_name):
        if db_reset or (input("Found a pre-existing database. Do you want to replace it? (Y/N) ").lower() == "y"):
            if not replace_database(driver, db_name):
                return False
        else:
            print("Reusing an existing database.")
    else:  # No such database found on the server
        if not create_database(driver, db_name):
            print("Failed to create a new database. Terminating...")
            return False
    if driver.databases.contains(db_name):
        return validate_data(driver, db_name)
    else:
        print("Database not found. Terminating...")
        return False
# end::db-setup[]


# tag::fetch[]
def fetch_all_users(driver, db_name) -> list:
    with driver.transaction(db_name, TransactionType.READ) as tx:
        query = "match $u isa user; fetch { 'phone': $u.phone, 'email': $u.email };"
        answers = list(tx.query(query).resolve().as_concept_documents())
        for i, JSON in enumerate(answers, start=0):
            print(f"JSON #{i}: {JSON}")
        return answers
# end::fetch[]


# tag::insert[]
def insert_new_user(driver, db_name, email, phone, username) -> list:
    with driver.transaction(db_name, TransactionType.WRITE) as tx:
        query = f"""
        insert 
          $u isa user, has $e, has $p, has $username; 
          $e isa email '{email}'; 
          $p isa phone '{phone}'; 
          $username isa username '{username}';
        """
        answers = list(tx.query(query).resolve().as_concept_rows())
        tx.commit()
        for i, row in enumerate(answers, start=1):
            phone = row.get("p").try_get_string()
            email = row.get("e").try_get_string()
            print(f"Added new user. Phone: {phone}, E-mail: {email}")
        return answers
# end::insert[]


# tag::match[]
def get_direct_relatives_by_email(driver, db_name, email):
    with driver.transaction(db_name, TransactionType.READ) as tx:
        users = list(tx.query(f"match $u isa user, has email '{email}';").resolve().as_concept_rows())
        users_len = len(users)
        if users_len == 1:
            answers = list(tx.query(f"""
              match 
                $e == '{email}';
                $u isa user, has email $e;
                $family isa family ($u, $relative);
                $relative has username $username;
                not {{ $u is $relative; }};
              select $username;
              sort $username asc;
            """).resolve().as_concept_rows())
            for row in answers:
                print(f"Relative: {row.get('username').try_get_string()}")
            if len(answers) == 0:
                print("No relatives found.")
            return answers
        else:
            print(f"Error: Found {users_len} users, expected 1.")
            return None
# end::match[]


# tag::match-function[]
def get_all_relatives_by_email(driver, db_name, email):
    with driver.transaction(db_name, TransactionType.READ) as tx:
        users = list(tx.query(f"match $u isa user, has email '{email}';").resolve().as_concept_rows())
        users_len = len(users)
        if users_len == 1:
            answers = list(tx.query(f"""
              match 
                $u isa user, has email $e;
                $e == '{email}';
                let $relative in all_relatives($u);
                not {{ $u is $relative; }};
                $relative has username $username;
                select $username;
                sort $username asc;
            """).resolve().as_concept_rows())
            for row in answers:
                print(f"Relative: {row.get('username').try_get_string()}")
            if len(answers) == 0:
                print("No relatives found.")
            return answers
        else:
            print(f"Error: Found {users_len} users, expected 1.")
            return None
# end::match-function[]


# tag::update[]
def update_phone_by_email(driver, db_name, email, old, new):
    with driver.transaction(db_name, TransactionType.WRITE) as tx:
        answers = list(tx.query(f"""
          match $u isa user, has email '{email}', has phone $phone; $phone == '{old}';
          update $u has phone '{new}';
        """).resolve().as_concept_rows())
        tx.commit()
        answers_len = len(answers)
        if answers_len == 0:
            print("Error: No phones updated")
            return None
        else:
            print(f"Total number of phones updated: {len(answers)}")
            return answers
# end::update[]


# tag::delete[]
def delete_user_by_email(driver, db_name, email):
    with driver.transaction(db_name, TransactionType.WRITE) as tx:
        answers = list(tx.query(f"match $u isa user, has email '{email}'; delete $u;").resolve().as_concept_rows())
        tx.commit()
        answers_len = len(answers)
        if answers_len == 0:
            print("Error: No users deleted")
            return None
        else:
            print(f"Total number of users deleted: {len(answers)}")
            return answers
# end::delete[]


# tag::connection[]
def driver_connect(uri, username=USERNAME, password=PASSWORD):
    # tag::driver_new[]
    driver = TypeDB.driver(uri, Credentials(username, password), DriverOptions(False, None))
    # end::driver_new[]
    return driver
# end::connection[]


# tag::queries[]
def queries(driver, db_name):
    print("\nRequest 1 of 6: Fetch all users as JSON objects with emails and phone numbers")
    users = fetch_all_users(driver, DB_NAME)
    assert len(users) == 3

    new_phone = "17778889999"
    new_email = "jk@typedb.com"
    new_username = "k-koolidge"
    print(f"\nRequest 2 of 6: Add a new user with the email {new_email} and phone {new_phone}")
    insert_new_user(driver, DB_NAME, new_email, new_phone, new_username)

    kevin_email = "kevin.morrison@typedb.com"
    print(f"\nRequest 3 of 6: Find direct relatives of a user with email {kevin_email}")
    relatives = get_direct_relatives_by_email(driver, DB_NAME, kevin_email)
    assert relatives is not None
    assert len(relatives) == 1

    print(f"\nRequest 4 of 6: Transitively find all relatives of a user with email {kevin_email}")
    relatives = get_all_relatives_by_email(driver, DB_NAME, kevin_email)
    assert relatives is not None
    assert len(relatives) == 2

    old_kevin_phone = "110000000"
    new_kevin_phone = "110000002"
    print(f"\nRequest 5 of 6: Update the phone of a of user with email {kevin_email} from {old_kevin_phone} to {new_kevin_phone}")
    updated_users = update_phone_by_email(driver, DB_NAME, kevin_email, old_kevin_phone, new_kevin_phone)
    assert updated_users is not None
    assert len(updated_users) == 1

    print(f'\nRequest 6 of 6: Delete the user with email "{new_email}"')
    delete_user_by_email(driver, DB_NAME, new_email)
# end::queries[]


# tag::main[]
def main():
    with driver_connect(SERVER_ADDR) as driver:
        if db_setup(driver, DB_NAME, db_reset=False):
            queries(driver, DB_NAME)
        else:
            print("Terminating...")
            exit()
# end::main[]


if __name__ == "__main__":
    main()
# end::code[]
