// tag::code[]
// tag::import[]
use std::{error::Error, fs, io, process};
use std::io::{BufRead, Write};

use futures_util::stream::TryStreamExt;
use futures_util::StreamExt;
use typedb_driver::{answer::{ConceptRow, JSON}, Credentials, DriverOptions, Error as TypeDBError, TransactionType, TypeDBDriver};

// end::import[]
// tag::constants[]
static DB_NAME: &str = "sample_app_db";
static SERVER_ADDR: &str = "127.0.0.1:1729";

static USERNAME: &str = "admin";
static PASSWORD: &str = "password";

// end::constants[]
// tag::fetch[]
async fn fetch_all_users(driver: &TypeDBDriver, db_name: &str) -> Result<Vec<JSON>, Box<dyn Error>> {
    let tx = driver.transaction(db_name, TransactionType::Read).await?;
    let response = tx.query("match $u isa user; fetch { 'phone': $u.phone, 'email': $u.email };").await?;
    let documents = response.into_documents().try_collect::<Vec<_>>().await?;
    let mut documents_json = vec![];
    for (index, document) in documents.into_iter().enumerate() {
        let as_json = document.into_json();
        println!("User #{}: {}", index, &as_json);
        documents_json.push(as_json);
    }
    if documents_json.len() > 0 {
        Ok(documents_json)
    } else {
        Err(Box::new(TypeDBError::Other("Error: No users found in a database.".to_string())))
    }
}

// end::fetch[]
// tag::insert[]
async fn insert_new_user(
    driver: &TypeDBDriver,
    db_name: &str,
    new_email: &str,
    new_phone: &str,
    new_username: &str,
) -> Result<Vec<ConceptRow>, Box<dyn Error>> {
    let tx = driver.transaction(db_name, TransactionType::Write).await?;
    let response = tx.query(&format!(
        "insert $u isa user, has $e, has $p, has $username; $e isa email '{}'; $p isa phone '{}'; $username isa username '{}';",
        new_email, new_phone, new_username
    )).await?;
    let rows = response.into_rows().try_collect::<Vec<_>>().await?;
    for row in &rows {
        let email = row.get("e").unwrap().unwrap().try_get_string().unwrap();
        let phone = row.get("p").unwrap().unwrap().try_get_string().unwrap();
        println!("Added new user. Phone: {}, E-mail: {}", phone, email);
    }
    if rows.len() > 0 {
        tx.commit().await?;
        Ok(rows)
    } else {
        Err(Box::new(TypeDBError::Other("Error: No new users created.".to_string())))
    }
}

// end::insert[]
// tag::match[]
async fn get_direct_relatives_by_email(
    driver: &TypeDBDriver,
    db_name: &str,
    email: &str,
) -> Result<Vec<ConceptRow>, Box<dyn Error>> {
    let tx = driver.transaction(db_name, TransactionType::Read).await?;
    let rows = tx
        .query(&format!("match $u isa user, has email '{}';", email)).await?
        .into_rows()
        .try_collect::<Vec<_>>()
        .await?;
    if rows.len() != 1 {
        return Err(Box::new(TypeDBError::Other(format!("Found {} users with email {}, expected 1.", rows.len(), email))));
    }
    let relative_emails = tx
        .query(&format!(
            "match
                $e == '{}';
                $u isa user, has email $e;
                $family isa family ($u, $relative);
                $relative has username $username;
                not {{ $u is $relative; }};
                select $username;
                sort $username asc;
                ",
            email
        )).await?
        .into_rows()
        .try_collect::<Vec<_>>()
        .await?;
    for (count, row) in relative_emails.iter().enumerate() {
        println!("Relative #{}: {}", count + 1, row.get("username").unwrap().unwrap().try_get_string().unwrap());
    }
    Ok(relative_emails)
}


// end::match[]
// tag::match-function[]
async fn get_all_relatives_by_email(
    driver: &TypeDBDriver,
    db_name: &str,
    email: &str,
) -> Result<Vec<ConceptRow>, Box<dyn Error>> {
    let tx = driver.transaction(db_name, TransactionType::Read).await?;
    let rows = tx
        .query(&format!("match $u isa user, has email '{}';", email)).await?
        .into_rows()
        .try_collect::<Vec<_>>()
        .await?;
    if rows.len() != 1 {
        return Err(Box::new(TypeDBError::Other(format!("Found {} users with email {}, expected 1.", rows.len(), email))));
    }
    let relative_emails = tx
        .query(&format!(
            "match
                $u isa user, has email $e;
                $e == '{}';
                let $relative in all_relatives($u);
                not {{ $u is $relative; }};
                $relative has username $username;
                select $username;
                sort $username asc;
                ",
            email
        )).await?
        .into_rows()
        .try_collect::<Vec<_>>()
        .await?;
    for (count, row) in relative_emails.iter().enumerate() {
        println!("Relative #{}: {}", count + 1, row.get("username").unwrap().unwrap().try_get_string().unwrap());
    }
    Ok(relative_emails)
}

