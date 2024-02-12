# tag::import[]
from typedb.driver import TypeDB, SessionType, TransactionType, TypeDBOptions, ValueType, Transitivity

# end::import[]

DB_NAME = "sample_db"

# tag::driver[]
with TypeDB.core_driver("localhost:1729") as driver:
    # end::driver[]

    # tag::list-db[]
    for db in driver.databases.all():
        print(db.name)
    # end::list-db[]
    # tag::delete-db[]
    if driver.databases.contains(DB_NAME):
        driver.databases.get(DB_NAME).delete()
    # end::delete-db[]
    # tag::create-db[]
    driver.databases.create(DB_NAME)
    # end::create-db[]

    assert driver.databases.contains(DB_NAME), "Database creation error."
    print("Database setup complete.")

    # tag::define[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            define_query = """
                            define
                            email sub attribute, value string;
                            name sub attribute, value string;
                            friendship sub relation, relates friend;
                            user sub entity,
                                owns email @key,
                                owns name,
                                plays friendship:friend;
                            admin sub user;
                            """
            response = transaction.query.define(define_query).resolve()
            transaction.commit()
    # end::define[]

    # tag::undefine[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            undefine_query = "undefine admin sub user;"
            response = transaction.query.undefine(undefine_query).resolve()
            transaction.commit()
    # end::undefine[]
    # tag::insert[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            insert_query = """
                            insert
                            $user1 isa user, has name "Alice", has email "alice@vaticle.com";
                            $user2 isa user, has name "Bob", has email "bob@vaticle.com";
                            $friendship (friend:$user1, friend: $user2) isa friendship;
                            """
            response = list(transaction.query.insert(insert_query))
            transaction.commit()
    # end::insert[]
    # tag::match-insert[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            match_insert_query = """
                                    match
                                    $u isa user, has name "Bob";
                                    insert
                                    $new-u isa user, has name "Charlie", has email "charlie@vaticle.com";
                                    $f($u,$new-u) isa friendship;
                                    """
            response = list(transaction.query.insert(match_insert_query))
            if len(response) == 1:
                transaction.commit()
            else:
                transaction.close()
    # end::match-insert[]
    # tag::delete[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            delete_query = """
                            match
                            $u isa user, has name "Charlie";
                            $f ($u) isa friendship;
                            delete
                            $f isa friendship;
                            """
            response = transaction.query.delete(delete_query).resolve()
            transaction.commit()
    # end::delete[]
    # tag::update[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            update_query = """
                            match
                            $u isa user, has name "Charlie", has email $e;
                            delete
                            $u has $e;
                            insert
                            $u has email "charles@vaticle.com";
                            """
            response = list(transaction.query.update(update_query))
            if len(response) == 1:
                transaction.commit()
            else:
                transaction.close()
    # end::update[]
    # tag::fetch[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            fetch_query = """
                            match
                            $u isa user;
                            fetch
                            $u: name, email;
                            """
            response = transaction.query.fetch(fetch_query)
            for i, JSON in enumerate(response):
                print(f"User #{i + 1}: {JSON}")
    # end::fetch[]
    # tag::get[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as transaction:
            get_query = """
                        match
                        $u isa user, has email $e;
                        get
                        $e;
                        """
            response = transaction.query.get(get_query)
            for i, concept_map in enumerate(response):
                email = concept_map.get("e").as_attribute().get_value()
                print(f"Email #{i + 1}: {email}")
    # end::get[]
    # tag::infer-rule[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            define_query = """
                            define
                            rule users:
                            when {
                                $u isa user;
                            } then {
                                $u has name "User";
                            };
                            """
            transaction.query.define(define_query)
            transaction.commit()
    # end::infer-rule[]
    # tag::infer-fetch[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ, TypeDBOptions(infer=True)) as transaction:
            fetch_query = """
                            match
                            $u isa user;
                            fetch
                            $u: name, email;
                            """
            response = transaction.query.fetch(fetch_query)
            for i, JSON in enumerate(response):
                print(f"User #{i + 1}: {JSON}")
    # end::infer-fetch[]
    # tag::types-editing[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            tag = transaction.concepts.put_attribute_type("tag", ValueType.STRING).resolve()
            entities = transaction.concepts.get_root_entity_type().get_subtypes(transaction, Transitivity.EXPLICIT)
            for entity in entities:
                print(entity.get_label())
                if not entity.is_abstract():
                    entity.set_owns(transaction, tag).resolve()
            transaction.commit()
    # end::types-editing[]
    # tag::types-api[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            user = transaction.concepts.get_entity_type("user").resolve()
            admin = transaction.concepts.put_entity_type("admin").resolve()
            admin.set_supertype(transaction, user)
            root_entity = transaction.concepts.get_root_entity_type()
            subtypes = list(root_entity.get_subtypes(transaction, Transitivity.TRANSITIVE))
            for subtype in subtypes:
                print(subtype.get_label().name)
            transaction.commit()

    # end::types-api[]
    # tag::rules-api[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as transaction:
            rules = transaction.logic.get_rules()
            for rule in rules:
                print("Rule label:", rule.label)
                print("  Condition:", rule.when)
                print("  Conclusion:", rule.then)
            new_rule = transaction.logic.put_rule("Employee",
                                                  "{$u isa user, has email $e; $e contains '@vaticle.com';}",
                                                  "$u has name 'Employee'").resolve()
            print("Rules (before deletion):")
            rules = transaction.logic.get_rules()
            for rule in rules:
                print("Rule label:", rule.label)

            new_rule.delete(transaction).resolve()

            print("Rules (after deletion):")
            rules = transaction.logic.get_rules()
            for rule in rules:
                print("Rule label:", rule.label)

            transaction.commit()

    # end::rules-api[]
