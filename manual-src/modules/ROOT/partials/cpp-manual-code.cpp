// tag::import[]
#include <iostream>
#include <typedb_driver.hpp>
// end::import[]
int main() {
    std::string DB_NAME = "manual_db";
    // tag::options[]
    TypeDB::Options options;
    // end::options[]
    // tag::driver[]
    TypeDB::Driver driver = TypeDB::Driver::coreDriver("127.0.0.1:1729");
    // end::driver[]
    try {
        // tag::list-db[]
        for (TypeDB::Database& db: driver.databases.all()) {
            std::cout << db.name() << std::endl;
        }
        // end::list-db[]
        if (driver.databases.contains(DB_NAME)) {
            // tag::delete-db[]
            driver.databases.get(DB_NAME).deleteDatabase();
            // end::delete-db[]
        }
        // tag::create-db[]
        driver.databases.create(DB_NAME);
        // end::create-db[]
        if (driver.databases.contains(DB_NAME)) {
            std::cout << "Database setup complete." << std::endl;
        }
    }
    catch (TypeDB::DriverException e ) {
        std::cout << "Caught TypeDB::DriverException: " << e.code() << "\n" << e.message()  << std::endl;
        return 2;
    }

    {
    // tag::connect_core[]
    TypeDB::Driver driver = TypeDB::Driver::coreDriver("127.0.0.1:1729");
    // end::connect_core[]
    try {
        // tag::connect_cloud[]
        TypeDB::Driver driver = TypeDB::Driver::cloudDriver({"127.0.0.1:1729"}, TypeDB::Credential("admin", "password", true));
        // end::connect_cloud[]
    }
    catch (TypeDB::DriverException e ) {
        //std::cout << "Caught TypeDB::DriverException: " << e.code() << "\n" << e.message()  << std::endl;
        //return 2;
    }
    // tag::session_open[]
    TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::SCHEMA, options);
    // end::session_open[]
    // tag::tx_open[]
    TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
    // end::tx_open[]
    // tag::tx_close[]
    tx.close();
    // end::tx_close[]
    if (tx.isOpen()) {
        // tag::tx_commit[]
        tx.commit();
        // end::tx_commit[]
    };
    // tag::session_close[]
    session.close();
    // end::session_close[]
    }

    {   // tag::define[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string defineQuery = R"(
                                define
                                email sub attribute, value string;
                                name sub attribute, value string;
                                friendship sub relation, relates friend;
                                user sub entity,
                                    owns email @key,
                                    owns name,
                                    plays friendship:friend;
                                admin sub user;
                                )";
            tx.query.define(defineQuery).get();
            tx.commit();
        }
        // end::define[]
    }

    {   // tag::undefine[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string undefineQuery = "undefine admin sub user;";
            tx.query.undefine(undefineQuery).get();
            tx.commit();
        }
        // end::undefine[]
    }

    {   // tag::insert[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string insertQuery = R"(
                                    insert
                                    $user1 isa user, has name "Alice", has email "alice@typedb.com";
                                    $user2 isa user, has name "Bob", has email "bob@typedb.com";
                                    $friendship (friend:$user1, friend: $user2) isa friendship;
                                    )";
            TypeDB::ConceptMapIterable result = tx.query.insert(insertQuery);
            tx.commit();
        }
        // end::insert[]
    }

    {   // tag::match-insert[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string matchInsertQuery = R"(
                                            match
                                            $u isa user, has name "Bob";
                                            insert
                                            $new-u isa user, has name "Charlie", has email "charlie@typedb.com";
                                            $f($u,$new-u) isa friendship;
                                            )";
            TypeDB::ConceptMapIterable result = tx.query.insert(matchInsertQuery);
            int16_t i = 0;
            for (TypeDB::ConceptMap& element : result) { i+=1; }
            if (i == 1) {
                tx.commit();
            } else {
                tx.close();
            }
        }
        // end::match-insert[]
    }

    {   // tag::delete[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string deleteQuery = R"(
                                        match
                                        $u isa user, has name "Charlie";
                                        $f ($u) isa friendship;
                                        delete
                                        $f isa friendship;
                                        )";
            tx.query.matchDelete(deleteQuery).get();
            tx.commit();
        }
        // end::delete[]
    }

    {   // tag::update[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string updateQuery = R"(
                                        match
                                        $u isa user, has name "Charlie", has email $e;
                                        delete
                                        $u has $e;
                                        insert
                                        $u has email "charles@typedb.com";
                                        )";
            TypeDB::ConceptMapIterable result = tx.query.update(updateQuery);
            int16_t i = 0;
            for (TypeDB::ConceptMap& element : result) { i+=1; }
            if (i == 1) {
                tx.commit();
            } else {
                tx.close();
            }
        }
        // end::update[]
    }

    {   // tag::fetch[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::READ, options);
            std::string fetchQuery = R"(
                                        match
                                        $u isa user;
                                        fetch
                                        $u: name, email;
                                        )";
            TypeDB::JSONIterable results = tx.query.fetch(fetchQuery);
            std::vector<TypeDB::JSON> fetchResult;
            for (TypeDB::JSON& result : results) {
                fetchResult.push_back(result);
            }
        }
        // end::fetch[]
    }

    {   // tag::get[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::READ, options);
            std::string getQuery = R"(
                                    match
                                    $u isa user, has email $e;
                                    get
                                    $e;
                                    )";
            TypeDB::ConceptMapIterable result = tx.query.get(getQuery);
            int16_t i = 0;
            for (TypeDB::ConceptMap& cm : result) {
                i += 1;
                std::cout << "Email #" << std::to_string(i) << ": " << cm.get("e")->asAttribute()->getValue()->asString() << std::endl;
            }
        }
        // end::get[]
    }

    {   // tag::infer-rule[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string defineQuery = R"(
                                        define
                                        rule users:
                                        when {
                                            $u isa user;
                                        } then {
                                            $u has name "User";
                                        };
                                        )";
            tx.query.define(defineQuery).get();
            tx.commit();
        }
        // end::infer-rule[]
        // tag::infer-fetch[]
        TypeDB::Options inferOptions;
        inferOptions.infer(true);
        TypeDB::Session session2 = driver.session(DB_NAME, TypeDB::SessionType::DATA, inferOptions);
        {
            TypeDB::Transaction tx2 = session.transaction(TypeDB::TransactionType::READ, inferOptions);
            std::string fetchQuery = R"(
                                        match
                                        $u isa user;
                                        fetch
                                        $u: name, email;
                                        )";
            TypeDB::JSONIterable results = tx2.query.fetch(fetchQuery);
            std::vector<TypeDB::JSON> fetchResult;
            for (TypeDB::JSON& result : results) {
                fetchResult.push_back(result);
            }
        }
        // end::infer-fetch[]
    }

    {
        // tag::types-editing[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::unique_ptr<TypeDB::AttributeType> tag = tx.concepts.putAttributeType("tag", TypeDB::ValueType::STRING).get();
            TypeDB::ConceptIterable<TypeDB::EntityType> entities = tx.concepts.getRootEntityType().get()->getSubtypes(tx);
            for (std::unique_ptr<TypeDB::EntityType>& entity : entities) {
                std::cout << entity.get()->getLabel() << std::endl;
                if (!(entity.get()->isAbstract())) {
                    (void) entity.get()->setOwns(tx, tag.get());
                };
            }
            tx.commit();
        }
        // end::types-editing[]
    }

    {
        // tag::types-api[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::unique_ptr<TypeDB::EntityType> userType = tx.concepts.getEntityType("user").get();
            std::unique_ptr<TypeDB::EntityType> adminType = tx.concepts.putEntityType("admin").get();
            adminType.get()->setSupertype(tx, userType.get()).wait();
            TypeDB::ConceptIterable<TypeDB::EntityType> entities = tx.concepts.getRootEntityType().get()->getSubtypes(tx, TypeDB::Transitivity::TRANSITIVE);
            for (std::unique_ptr<TypeDB::EntityType>& entity : entities) {
                std::cout << entity.get()->getLabel() << std::endl;
            }
            tx.commit();
        }
        // end::types-api[]
    }

    {
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            // tag::get_type[]
            std::unique_ptr<TypeDB::EntityType> userType = tx.concepts.getEntityType("user").get();
            // end::get_type[]
            // tag::add_type[]
            std::unique_ptr<TypeDB::EntityType> adminType = tx.concepts.putEntityType("admin").get();
            // end::add_type[]
            // tag::set_supertype[]
            adminType.get()->setSupertype(tx, userType.get()).wait();
            // end::set_supertype[]
            // tag::get_instances[]
            TypeDB::ConceptIterable<TypeDB::Entity> users = userType -> getInstances(tx);
            // end::get_instances[]
            for (std::unique_ptr<TypeDB::Entity>& user : users) {
                // tag::get_has[]
                TypeDB::ConceptIterable<TypeDB::Attribute> attributes = user.get()->getHas(tx);
                // end::get_has[]
                std::cout << "User: " << std::endl;
                for (std::unique_ptr<TypeDB::Attribute>& attribute : attributes) {
                    std::cout << "  " << attribute.get()->getType().get()->getLabel() << ": " << attribute.get()->getValue().get()->asString() << std::endl;
                }
            }
            // tag::create[]
            std::unique_ptr<TypeDB::Entity> newUser = tx.concepts.getEntityType("user").get().get()->create(tx).get();
            // end::create[]
            // tag::delete_user[]
            newUser.get()->deleteThing(tx).get();
            // end::delete_user[]
        }
    }

    {
        // tag::rules-api[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            TypeDB::RuleIterable rules = tx.logic.getRules();
            for (TypeDB::Rule& rule : rules) {
                std::cout << rule.label() << std::endl;
                std::cout << rule.when() << std::endl;
                std::cout << rule.then() << std::endl;
            }
            TypeDB::Rule newRule = tx.logic.putRule("Employee", "{$u isa user, has email $e; $e contains '@typedb.com';}","$u has name 'Employee'").get();
            TypeDB::Rule oldRule = tx.logic.getRule("users").get().value();
            std::cout << oldRule.label() << std::endl;
            newRule.deleteRule(tx).get();
            tx.commit();
        }
        // end::rules-api[]
    }

    {
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            // tag::get_rules[]
            TypeDB::RuleIterable rules = tx.logic.getRules();
            for (TypeDB::Rule& rule : rules) {
                std::cout << rule.label() << std::endl;
                std::cout << rule.when() << std::endl;
                std::cout << rule.then() << std::endl;
            }
            // end::get_rules[]
            // tag::put_rule[]
            TypeDB::Rule newRule = tx.logic.putRule("Employee", "{$u isa user, has email $e; $e contains '@typedb.com';}","$u has name 'Employee'").get();
            // end::put_rule[]
            // tag::get_rule[]
            TypeDB::Rule oldRule = tx.logic.getRule("users").get().value();
            // end::get_rule[]
            std::cout << oldRule.label() << std::endl;
            // tag::delete_rule[]
            newRule.deleteRule(tx).get();
            // end::delete_rule[]
        }
    }

    {
        // tag::data-api[]
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::unique_ptr<TypeDB::EntityType> userType = tx.concepts.getEntityType("user").get();
            TypeDB::ConceptIterable<TypeDB::Entity> users = userType -> getInstances(tx);
            for (std::unique_ptr<TypeDB::Entity>& user : users) {
                TypeDB::ConceptIterable<TypeDB::Attribute> attributes = user.get()->getHas(tx);
                std::cout << "User: " << std::endl;
                for (std::unique_ptr<TypeDB::Attribute>& attribute : attributes) {
                    std::cout << "  " << attribute.get()->getType().get()->getLabel() << ": " << attribute.get()->getValue().get()->asString() << std::endl;
                }
            }
            std::unique_ptr<TypeDB::Entity> newUser = tx.concepts.getEntityType("user").get().get()->create(tx).get();
            newUser.get()->deleteThing(tx).get();
            tx.commit();
        }
        // end::data-api[]
    }

    {
        // tag::explain-get[]
        TypeDB::Options inferOptions;
        inferOptions.infer(true);
        inferOptions.explain(true);
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::DATA, inferOptions);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::READ, inferOptions);
            std::string getQuery = R"(
                                    match
                                    $u isa user, has email $e, has name $n;
                                    $e contains 'Alice';
                                    get
                                    $u, $n;
                                    )";
            TypeDB::ConceptMapIterable results = tx.query.get(getQuery);
            int16_t i = 0;
            for (TypeDB::ConceptMap& cm : results) {
                i += 1;
                std::cout << "Name #" << std::to_string(i) << ": " << cm.get("n")->asAttribute()->getValue()->asString() << std::endl;
                TypeDB::StringIterable explainableRelations = cm.explainables().relations();
                for (std::string& explainable : explainableRelations) {
                    std::cout << "Explained variable " << explainable << std::endl;
                    std::cout << "Explainable part of the query " << cm.explainables().relation(explainable).conjunction() << std::endl;
                    TypeDB::ExplanationIterable explainIterator = tx.query.explain(cm.explainables().relation(explainable));
                    for (TypeDB::Explanation& explanation : explainIterator) {
                        std::cout << "Rule: " << explanation.rule().label() << std::endl;
                        std::cout << "Condition: " << explanation.rule().when() << std::endl;
                        std::cout << "Conclusion: " << explanation.rule().then() << std::endl;
                        std::cout << "Variable mapping: " << std::endl;
                        for (std::string& var : explanation.queryVariables()) {
                            std::cout << "Query variable " << var << " maps to the rule variable " << explanation.queryVariableMapping(var)[1] << std::endl;
                        }
                    }
                }
            }
        }
        // end::explain-get[]
    }

    {
        TypeDB::Options inferOptions;
        inferOptions.infer(true);
        inferOptions.explain(true);
        TypeDB::Session session = driver.session(DB_NAME, TypeDB::SessionType::DATA, inferOptions);
        {
            TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::READ, inferOptions);
            std::string getQuery = R"(
                                    match
                                    $u isa user, has email $e, has name $n;
                                    $e contains 'Alice';
                                    get
                                    $u, $n;
                                    )";
            // tag::explainables[]
            TypeDB::ConceptMapIterable results = tx.query.get(getQuery);
            // end::explainables[]
            int16_t i = 0;
            // tag::explainables[]
            for (TypeDB::ConceptMap& cm : results) {
            // end::explainables[]
                i += 1;
                std::cout << "Name #" << std::to_string(i) << ": " << cm.get("n")->asAttribute()->getValue()->asString() << std::endl;
                // tag::explainables[]
                TypeDB::StringIterable explainableRelations = cm.explainables().relations();
                // end::explainables[]
                // tag::explain[]
                for (std::string& explainable : explainableRelations) {
                    TypeDB::ExplanationIterable explainIterator = tx.query.explain(cm.explainables().relation(explainable));
                // end::explain[]
                    std::cout << "Explained variable " << explainable << std::endl;
                    std::cout << "Explainable part of the query " << cm.explainables().relation(explainable).conjunction() << std::endl;
                    // tag::explanation[]
                    for (TypeDB::Explanation& explanation : explainIterator) {
                        std::cout << "Rule: " << explanation.rule().label() << std::endl;
                        std::cout << "Condition: " << explanation.rule().when() << std::endl;
                        std::cout << "Conclusion: " << explanation.rule().then() << std::endl;
                        std::cout << "Variable mapping: " << std::endl;
                        for (std::string& var : explanation.queryVariables()) {
                            std::cout << "Query variable " << var << " maps to the rule variable " << explanation.queryVariableMapping(var)[1] << std::endl;
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
    return 0;
}