// end::match-function[]
// tag::update[]
async fn update_phone_by_email(
    driver: &TypeDBDriver,
    db_name: &str,
    email: &str,
    old_phone: &str,
    new_phone: &str,
) -> Result<Vec<ConceptRow>, Box<dyn Error>> {
    let tx = driver.transaction(db_name, TransactionType::Write).await?;
    let rows = tx
        .query(&format!(
            "match $u isa user, has email '{email}', has phone $phone; $phone == '{old_phone}';
            update $u has phone '{new_phone}';",
        ))
        .await?
        .into_rows()
        .try_collect::<Vec<_>>()
        .await?;
    tx.commit().await?;
    println!("Total number of users updated: {}", rows.len());
    Ok(rows)
}

// end::update[]
// tag::delete[]
async fn delete_user_by_email(driver: &TypeDBDriver, db_name: &str, email: &str) -> Result<(), Box<dyn Error>> {
    let tx = driver.transaction(db_name, TransactionType::Write).await?;
    let rows = tx.query(&format!(
        "match $u isa user, has email '{email}';
        delete $u;"
    ))
        .await?
        .into_rows()
        .try_collect::<Vec<_>>()
        .await?;
    println!("Deleted {} users", rows.len());
    Ok(())
}

// end::delete[]
// tag::queries[]
async fn queries(driver: &TypeDBDriver, db_name: &str) -> Result<(), Box<dyn Error>> {
    println!("\nRequest 1 of 6: Fetch all users as JSON objects with emails and phone numbers");
    let users = fetch_all_users(driver, db_name).await?;
    assert_eq!(users.len(), 3);

    let new_user_phone = "17778889999";
    let new_user_email = "k.koolidge@typedb.com";
    let new_user_username = "k-koolidge";
    println!("\nRequest 2 of 6: Add a new user with the email {} and phone {}", new_user_email, new_user_phone);
    let new_user = insert_new_user(driver, db_name, new_user_email, new_user_phone, new_user_username).await?;
    assert_eq!(new_user.len(), 1);

    let kevin_email = "kevin.morrison@typedb.com";
    println!("\nRequest 3 of 6: Find direct relatives of a user with email {}", kevin_email);
    let direct_relatives = get_direct_relatives_by_email(driver, db_name, kevin_email).await?;
    assert_eq!(direct_relatives.len(), 1);

    println!("\nRequest 4 of 6: Transitively find all relatives of a user with email {}", kevin_email);
    let all_relatives = get_all_relatives_by_email(driver, db_name, kevin_email).await?;
    assert_eq!(all_relatives.len(), 2);

    let old_kevin_phone = "110000000";
    let new_kevin_phone = "110000002";
    println!("\nRequest 5 of 6: Update the phone of a of user with email {} from {} to {}", kevin_email, old_kevin_phone, new_kevin_phone);
    let updated_users = update_phone_by_email(driver, db_name, kevin_email, old_kevin_phone, new_kevin_phone).await?;
    assert!(updated_users.len() == 1);

    println!("\nRequest 6 of 6: Delete the user with email {}", new_user_email);
    delete_user_by_email(driver, db_name, new_user_email).await
}

// end::queries[]
// WARNING: keep when changing the AsRef and signatures, ensure they aren't required as-is for code snippets throughout docs
// tag::connection[]
async fn driver_connect(
    uri: &str,
    username: impl AsRef<str>,
    password: impl AsRef<str>,
) -> Result<TypeDBDriver, typedb_driver::Error> {
    let username = username.as_ref();
    let password = password.as_ref();
    #[allow(clippy::let_and_return, reason = "tutorial readability")]
    // tag::driver_new[]
    let driver = TypeDBDriver::new(
        &uri,
        Credentials::new(username, password),
        DriverOptions::new(false, None).unwrap(),
    ).await;
    // end::driver_new[]
    driver
}
// end::connection[]

// tag::create_new_db[]
async fn create_database(driver: &TypeDBDriver, db_name: impl AsRef<str>) -> Result<bool, Box<dyn Error>> {
    print!("Creating a new database...");
    let result = driver.databases().create(db_name.as_ref()).await;
    match result {
        Ok(_) => println!("OK"),
        Err(err) => return Err(Box::new(TypeDBError::Other(format!("Failed to create a DB, due to: {}", err)))),
    };
    db_schema_setup(driver, db_name.as_ref(), "schema.tql").await?;
    db_dataset_setup(driver, db_name.as_ref(), "data_small_single_query.tql").await?;
    return Ok(true);
}

