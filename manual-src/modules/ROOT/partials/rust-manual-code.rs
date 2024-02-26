// tag::import[]
use std::error::Error;

use typedb_driver::{
    concept::{Attribute, Concept, Transitivity, Value, ValueType},
    transaction::{
        concept::api::{EntityTypeAPI, ThingAPI, ThingTypeAPI},
        logic::api::RuleAPI,
    },
    Connection, Credential, DatabaseManager, Options, Promise, Session, SessionType, TransactionType,
};
// end::import[]

fn main() -> Result<(), Box<dyn Error>> {
    const DB_NAME: &str = "sample_db";
    const SERVER_ADDR: &str = "127.0.0.1:1729";

    println!("TypeDB Manual sample code");

    println!("Attempting to connect to a TypeDB Core server: {}", SERVER_ADDR);
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
    if databases.contains(DB_NAME)? {
        // tag::delete-db[]
        let _ = databases.get(DB_NAME)?.delete();
        // end::delete-db[]
    }
    // tag::create-db[]
    let _ = databases.create(DB_NAME);
    // end::create-db[]
    if databases.contains(DB_NAME)? {
        println!("Database setup complete");
    }
    {
        let _ = || -> Result<(), Box<dyn Error>> {
            // tag::connect_core[]
            let driver = Connection::new_core("127.0.0.1:1729")?;
            // end::connect_core[]
            // tag::connect_cloud[]
            let driver = Connection::new_cloud(&["127.0.0.1:1729"], Credential::with_tls("admin", "password", None)?)?;
            // end::connect_cloud[]
            // tag::session_open[]
            let session = Session::new(databases.get(DB_NAME)?, SessionType::Schema)?;
            // end::session_open[]
            // tag::tx_open[]
            let tx = session.transaction(TransactionType::Write)?;
            // end::tx_open[]
            // tag::tx_close[]
            tx.force_close();
            // end::tx_close[]
            if tx.is_open() {
                // tag::tx_commit[]
                let _ = tx.commit();
                // end::tx_commit[]
            }
            // tag::session_close[]
            let _ = session.force_close();
            // end::session_close[]
            Ok({})
        };
    }
    {
        // tag::define[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Schema)?;
            {
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
            }
        }
        // end::define[]
    }

    {
        // tag::undefine[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Schema)?;
            {
                let tx = session.transaction(TransactionType::Write)?;
                let undefine_query = "undefine admin sub user;";
                tx.query().undefine(undefine_query).resolve()?;
                tx.commit().resolve()?;
            }
        }
        // end::undefine[]
    }

    {
        // tag::insert[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Data)?;
            {
                let tx = session.transaction(TransactionType::Write)?;
                let insert_query = "
                                    insert
                                    $user1 isa user, has name 'Alice', has email 'alice@vaticle.com';
                                    $user2 isa user, has name 'Bob', has email 'bob@vaticle.com';
                                    $friendship (friend:$user1, friend: $user2) isa friendship;
                                    ";
                let _ = tx.query().insert(insert_query)?;
                tx.commit().resolve()?;
            }
        }
        // end::insert[]
    }

    {
        // tag::match-insert[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Data)?;
            {
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
            }
        }
        // end::match-insert[]
    }

    {
        // tag::delete[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Data)?;
            {
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
            }
        }
        // end::delete[]
    }

    {
        // tag::update[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Data)?;
            {
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
            }
        }
        // end::update[]
    }

    {
        // tag::fetch[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Data)?;
            {
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
            }
        }
        // end::fetch[]
    }

    {
        // tag::get[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Data)?;
            {
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
                        Concept::Attribute(Attribute { value: Value::String(value), .. }) => value,
                        _ => unreachable!(),
                    };
                    println!("Email #{}: {}", (i + 1).to_string(), email)
                }
            }
        }
        // end::get[]
    }

    {
        // tag::infer-rule[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Schema)?;
            {
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
            }
        }
        // end::infer-rule[]
        // tag::infer-fetch[]
        let db = databases.get(DB_NAME)?;
        let options = Options::new().infer(true);
        {
            let session = Session::new(db, SessionType::Data)?;
            {
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
            }
        }
        // end::infer-fetch[]
    }

    {
        // tag::types-editing[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Schema)?;
            {
                let tx = session.transaction(TransactionType::Write)?;
                let tag = &tx.concept().put_attribute_type("tag".to_owned(), ValueType::String).resolve()?;
                let entities = tx
                    .concept()
                    .get_entity_type("entity".to_owned())
                    .resolve()?
                    .ok_or("No root entity")?
                    .get_subtypes(&tx, Transitivity::Explicit)?;
                for entity in entities {
                    let mut e = entity?;
                    println!("{}", e.label);
                    if !(e.is_abstract()) {
                        let _ = e.set_owns(&tx, tag.clone(), None, vec![]);
                    }
                }
                let _ = tx.commit().resolve();
            }
        }
        // end::types-editing[]
    }

    {
        // tag::types-api[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Schema)?;
            {
                let tx = session.transaction(TransactionType::Write)?;
                let user_type = tx.concept().get_entity_type("user".to_owned()).resolve()?.ok_or("No root entity")?;
                let mut admin_type = tx.concept().put_entity_type("admin".to_owned()).resolve()?;
                drop(admin_type.set_supertype(&tx, user_type).resolve());
                let entities = tx
                    .concept()
                    .get_entity_type("entity".to_owned())
                    .resolve()?
                    .ok_or("No root entity")?
                    .get_subtypes(&tx, Transitivity::Transitive)?;
                for subtype in entities {
                    println!("{}", subtype?.label);
                }
                let _ = tx.commit().resolve();
            }
        }
        // end::types-api[]
    }
    {
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Schema)?;
            {
                let tx = session.transaction(TransactionType::Write)?;
                // tag::get_type[]
                let user_type = tx.concept().get_entity_type("user".to_owned()).resolve()?.unwrap();
                // end::get_type[]
                // tag::add_type[]
                let mut admin_type = tx.concept().put_entity_type("admin".to_owned()).resolve()?;
                // end::add_type[]
                // tag::set_supertype[]
                drop(admin_type.set_supertype(&tx, user_type.clone()).resolve());
                // end::set_supertype[]
                // tag::get_instances[]
                let users = user_type.get_instances(&tx, Transitivity::Transitive)?;
                // end::get_instances[]
                for user in users {
                    // tag::get_has[]
                    let attributes = user?.get_has(&tx, vec![], vec![])?;
                    // end::get_has[]
                }
                // tag::create[]
                let new_user =
                    tx.concept().get_entity_type("user".to_owned()).resolve()?.unwrap().create(&tx).resolve()?;
                // end::create[]
                // tag::delete_user[]
                let _ = new_user.delete(&tx).resolve();
                // end::delete_user[]
            }
        }
    }
    {
        // tag::rules-api[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Schema)?;
            {
                let tx = session.transaction(TransactionType::Write)?;
                let rules = tx.logic().get_rules()?;
                for rule in rules {
                    println!("{}", rule.clone()?.label);
                    println!("{}", rule.clone()?.when.to_string());
                    println!("{}", rule.clone()?.then.to_string());
                }
                let condition = typeql::parse_pattern("{$u isa user, has email $e; $e contains '@vaticle.com';}")?
                    .into_conjunction();
                let conclusion = typeql::parse_pattern("$u has name 'Employee'")?.into_statement();
                let mut new_rule = tx.logic().put_rule("Employee".to_string(), condition, conclusion).resolve()?;
                let _ = new_rule.delete(&tx).resolve();
                let old_rule = tx.logic().get_rule("users".to_owned()).resolve()?.ok_or("Rule not found.")?;
                let _ = tx.commit().resolve();
            }
        }
        // end::rules-api[]
    }
    {
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Schema)?;
            {
                let tx = session.transaction(TransactionType::Write)?;
                // tag::get_rule[]
                let old_rule = tx.logic().get_rule("users".to_owned()).resolve()?.ok_or("Rule not found.")?;
                // end::get_rule[]
                // tag::put_rule[]
                let condition = typeql::parse_pattern("{$u isa user, has email $e; $e contains '@vaticle.com';}")?
                    .into_conjunction();
                let conclusion = typeql::parse_pattern("$u has name 'Employee'")?.into_statement();
                let mut new_rule = tx.logic().put_rule("Employee".to_string(), condition, conclusion).resolve()?;
                // end::put_rule[]
                // tag::get_rules[]
                let rules = tx.logic().get_rules()?;
                for rule in rules {
                    println!("{}", rule.clone()?.label);
                    println!("{}", rule.clone()?.when.to_string());
                    println!("{}", rule.clone()?.then.to_string());
                }
                // end::get_rules[]
                // tag::delete_rule[]
                let _ = new_rule.delete(&tx).resolve();
                // end::delete_rule[]
            }
        }
    }
    {
        // tag::data-api[]
        let db = databases.get(DB_NAME)?;
        {
            let session = Session::new(db, SessionType::Data)?;
            {
                let tx = session.transaction(TransactionType::Write)?;
                let user_type = tx.concept().get_entity_type("user".to_owned()).resolve()?.unwrap();
                let users = user_type.get_instances(&tx, Transitivity::Transitive)?;
                for user in users {
                    let user = user?;
                    println!("User:");
                    let attributes = user.get_has(&tx, vec![], vec![])?;
                    for attribute in attributes {
                        let attribute = attribute?;
                        let value = match attribute.value {
                            Value::String(value) => value,
                            Value::Long(value) => value.to_string(),
                            Value::Double(value) => value.to_string(),
                            Value::DateTime(value) => value.to_string(),
                            Value::Boolean(value) => value.to_string(),
                        };
                        println!("  {}: {}", attribute.type_.label, value)
                    }
                }
                let new_user =
                    tx.concept().get_entity_type("user".to_owned()).resolve()?.unwrap().create(&tx).resolve()?;
                let _ = new_user.delete(&tx).resolve();
            }
        }
        // end::data-api[]
    }

    {
        // tag::explain-get[]
        let db = databases.get(DB_NAME)?;
        let options = Options::new().infer(true).explain(true);
        {
            let session = Session::new(db, SessionType::Data)?;
            {
                let tx = session.transaction_with_options(TransactionType::Read, options)?;
                let get_query = "
                                match
                                $u isa user, has email $e, has name $n;
                                $e contains 'Alice';
                                get
                                $u, $n;
                                ";
                let response = tx.query().get(get_query)?;
                for (i, cmap) in response.enumerate() {
                    let ncmap = cmap.clone();
                    let name_concept = ncmap?.get("n").unwrap().clone();
                    let name = match name_concept {
                        Concept::Attribute(Attribute { value: Value::String(value), .. }) => value,
                        _ => unreachable!(),
                    };
                    println!("Name #{}: {}", (i + 1).to_string(), name);
                    let explainable_relations = cmap?.explainables.relations;
                    for (var, explainable) in explainable_relations {
                        println!("{}", var);
                        println!("{}", explainable.conjunction);
                        let explain_iterator = tx.query().explain(&explainable)?;
                        for explanation in explain_iterator {
                            let exp = explanation?;
                            println!("Rule: {}", exp.rule.label);
                            println!("Condition: {}", exp.rule.when.to_string());
                            println!("Conclusion: {}", exp.rule.then.to_string());
                            println!("Variable mapping:");
                            for qvar in exp.variable_mapping.keys() {
                                println!(
                                    "Query variable {} maps to the rule variable {}",
                                    *qvar,
                                    exp.variable_mapping.get(qvar).unwrap().concat().to_string()
                                );
                            }
                        }
                    }
                }
            }
        }
        // end::explain-get[]
    }

    {
        let db = databases.get(DB_NAME)?;
        let options = Options::new().infer(true).explain(true);
        {
            let session = Session::new(db, SessionType::Data)?;
            {
                let tx = session.transaction_with_options(TransactionType::Read, options)?;
                let get_query = "
                                match
                                $u isa user, has email $e, has name $n;
                                $e contains 'Alice';
                                get
                                $u, $n;
                                ";
                // tag::explainables[]
                let response = tx.query().get(get_query)?;
                for (i, cmap) in response.enumerate() {
                    let explainable_relations = cmap.clone()?.explainables.relations;
                    // end::explainables[]
                    let ncmap = cmap.clone()?;
                    let name_concept = ncmap.get("n").unwrap().clone();
                    let name = match name_concept {
                        Concept::Attribute(Attribute { value: Value::String(value), .. }) => value,
                        _ => unreachable!(),
                    };
                    println!("Name #{}: {}", (i + 1).to_string(), name);

                    // tag::explain[]
                    for (var, explainable) in explainable_relations {
                        // end::explain[]
                        println!("{}", var);
                        println!("{}", explainable.conjunction);
                        // tag::explain[]
                        let explain_iterator = tx.query().explain(&explainable)?;
                        // end::explain[]
                        // tag::explanation[]
                        for explanation in explain_iterator {
                            let exp = explanation?;
                            println!("Rule: {}", exp.rule.label);
                            println!("Condition: {}", exp.rule.when.to_string());
                            println!("Conclusion: {}", exp.rule.then.to_string());
                            println!("Variable mapping:");
                            for qvar in exp.variable_mapping.keys() {
                                println!(
                                    "Query variable {} maps to the rule variable {}",
                                    *qvar,
                                    exp.variable_mapping.get(qvar).unwrap().concat().to_string()
                                );
                            }
                        }
                        // end::explanation[]
                        // tag::explain[]
                    }
                    // end::explain[]
                // tag::explainables[]
                }
                // end::explainables[]
            }
        }
    }
    Ok({})
}
