// tag::import[]
use typedb_driver::{
    concept::{Attribute, Concept, Value}, Connection, DatabaseManager, Error, Options, Promise, Session, SessionType, TransactionType
};
// end::import[]

fn main() -> Result<(), Error> {
    const DB_NAME: &str = "sample_db";
    const SERVER_ADDR: &str = "127.0.0.1:1729";

    println!("TypeDB Manual sample code");

    println!(
        "Attempting to connect to a TypeDB Core server: {}",
        SERVER_ADDR
    );
    // tag::driver[]
    let driver = Connection::new_core(SERVER_ADDR)?;
    // end::driver[]
    // tag::databases[]
    let databases = DatabaseManager::new(driver);
    // end::databases[]
    // tag::list-db[]
    for db in databases.all()? {
        println!("{}", db.name());
    }
    // end::list-db[]
    // tag::delete-db[]
    if databases.contains(DB_NAME)? {
        let _ = databases.get(DB_NAME)?.delete();
    }
    // end::delete-db[]
    // tag::create-db[]
    let _ = databases.create(DB_NAME);
    // end::create-db[]
    if databases.contains(DB_NAME)? {
        println!("Database setup complete");
    }

    {   // tag::define[]
        let db = databases.get(DB_NAME)?;
        let session = Session::new(db, SessionType::Schema)?;
        let tx = session.transaction(TransactionType::Write)?;
        let define_query = "
                                define
                                email sub attribute, value string;
                                name sub attribute, value string;
                                friendship sub relation, relates friend;
                                user sub entity,
                                    owns email @key,
                                    owns name,
                                    plays friendship:friend;
                                admin sub user;
                                ";
        tx.query().define(define_query).resolve()?;
        tx.commit().resolve()?;
        // end::define[]
    }

    {   // tag::undefine[]
        let db = databases.get(DB_NAME)?;
        let session = Session::new(db, SessionType::Schema)?;
        let tx = session.transaction(TransactionType::Write)?;
        let undefine_query = "undefine admin sub user;";
        tx.query().undefine(undefine_query).resolve()?;
        tx.commit().resolve()?;
        // end::undefine[]
    }

    {   // tag::insert[]
        let db = databases.get(DB_NAME)?;
        let session = Session::new(db, SessionType::Data)?;
        let tx = session.transaction(TransactionType::Write)?;
        let insert_query = "
                                insert
                                $user1 isa user, has name 'Alice', has email 'alice@vaticle.com';
                                $user2 isa user, has name 'Bob', has email 'bob@vaticle.com';
                                $friendship (friend:$user1, friend: $user2) isa friendship;
                                ";
        let _ = tx.query().insert(insert_query)?;
        tx.commit().resolve()?;
        // end::insert[]
    }

    {   // tag::match-insert[]
        let db = databases.get(DB_NAME)?;
        let session = Session::new(db, SessionType::Data)?;
        let tx = session.transaction(TransactionType::Write)?;
        let match_insert_query = "
                                match
                                $u isa user, has name 'Bob';
                                insert
                                $new-u isa user, has name 'Charlie', has email 'charlie@vaticle.com';
                                $f($u,$new-u) isa friendship;
                                ";
        let response_count = tx.query().insert(match_insert_query)?.count();
        if response_count == 1 {
            tx.commit().resolve()?;
        } else {
            tx.force_close();
        }
        // end::match-insert[]
    }

    {   // tag::delete[]
        let db = databases.get(DB_NAME)?;
        let session = Session::new(db, SessionType::Data)?;
        let tx = session.transaction(TransactionType::Write)?;
        let delete_query = "
                                match
                                $u isa user, has name 'Charlie';
                                $f ($u) isa friendship;
                                delete
                                $f isa friendship;
                                ";
        let _ = tx.query().delete(delete_query).resolve();
        tx.commit().resolve()?;
        // end::delete[]
    }

    {   // tag::update[]
        let db = databases.get(DB_NAME)?;
        let session = Session::new(db, SessionType::Data)?;
        let tx = session.transaction(TransactionType::Write)?;
        let update_query = "
                                match
                                $u isa user, has name 'Charlie', has email $e;
                                delete
                                $u has $e;
                                insert
                                $u has email 'charles@vaticle.com';
                                ";
        let response_count = tx.query().update(update_query)?.count();
        if response_count == 1 {
            tx.commit().resolve()?;
        } else {
            tx.force_close();
        }
        // end::update[]
    }

    {   // tag::fetch[]
        let db = databases.get(DB_NAME)?;
        let session = Session::new(db, SessionType::Data)?;
        let tx = session.transaction(TransactionType::Read)?;
        let fetch_query = "
                                match
                                $u isa user;
                                fetch
                                $u: name, email;
                                ";
        let response = tx.query().fetch(fetch_query)?;
        for (i, json) in response.enumerate() {
            println!("User #{}: {}", (i + 1).to_string(), json.unwrap().to_string())
        }
        // end::fetch[]
    }

    {   // tag::get[]
        let db = databases.get(DB_NAME)?;
        let session = Session::new(db, SessionType::Data)?;
        let tx = session.transaction(TransactionType::Read)?;
        let get_query = "
                                match
                                $u isa user, has email $e;
                                get
                                $e;
                                ";
        let response = tx.query().get(get_query)?;
        for (i, cm) in response.enumerate() {
            let email_concept = cm.unwrap().get("e").unwrap().clone();
            let email = match email_concept {
                Concept::Attribute(Attribute {
                    value: Value::String(value),
                    ..
                }) => value,
                _ => unreachable!(),
            };
            println!("Email #{}: {}", (i + 1).to_string(), email)
        }
        // end::get[]
    }

    {   // tag::infer[]
        let db = databases.get(DB_NAME)?;
        let session = Session::new(db, SessionType::Schema)?;
        let tx = session.transaction(TransactionType::Write)?;
        let define_query = "
                                define
                                rule users:
                                when {
                                    $u isa user;
                                } then {
                                    $u has name 'User';
                                };
                                ";
        tx.query().define(define_query).resolve()?;
        tx.commit().resolve()?;

        let db = databases.get(DB_NAME)?;
        let options = Options::new().infer(true);
        let session = Session::new(db, SessionType::Data)?;
        let tx = session.transaction_with_options(TransactionType::Read, options)?;
        let fetch_query = "
                                match
                                $u isa user;
                                fetch
                                $u: name, email;
                                ";
        let response = tx.query().fetch(fetch_query)?;
        for (i, json) in response.enumerate() {
            println!("User #{}: {}", (i + 1).to_string(), json.unwrap().to_string())
        }
        // end::infer[]
    }
    Ok({})
}