// end::create_new_db[]
// tag::replace_db[]
async fn replace_database(driver: &TypeDBDriver, db_name: &str) -> Result<bool, Box<dyn Error>> {
    print!("Deleting an existing database...");
    let deletion_result = driver.databases().get(db_name).await?.delete().await;
    match deletion_result {
        Ok(_) => println!("OK"),
        Err(err) => return Err(Box::new(TypeDBError::Other(format!("Failed to delete a database, due to: {}", err))))
    };
    let creation_result = create_database(&driver, db_name).await;
    match creation_result {
        Ok(_) => return Ok(true),
        Err(err) => return Err(Box::new(TypeDBError::Other(format!("Failed to create a new database, due to: {}", err))))
    };
}
// end::replace_db[]

// tag::db-schema-setup[]
async fn db_schema_setup(driver: &TypeDBDriver, db_name: &str, schema_file_path: &str) -> Result<(), TypeDBError> {
    let tx = driver.transaction(db_name, TransactionType::Schema).await?;
    let schema_query = fs::read_to_string(schema_file_path)
        .map_err(|err| TypeDBError::Other(format!("Error loading file content from '{schema_file_path}', due to: {}", err)))?;
    print!("Defining schema...");
    let response = tx.query(&schema_query).await?;
    assert!(response.is_ok());
    tx.commit().await?;
    println!("OK");
    Ok(())
}

// end::db-schema-setup[]
// tag::db-dataset-setup[]
async fn db_dataset_setup(driver: &TypeDBDriver, db_name: &str, data_file_path: &str) -> Result<(), Box<dyn Error>> {
    let tx = driver.transaction(db_name, TransactionType::Write).await?;
    let data = fs::read_to_string(data_file_path)
        .map_err(|err| TypeDBError::Other(format!("Error loading file content from '{data_file_path}', due to: {}", err)))?;
    print!("Loading data...");
    let response = tx.query(&data).await?;
    assert!(response.is_row_stream());
    let results = response.into_rows().try_collect::<Vec<_>>().await?;
    assert!(results.len() > 0);
    tx.commit().await?;
    println!("OK");
    Ok(())
}

// end::db-dataset-setup[]
// tag::validate-db[]
async fn validate_data(driver: &TypeDBDriver, db_name: &str) -> Result<bool, Box<dyn Error>> {
    let tx = driver.transaction(db_name, TransactionType::Read).await?;
    let count_query = "match $u isa user; reduce $count = count;";
    print!("Validating the dataset...");
    let response = tx.query(count_query).await?;
    assert!(response.is_row_stream());
    let row = response.into_rows().next().await.unwrap()?;
    let count = row.get("count").unwrap().unwrap().try_get_integer().unwrap();
    if count == 3 {
        println!("OK");
        Ok(true)
    } else {
        Err(Box::new(TypeDBError::Other(format!("Validation failed, unexpected number of users: {}. Terminating...", count))))
    }
}

// end::validate-db[]
// tag::db-setup[]
async fn db_setup(driver: &TypeDBDriver, db_name: &str, db_reset: bool) -> Result<bool, Box<dyn Error>> {
    println!("Setting up the database: {}", db_name);
    if driver.databases().contains(db_name).await? {
        if db_reset {
            replace_database(&driver, db_name).await?;
        } else {
            print!("Found a pre-existing database. Do you want to replace it? (Y/N) ");
            io::stdout().flush()?;
            let answer = io::stdin().lock().lines().next().unwrap().unwrap();
            if answer.trim().to_lowercase() == "y" {
                replace_database(&driver, db_name).await?;
            } else {
                println!("Reusing an existing database.");
            }
        }
    } else {
        // No such database found on the server
        create_database(&driver, db_name).await?;
    }
    validate_data(&driver, db_name).await
}
// end::db-setup[]

// tag::main[]
#[tokio::main]
async fn main() {
    println!("Sample App");
    let driver = driver_connect(SERVER_ADDR, USERNAME, PASSWORD).await
        .map_err(|err| {
            println!("{err}");
            process::exit(1);
        })
        .unwrap();
    db_setup(&driver, DB_NAME, false).await
        .map_err(|err| {
            println!("{err}");
            process::exit(1);
        })
        .unwrap();
    queries(&driver, DB_NAME).await
        .map_err(|err| {
            println!("{err}");
            process::exit(1);
        })
        .unwrap();
}
// end::main[]
// end::code[]
