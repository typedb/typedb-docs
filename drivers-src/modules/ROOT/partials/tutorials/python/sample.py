# tag::code[]
# tag::import[]
from typedb.driver import TypeDB, SessionType, TransactionType, TypeDBOptions, TypeDBCredential
from enum import Enum
# end::import[]


# tag::enum[]
class Edition(Enum):
    Cloud = 1
    Core = 2
# end::enum[]


# tag::constants[]
DB_NAME = "sample_app_db"
SERVER_ADDR = "127.0.0.1:1729"
TYPEDB_EDITION = Edition.Core
CLOUD_USERNAME = "admin"
CLOUD_PASSWORD = "password"
# end::constants[]


# tag::create_new_db[]
def try_create_database(driver, db_name, db_reset=False) -> bool:
    if driver.databases.contains(db_name):
        if db_reset:
            print("Replacing an existing database", end="...")
            driver.databases.get(db_name).delete()  # Delete the database if it exists already
            driver.databases.create(db_name)
            print("OK")
            return True
        else:
            answer = input("Found a pre-existing database. Do you want to replace it? (Y/N) ")
            if answer.lower() == "y":
                return try_create_database(driver, db_name, db_reset=True)
            else:
                print("Reusing an existing database.")
                return False
    else:  # No such database found on the server
        print("Creating a new database", end="...")
        driver.databases.create(db_name)
        print("OK")
        return True
# end::create_new_db[]


# tag::db-schema-setup[]
def db_schema_setup(schema_session, schema_file='iam-schema.tql'):
    with open(schema_file, 'r') as data:
        define_query = data.read()
    with schema_session.transaction(TransactionType.WRITE) as tx:
        print("Defining schema", end="...")
        tx.query.define(define_query)
        tx.commit()
        print("OK")
# end::db-schema-setup[]


# tag::db-dataset-setup[]
def db_dataset_setup(data_session, data_file='iam-data-single-query.tql'):
    with open(data_file, 'r') as data:
        insert_query = data.read()
    with data_session.transaction(TransactionType.WRITE) as tx:
        print("Loading data", end="...")
        tx.query.insert(insert_query)
        tx.commit()
        print("OK")
# end::db-dataset-setup[]


# tag::test-db[]
def test_initial_database(data_session) -> bool:
    with data_session.transaction(TransactionType.READ) as tx:
        test_query = "match $u isa user; get $u; count;"
        print("Testing the database", end="...")
        response = tx.query.get_aggregate(test_query)
        result = response.resolve().as_value().as_long()
        if result == 3:
            print("Passed")
            return True
        else:
            print("Failed with the result:", result, "\n Expected result: 3.")
            return False
# end::test-db[]


# tag::db-setup[]
def db_setup(driver, db_name, db_reset=False) -> bool:
    print(f"Setting up the database: {db_name}")
    is_new = try_create_database(driver, db_name, db_reset)
    if not driver.databases.contains(db_name):
        print("Database creation failed. Terminating...")
        return False
    if is_new:
        with driver.session(db_name, SessionType.SCHEMA) as session:
            db_schema_setup(session)
        with driver.session(db_name, SessionType.DATA) as session:
            db_dataset_setup(session)
    with driver.session(db_name, SessionType.DATA) as session:
        return test_initial_database(session)
# end::db-setup[]


# tag::fetch[]
def fetch_all_users(driver, db_name) -> list:
    with driver.session(db_name, SessionType.DATA) as data_session:
        with data_session.transaction(TransactionType.READ) as read_tx:
            users = list(read_tx.query.fetch("match $u isa user; fetch $u: full-name, email;"))
            for i, JSON in enumerate(users, start=0):
                print(f"User #{i + 1} — Full-name:", JSON['u']['full-name'][0]['value'],
                      "E-mail:", JSON['u']['email'][0]['value'])
            return users
# end::fetch[]


# tag::insert[]
def insert_new_user(driver, db_name, name, email) -> list:
    with driver.session(db_name, SessionType.DATA) as data_session:
        with data_session.transaction(TransactionType.WRITE) as write_tx:
            response = list(
                write_tx.query.insert(
                    f"insert $p isa person, has full-name $fn, has email $e; $fn == '{name}'; $e == '{email}';"))
            write_tx.commit()
            for i, concept_map in enumerate(response, start=1):
                name = concept_map.get("fn").as_attribute().get_value()
                email = concept_map.get("e").as_attribute().get_value()
                print("Added new user. Name: " + name + ", E-mail:" + email)
            return response
# end::insert[]


