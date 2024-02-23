# tag::import[]
from typedb.driver import TypeDB, SessionType, TransactionType, TypeDBOptions, ValueType, Transitivity, TypeDBCredential

# end::import[]
DB_NAME = "manual_db"
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
    # tag::connect_core[]
    driver = TypeDB.core_driver("127.0.0.1:1729")
    # end::connect_core[]
    try:
        # tag::connect_cloud[]
        driver = TypeDB.cloud_driver("127.0.0.1:1729", TypeDBCredential("admin", "password", tls_enabled=True))
        # end::connect_cloud[]
    except:
        pass
    # tag::session_open[]
    session = driver.session(DB_NAME, SessionType.SCHEMA)
    # end::session_open[]
    # tag::tx_open[]
    tx = session.transaction(TransactionType.WRITE)
    # end::tx_open[]
    # tag::tx_close[]
    tx.close()
    # end::tx_close[]
    if tx.is_open():
        # tag::tx_commit[]
        tx.commit()
        # end::tx_commit[]
    # tag::session_close[]
    session.close()
    # end::session_close[]
    # tag::define[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
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
            tx.query.define(define_query).resolve()
            tx.commit()
    # end::define[]
    # tag::undefine[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            undefine_query = "undefine admin sub user;"
            tx.query.undefine(undefine_query).resolve()
            tx.commit()
    # end::undefine[]
    # tag::insert[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            insert_query = """
                            insert
                            $user1 isa user, has name "Alice", has email "alice@vaticle.com";
                            $user2 isa user, has name "Bob", has email "bob@vaticle.com";
                            $friendship (friend:$user1, friend: $user2) isa friendship;
                            """
            response = list(tx.query.insert(insert_query))
            tx.commit()
    # end::insert[]
    # tag::match-insert[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            match_insert_query = """
                                    match
                                    $u isa user, has name "Bob";
                                    insert
                                    $new-u isa user, has name "Charlie", has email "charlie@vaticle.com";
                                    $f($u,$new-u) isa friendship;
                                    """
            response = list(tx.query.insert(match_insert_query))
            if len(response) == 1:
                tx.commit()
            else:
                tx.close()
    # end::match-insert[]
    # tag::delete[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            delete_query = """
                            match
                            $u isa user, has name "Charlie";
                            $f ($u) isa friendship;
                            delete
                            $f isa friendship;
                            """
            response = tx.query.delete(delete_query).resolve()
            tx.commit()
    # end::delete[]
    # tag::update[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            update_query = """
                            match
                            $u isa user, has name "Charlie", has email $e;
                            delete
                            $u has $e;
                            insert
                            $u has email "charles@vaticle.com";
                            """
            response = list(tx.query.update(update_query))
            if len(response) == 1:
                tx.commit()
            else:
                tx.close()
    # end::update[]
    # tag::fetch[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as tx:
            fetch_query = """
                            match
                            $u isa user;
                            fetch
                            $u: name, email;
                            """
            response = tx.query.fetch(fetch_query)
            for i, JSON in enumerate(response):
                print(f"User #{i + 1}: {JSON}")
    # end::fetch[]
    # tag::get[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ) as tx:
            get_query = """
                        match
                        $u isa user, has email $e;
                        get
                        $e;
                        """
            response = tx.query.get(get_query)
            for i, concept_map in enumerate(response):
                email = concept_map.get("e").as_attribute().get_value()
                print(f"Email #{i + 1}: {email}")
    # end::get[]
    # tag::infer-rule[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            define_query = """
                            define
                            rule users:
                            when {
                                $u isa user;
                            } then {
                                $u has name "User";
                            };
                            """
            tx.query.define(define_query)
            tx.commit()
    # end::infer-rule[]
    # tag::infer-fetch[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ, TypeDBOptions(infer=True)) as tx:
            fetch_query = """
                            match
                            $u isa user;
                            fetch
                            $u: name, email;
                            """
            response = tx.query.fetch(fetch_query)
            for i, JSON in enumerate(response):
                print(f"User #{i + 1}: {JSON}")
    # end::infer-fetch[]
    # tag::types-editing[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            tag = tx.concepts.put_attribute_type("tag", ValueType.STRING).resolve()
            entities = tx.concepts.get_root_entity_type().get_subtypes(tx, Transitivity.EXPLICIT)
            for entity in entities:
                print(entity.get_label())
                if not entity.is_abstract():
                    entity.set_owns(tx, tag).resolve()
            tx.commit()
    # end::types-editing[]
    # tag::types-api[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            user = tx.concepts.get_entity_type("user").resolve()
            admin = tx.concepts.put_entity_type("admin").resolve()
            admin.set_supertype(tx, user)
            root_entity = tx.concepts.get_root_entity_type()
            subtypes = list(root_entity.get_subtypes(tx, Transitivity.TRANSITIVE))
            for subtype in subtypes:
                print(subtype.get_label().name)
            tx.commit()
    # end::types-api[]

    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            # tag::get_type[]
            user = tx.concepts.get_entity_type("user").resolve()
            # end::get_type[]
            # tag::add_type[]
            admin = tx.concepts.put_entity_type("admin").resolve()
            # end::add_type[]
            # tag::set_supertype[]
            admin.set_supertype(tx, user)
            # end::set_supertype[]
            # tag::get_instances[]
            users = tx.concepts.get_entity_type("user").resolve().get_instances(tx)
            # end::get_instances[]
            for user in users:
                # tag::get_has[]
                attributes = user.get_has(tx)
                # end::get_has[]
            # tag::create[]
            new_user = tx.concepts.get_entity_type("user").resolve().create(tx).resolve()
            # end::create[]
            # tag::delete_user[]
            new_user.delete(tx)
            # end::delete_user[]
    # tag::rules-api[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            rules = tx.logic.get_rules()
            for rule in rules:
                print("Rule label:", rule.label)
                print("  Condition:", rule.when)
                print("  Conclusion:", rule.then)
            new_rule = tx.logic.put_rule("Employee",
                                         "{$u isa user, has email $e; $e contains '@vaticle.com';}",
                                         "$u has name 'Employee'").resolve()
            print(tx.logic.get_rule("Employee").resolve().label)
            new_rule.delete(tx).resolve()
            tx.commit()
    # end::rules-api[]
    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            # tag::get_rules[]
            rules = tx.logic.get_rules()
            for rule in rules:
                print("Rule label:", rule.label)
                print("  Condition:", rule.when)
                print("  Conclusion:", rule.then)
            # end::get_rules[]
            # tag::put_rule[]
            new_rule = tx.logic.put_rule("Employee",
                                         "{$u isa user, has email $e; $e contains '@vaticle.com';}",
                                         "$u has name 'Employee'").resolve()
            # end::put_rule[]
            # tag::get_rule[]
            rule = tx.logic.get_rule("Employee").resolve()
            # end::get_rule[]
            print(rule.label)
            # tag::delete_rule[]
            new_rule.delete(tx).resolve()
            # end::delete_rule[]
    # tag::data-api[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            user_type = tx.concepts.get_entity_type("user").resolve()
            users = user_type.get_instances(tx)
            for user in users:
                attributes = user.get_has(tx)
                print("User:")
                for attribute in attributes:
                    print(f"  {attribute.get_type().get_label().name} : {attribute.get_value()}")
            new_user = tx.concepts.get_entity_type("user").resolve().create(tx).resolve()
            new_user.delete(tx)
            tx.commit()
    # end::data-api[]
    # tag::explain-get[]
    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ, TypeDBOptions(infer=True, explain=True)) as tx:
            get_query = """
                        match
                        $u isa user, has email $e, has name $n;
                        $e contains 'alice';
                        get
                        $u, $n;
                        """
            response = tx.query.get(get_query)
            for i, ConceptMap in enumerate(response):
                name = ConceptMap.get("n").as_attribute().get_value()
                print(f"Name #{i + 1}: {name}")
                explainable_relations = ConceptMap.explainables().relations()
                for var, explainable in explainable_relations:
                    print("Explained variable:", explainable)
                    print("Explainable object:", explainable_relations[explainable])  # ???
                    print("Explainable part of query:", explainable_relations[explainable].conjunction())
                    explain_iterator = tx.query.explain(explainable)
                    for explanation in explain_iterator:
                        print("\nRule: ", explanation.rule().label)
                        print("Condition: ", explanation.condition())
                        print("Conclusion: ", explanation.conclusion())
                        print("Variable mapping: ")
                        for qvar in explanation.query_variables():
                            print(
                                f"  Query variable {qvar} maps to the rule variable {explanation.query_variable_mapping(var)}")
                        print("----------------------------------------------------------")
    # end::explain-get[]

    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.READ, TypeDBOptions(infer=True, explain=True)) as tx:
            get_query = """
                        match
                        $u isa user, has email $e, has name $n;
                        $e contains 'alice';
                        get
                        $u, $n;
                        """
            # tag::explainables[]
            response = tx.query.get(get_query)
            for i, ConceptMap in enumerate(response):
                explainable_relations = ConceptMap.explainables().relations()
            # end::explainables[]
                name = ConceptMap.get("n").as_attribute().get_value()
                print(f"Name #{i + 1}: {name}")
                # tag::explain[]
                for var, explainable in explainable_relations:
                    explain_iterator = tx.query.explain(explainable)
                # end::explain[]
                    print("Explained variable:", explainable)
                    print("Explainable object:", explainable_relations[explainable])
                    print("Explainable part of query:", explainable_relations[explainable].conjunction())
                    # tag::explanation[]
                    for explanation in explain_iterator:
                        print("\nRule: ", explanation.rule().label)
                        print("Condition: ", explanation.condition())
                        print("Conclusion: ", explanation.conclusion())
                        print("Variable mapping: ")
                        for qvar in explanation.query_variables():
                            print(
                                f"  Query variable {qvar} maps to the rule variable {explanation.query_variable_mapping(var)}")
                    # end::explanation[]
                        print("----------------------------------------------------------")
