// tag::code[]
// tag::import[]
use std::{error::Error, fs, io};

use typedb_driver::{
    answer::{ConceptMap, JSON},
    concept::{Attribute, Concept, Value},
    Connection, Credential, DatabaseManager, Error as TypeDBError, Options, Promise, Session, SessionType,
    TransactionType,
};
// end::import[]
// tag::constants[]
static DB_NAME: &str = "sample_app_db";
static SERVER_ADDR: &str = "127.0.0.1:1729";

enum Edition {
    Core,
    Cloud,
}

static TYPEDB_EDITION: Edition = Edition::Core;
static CLOUD_USERNAME: &str = "admin";
static CLOUD_PASSWORD: &str = "password";
// end::constants[]
// tag::fetch[]
fn fetch_all_users(driver: Connection, db_name: String) -> Result<Vec<JSON>, Box<dyn Error>> {
    let databases = DatabaseManager::new(driver);
    let session = Session::new(databases.get(db_name)?, SessionType::Data)?;
    let tx = session.transaction(TransactionType::Read)?;
    let iterator = tx.query().fetch("match $u isa user; fetch $u: full-name, email;")?;
    let mut count = 0;
    let mut result = vec![];
    for item in iterator {
        count += 1;
        let json = item?;
        println!("User #{}: {}", count.to_string(), json.to_string());
        result.push(json);
    }
    if result.len() > 0 {
        Ok(result)
    } else {
        Err(Box::new(TypeDBError::Other("Error: No users found in a database.".to_string())))
    }
}
// end::fetch[]
// tag::insert[]
fn insert_new_user(
    driver: Connection,
    db_name: String,
    new_name: &str,
    new_email: &str,
) -> Result<Vec<ConceptMap>, Box<dyn Error>> {
    let databases = DatabaseManager::new(driver);
    let session = Session::new(databases.get(db_name)?, SessionType::Data)?;
    let tx = session.transaction(TransactionType::Write)?;
    let iterator = tx.query().insert(&format!(
        "insert $p isa person, has full-name $fn, has email $e; $fn == '{}'; $e == '{}';",
        new_name, new_email
    ))?;
    let mut result = vec![];
    for item in iterator {
        let concept_map = item?;
        let name = unwrap_string(concept_map.get("fn").unwrap().clone());
        let email = unwrap_string(concept_map.get("e").unwrap().clone());
        println!("Added new user. Name: {}, E-mail: {}", name, email);
        result.push(concept_map);
    }
    if result.len() > 0 {
        let _ = tx.commit().resolve();
        Ok(result)
    } else {
        Err(Box::new(TypeDBError::Other("Error: No users found in a database.".to_string())))
    }
}
// end::insert[]
// tag::get[]
fn get_files_by_user(
    driver: Connection,
    db_name: String,
    name: &str,
    inference: bool,
) -> Result<Vec<(usize, ConceptMap)>, Box<dyn Error>> {
    let databases = DatabaseManager::new(driver);
    let session = Session::new(databases.get(db_name)?, SessionType::Data)?;
    let tx = session.transaction_with_options(TransactionType::Read, Options::new().infer(inference))?;
    let users = tx
        .query()
        .get(&format!("match $u isa user, has full-name '{}'; get;", name))?
        .map(|x| x.unwrap())
        .collect::<Vec<_>>();
    let response;
    if users.len() > 1 {
        return Err(Box::new(TypeDBError::Other("Found more than one user with that name.".to_string())));
    } else if users.len() == 1 {
        response = tx
            .query()
            .get(&format!(
                "match
                $fn == '{}';
                $u isa user, has full-name $fn;
                $p($u, $pa) isa permission;
                $o isa object, has path $fp;
                $pa($o, $va) isa access;
                $va isa action, has name 'view_file';
                get $fp; sort $fp asc;
                ",
                name
            ))?
            .map(|x| x.unwrap())
            .enumerate()
            .collect::<Vec<_>>();
        for (count, file) in &response {
            println!("File #{}: {}", count + 1, unwrap_string(file.get("fp").unwrap().clone()));
        }
        if response.len() == 0 {
            println!("No files found. Try enabling inference.");
        }
        return Ok(response);
    } else {
        return Err(Box::new(TypeDBError::Other("No users found with that name.".to_string())));
    }
}
// end::get[]
// tag::update[]
fn update_filepath(
    driver: Connection,
    db_name: String,
    old_path: &str,
    new_path: &str,
) -> Result<Vec<ConceptMap>, Box<dyn Error>> {
    let databases = DatabaseManager::new(driver);
    let session = Session::new(databases.get(db_name)?, SessionType::Data)?;
    let tx = session.transaction(TransactionType::Write)?;
    let response = tx
        .query()
        .update(&format!(
            "match
            $f isa file, has path $old_path;
            $old_path = '{old}';
            delete
            $f has $old_path;
            insert
            $f has path $new_path;
            $new_path = '{new}';",
            old = old_path,
            new = new_path
        ))?
        .map(|x| x.unwrap())
        .collect::<Vec<_>>();
    if response.len() > 0 {
        let _ = tx.commit().resolve();
        println!("Total number of paths updated: {}", response.len());
        return Ok(response);
    } else if response.len() == 0 {
        println!("No matched paths: nothing to update");
        return Ok(response);
    } else {
        return Err(Box::new(TypeDBError::Other("Impossible query response.".to_string())));
    }
}
// end::update[]
// tag::delete[]
fn delete_file(driver: Connection, db_name: String, path: &str) -> Result<(), Box<dyn Error>> {
    let databases = DatabaseManager::new(driver);
    let session = Session::new(databases.get(db_name)?, SessionType::Data)?;
    let tx = session.transaction(TransactionType::Write)?;
    let files = tx
        .query()
        .get(&format!(
            "match
            $f isa file, has path '{}';
            get;",
            path
        ))?
        .map(|x| x.unwrap())
        .collect::<Vec<_>>();
    if files.len() == 1 {
        let response = tx
            .query()
            .delete(&format!(
                "match
                $f isa file, has path '{path}';
                delete
                $f isa file;
                "
            ))
            .resolve();
        match response {
            Ok(_) => {
                println!("File has been deleted.");
                Ok(())
            }
            Err(_) => return Err(Box::new(TypeDBError::Other("Error: Failed to delete.".to_string()))),
        }
    } else {
        return Err(Box::new(TypeDBError::Other(
            format!("Wrong number of files to delete: {}", files.len()).to_string(),
        )));
    }
}
// end::delete[]
// tag::queries[]
fn queries(driver: Connection, db_name: String) -> Result<(), Box<dyn Error>> {
    println!("Request 1 of 6: Fetch all users as JSON objects with full names and emails");
    let users = fetch_all_users(driver.clone(), db_name.clone());
    assert!(users?.len() == 3);

    let new_name = "Jack Keeper";
    let new_email = "jk@vaticle.com";
    println!("Request 2 of 6: Add a new user with the full-name {} and email {}", new_name, new_email);
    let new_user = insert_new_user(driver.clone(), db_name.clone(), new_name, new_email);
    assert!(new_user?.len() == 1);

    let infer = false;
    let name = "Kevin Morrison";
    println!("Request 3 of 6: Find all files that the user {} has access to view (no inference)", name);
    let no_files = get_files_by_user(driver.clone(), db_name.clone(), name, infer);
    assert!(no_files?.len() == 0);

    let infer = true;
    println!("Request 4 of 6: Find all files that the user {} has access to view (with inference)", name);
    let files = get_files_by_user(driver.clone(), db_name.clone(), name, infer);
    assert!(files?.len() == 10);

    let old_path = "lzfkn.java";
    let new_path = "lzfkn2.java";
    println!("Request 5 of 6: Update the path of a file from {} to {}", old_path, new_path);
    let updated_files = update_filepath(driver.clone(), db_name.clone(), old_path, new_path);
    assert!(updated_files?.len() == 1);

    let path = "lzfkn2.java";
    println!("Request 6 of 6: Delete the file with path {}", path);
    let deleted = delete_file(driver.clone(), db_name.clone(), path);

    match deleted {
        Ok(_) => return Ok(()),
        Err(_) => return Err(Box::new(TypeDBError::Other("Application terminated unexpectedly".to_string()))),
    };
}
// end::queries[]
// tag::connection[]
fn connect_to_typedb(edition: &Edition, addr: &str) -> Result<Connection, typedb_driver::Error> {
    match edition {
        Edition::Core => return Connection::new_core(addr),
        Edition::Cloud => {
            return Connection::new_cloud(&[addr], Credential::with_tls(CLOUD_USERNAME, CLOUD_PASSWORD, None)?)
        }
    };
}
// end::connection[]
// tag::create_new_db[]
fn try_create_database(driver: &Connection, db_name: String, db_reset: bool) -> Result<bool, TypeDBError> {
    let databases = DatabaseManager::new(driver.to_owned());
    if databases.contains(&db_name)? {
        if db_reset {
            print!("Replacing an existing database...");
            databases.get(&db_name)?.delete()?;
            let result = databases.create(&db_name);

            match result {
                Ok(_) => {
                    println!("OK");
                    return Ok(true);
                }
                Err(x) => return Err(x),
            };
        } else {
            let mut answer = String::new();
            print!("Found a pre-existing database. Do you want to replace it? (Y/N) ");
            io::Write::flush(&mut io::stdout()).unwrap();
            io::stdin().read_line(&mut answer).expect("Failed to read a line");
            if answer.trim().to_lowercase() == "y" {
                return try_create_database(driver, db_name, true);
            } else {
                println!("Reusing an existing database.");
                return Ok(false);
            }
        }
    } else {
        // No such database found on the server
        print!("Creating a new database...");
        let result = databases.create(&db_name);
        match result {
            Ok(_) => {
                println!("OK");
                return Ok(false);
            }
            Err(x) => return Err(x),
        };
    }
}
// end::create_new_db[]
// tag::db-schema-setup[]
fn db_schema_setup(schema_session: &Session, schema_file: String) -> Result<(), TypeDBError> {
    let tx = schema_session.transaction(TransactionType::Write)?;
    let data = fs::read_to_string(schema_file)?; // "iam-schema.tql"
    print!("Defining schema...");
    let response = tx.query().define(&data).resolve();
    tx.commit().resolve()?;
    println!("OK");
    return response;
}
// end::db-schema-setup[]
// tag::db-dataset-setup[]
fn db_dataset_setup(data_session: &Session, data_file: String) -> Result<(), Box<dyn Error>> {
    let tx = data_session.transaction(TransactionType::Write)?;
    let data = fs::read_to_string(data_file)?; // "iam-data-single-query.tql"
    print!("Loading data...");
    let response = tx.query().insert(&data)?;
    let result = response.collect::<Vec<_>>();
    tx.commit().resolve()?;
    println!("OK");
    Ok({
        drop(result);
    })
}
// end::db-dataset-setup[]
// tag::test-db[]
fn test_initial_database(data_session: &Session) -> Result<bool, Box<dyn Error>> {
    let tx = data_session.transaction(TransactionType::Write)?;
    let test_query = "match $u isa user; get $u; count;";
    print!("Testing the database...");
    let response = tx.query().get_aggregate(test_query).resolve();
    let result = match response?.ok_or("Error: unexpected test query response.")? {
        Value::Long(value) => value,
        _ => unreachable!(),
    };
    if result == 3 {
        println!("OK");
        Ok(true)
    } else {
        Err(Box::new(TypeDBError::Other("Test failed. Terminating...".to_string())))
    }
}
// end::test-db[]
// tag::db-setup[]
pub fn db_setup(driver: Connection, db_name: String) -> Result<(), Box<dyn Error>> {
    println!("Setting up the database: {}", &db_name);
    let is_new = try_create_database(&driver, db_name.clone(), false);
    {
        let databases = DatabaseManager::new(driver.clone());
        {
            let schema_session = Session::new(databases.get(&db_name)?, SessionType::Schema)?;
            db_schema_setup(&schema_session, "iam-schema.tql".to_string())?;
        }
        {
            let data_session = Session::new(databases.get(&db_name)?, SessionType::Data)?;
            if is_new? {
                db_dataset_setup(&data_session, "iam-data-single-query.tql".to_string())?;
            }
            if test_initial_database(&data_session)? {
                Ok(())
            } else {
                Err(Box::new(TypeDBError::Other("Test failed. Terminating...".to_string())))
            }
        }
    }
}
// end::db-setup[]
// tag::main[]
fn main() -> Result<(), Box<dyn Error>> {
    println!("Sample App");
    let driver = connect_to_typedb(&TYPEDB_EDITION, SERVER_ADDR)?;
    match db_setup(driver.clone(), DB_NAME.to_owned()) {
        Ok(()) => match queries(driver, DB_NAME.to_owned()) {
            Ok(_) => {
                return Ok(());
            }
            Err(x) => return Err(x),
        },
        Err(_) => return Err(Box::new(TypeDBError::Other("DB setup failed.".to_string()))),
    };
}
// end::main[]
// tag::string[]
fn unwrap_string(concept: Concept) -> String {
    match concept {
        Concept::Attribute(Attribute { value: Value::String(value), .. }) => value,
        _ => unreachable!(),
    }
}
// end::string[]
// end::code[]