# tag::get[]
def get_files_by_user(driver, db_name, name, inference=False):
    options = TypeDBOptions(infer=inference)
    with driver.session(db_name, SessionType.DATA) as data_session:
        with data_session.transaction(TransactionType.READ, options) as read_tx:
            users = list(read_tx.query.get(f"match $u isa user, has full-name '{name}'; get;"))
            if len(users) > 1:
                print("Error: Found more than one user with that name.")
                return None
            elif len(users) == 1:
                response = list(read_tx.query.get(f"""
                                                    match
                                                    $fn == '{name}';
                                                    $u isa user, has full-name $fn;
                                                    $p($u, $pa) isa permission;
                                                    $o isa object, has path $fp;
                                                    $pa($o, $va) isa access;
                                                    $va isa action, has name 'view_file';
                                                    get $fp; sort $fp asc;
                                                    """))
                for i, file in enumerate(response, start=1):
                    print(f"File #{i}:", file.get("fp").as_attribute().get_value())
                if len(response) == 0:
                    print("No files found. Try enabling inference.")
                return response
            else:
                print("Error: No users found with that name.")
                return None
# end::get[]


# tag::update[]
def update_filepath(driver, db_name, old, new):
    with driver.session(db_name, SessionType.DATA) as data_session:
        with data_session.transaction(TransactionType.WRITE) as write_tx:
            response = list(write_tx.query.update(f"""
                                                    match
                                                    $f isa file, has path $old_path;
                                                    $old_path = '{old}';
                                                    delete
                                                    $f has $old_path;
                                                    insert
                                                    $f has path $new_path;
                                                    $new_path = '{new}';
                                                    """))
            if len(response) > 0:
                write_tx.commit()
                print(f"Total number of paths updated: {len(response)}.")
                return response
            else:
                print("No matched paths: nothing to update.")
                return None
# end::update[]


# tag::delete[]
def delete_file(driver, db_name, path):
    with driver.session(db_name, SessionType.DATA) as data_session:
        with data_session.transaction(TransactionType.WRITE) as write_tx:
            response = list(write_tx.query.get(f"""
                                                match
                                                $f isa file, has path '{path}';
                                                get;
                                                """))
            if len(response) == 1:
                write_tx.query.delete(f"""
                                        match
                                        $f isa file, has path '{path}';
                                        delete
                                        $f isa file;
                                        """).resolve()
                write_tx.commit()
                print("The file has been deleted.")
                return True
            elif len(response) > 1:
                print("Matched more than one file with the same path.")
                print("No files were deleted.")
                return False
            else:
                print("No files matched in the database.")
                print("No files were deleted.")
                return False
# end::delete[]


# tag::connection[]
def connect_to_typedb(edition, addr, username=CLOUD_USERNAME, password=CLOUD_PASSWORD):
    if edition is Edition.Core:
        return TypeDB.core_driver(addr)
    if edition is Edition.Cloud:
        credentials = TypeDBCredential(username, password, tls_enabled=True)
        return TypeDB.cloud_driver(addr, credentials)
# end::connection[]


# tag::queries[]
def queries(driver, db_name):
    print("\nRequest 1 of 6: Fetch all users as JSON objects with full names and emails")
    users = fetch_all_users(driver, DB_NAME)
    assert len(users) == 3

    new_name = "Jack Keeper"
    new_email = "jk@vaticle.com"
    print(f"\nRequest 2 of 6: Add a new user with the full-name {new_name} and email {new_email}")
    insert_new_user(driver, DB_NAME, new_name, new_email)

    name = "Kevin Morrison"
    print(f"\nRequest 3 of 6: Find all files that the user {name} has access to view (no inference)")
    files = get_files_by_user(driver, DB_NAME, name)
    assert files is not None
    assert len(files) == 0

    print(f"\nRequest 4 of 6: Find all files that the user {name} has access to view (with inference)")
    files = get_files_by_user(driver, DB_NAME, name, inference=True)
    assert files is not None
    assert len(files) == 10

    old_path = 'lzfkn.java'
    new_path = 'lzfkn2.java'
    print(f"\nRequest 5 of 6: Update the path of a file from {old_path} to {new_path}")
    updated_files = update_filepath(driver, DB_NAME, old_path, new_path)
    assert updated_files is not None
    assert len(updated_files) == 1

    path = 'lzfkn2.java'
    print(f"\nRequest 6 of 6: Delete the file with path {path}")
    deleted = delete_file(driver, DB_NAME, path)
    assert deleted
# end::queries[]


# tag::main[]
def main():
    with connect_to_typedb(TYPEDB_EDITION, SERVER_ADDR) as driver:
        if db_setup(driver, DB_NAME, db_reset=False):
            queries(driver, DB_NAME)
        else:
            print("Terminating...")
            exit()
# end::main[]


if __name__ == "__main__":
    main()
# end::code[]
