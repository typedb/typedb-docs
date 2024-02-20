// tag::import[]
#include <iostream>
#include <typedb_driver.hpp>
// end::import[]
int main() {
    std::string dbName = "manual";
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
        // tag::delete-db[]
        if (driver.databases.contains(dbName)) {
            driver.databases.get(dbName).deleteDatabase();
        }
        // end::delete-db[]
        // tag::create-db[]
        driver.databases.create(dbName);
        // end::create-db[]
        if (driver.databases.contains(dbName)) {
            std::cout << "Database setup complete." << std::endl;
        }
    }
    catch (TypeDB::DriverException e ) {
        std::cout << "Caught TypeDB::DriverException: " << e.code() << "\n" << e.message()  << std::endl;
        return 2;
    }

    {   // tag::define[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
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
            txn.query.define(defineQuery).get();
            txn.commit();
        }
        // end::define[]
    }

    {   // tag::undefine[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string undefineQuery = "undefine admin sub user;";
            txn.query.undefine(undefineQuery).get();
            txn.commit();
        }
        // end::undefine[]
    }

    {   // tag::insert[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string insertQuery = R"(
                                    insert
                                    $user1 isa user, has name "Alice", has email "alice@vaticle.com";
                                    $user2 isa user, has name "Bob", has email "bob@vaticle.com";
                                    $friendship (friend:$user1, friend: $user2) isa friendship;
                                    )";
            TypeDB::ConceptMapIterable result = txn.query.insert(insertQuery);
            txn.commit();
        }
        // end::insert[]
    }

    {   // tag::match-insert[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string matchInsertQuery = R"(
                                            match
                                            $u isa user, has name "Bob";
                                            insert
                                            $new-u isa user, has name "Charlie", has email "charlie@vaticle.com";
                                            $f($u,$new-u) isa friendship;
                                            )";
            TypeDB::ConceptMapIterable result = txn.query.insert(matchInsertQuery);
            int16_t i = 0;
            for (TypeDB::ConceptMap& element : result) { i+=1; }
            if (i == 1) {
                txn.commit();
            } else {
                txn.close();
            }
        }
        // end::match-insert[]
    }

    {   // tag::delete[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string deleteQuery = R"(
                                        match
                                        $u isa user, has name "Charlie";
                                        $f ($u) isa friendship;
                                        delete
                                        $f isa friendship;
                                        )";
            txn.query.matchDelete(deleteQuery).get();
            txn.commit();
        }
        // end::delete[]
    }

    {   // tag::update[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string updateQuery = R"(
                                        match
                                        $u isa user, has name "Charlie", has email $e;
                                        delete
                                        $u has $e;
                                        insert
                                        $u has email "charles@vaticle.com";
                                        )";
            TypeDB::ConceptMapIterable result = txn.query.update(updateQuery);
            int16_t i = 0;
            for (TypeDB::ConceptMap& element : result) { i+=1; }
            if (i == 1) {
                txn.commit();
            } else {
                txn.close();
            }
        }
        // end::update[]
    }

    {   // tag::fetch[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::READ, options);
            std::string fetchQuery = R"(
                                        match
                                        $u isa user;
                                        fetch
                                        $u: name, email;
                                        )";
            TypeDB::JSONIterable results = txn.query.fetch(fetchQuery);
            std::vector<TypeDB::JSON> fetchResult;
            for (TypeDB::JSON& result : results) {
                fetchResult.push_back(result);
            }
        }
        // end::fetch[]
    }

    {   // tag::get[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::READ, options);
            std::string getQuery = R"(
                                    match
                                    $u isa user, has email $e;
                                    get
                                    $e;
                                    )";
            TypeDB::ConceptMapIterable result = txn.query.get(getQuery);
            int16_t i = 0;
            for (TypeDB::ConceptMap& cm : result) {
                i += 1;
                std::cout << "Email #" << std::to_string(i) << ": " << cm.get("e")->asAttribute()->getValue()->asString() << std::endl;
            }
        }
        // end::get[]
    }

    {   // tag::infer-rule[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string defineQuery = R"(
                                        define
                                        rule users:
                                        when {
                                            $u isa user;
                                        } then {
                                            $u has name "User";
                                        };
                                        )";
            txn.query.define(defineQuery).get();
            txn.commit();
        }
        // end::infer-rule[]
        // tag::infer-fetch[]
        TypeDB::Options inferOptions;
        inferOptions.infer(true);
        TypeDB::Session session2 = driver.session(dbName, TypeDB::SessionType::DATA, inferOptions);
        {
            TypeDB::Transaction txn2 = session.transaction(TypeDB::TransactionType::READ, inferOptions);
            std::string fetchQuery = R"(
                                        match
                                        $u isa user;
                                        fetch
                                        $u: name, email;
                                        )";
            TypeDB::JSONIterable results = txn2.query.fetch(fetchQuery);
            std::vector<TypeDB::JSON> fetchResult;
            for (TypeDB::JSON& result : results) {
                fetchResult.push_back(result);
            }
        }
        // end::infer-fetch[]
    }

    {
        // tag::types-editing[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::unique_ptr<TypeDB::AttributeType> tag = txn.concepts.putAttributeType("tag", TypeDB::ValueType::STRING).get();
            TypeDB::ConceptIterable<TypeDB::EntityType> entities = txn.concepts.getRootEntityType().get()->getSubtypes(txn);
            for (std::unique_ptr<TypeDB::EntityType>& entity : entities) {
                std::cout << entity.get()->getLabel() << std::endl;
                if (!(entity.get()->isAbstract())) {
                    (void) entity.get()->setOwns(txn, tag.get());
                };
            }
            txn.commit();
        }
        // end::types-editing[]
    }

    {
        // tag::types-api[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::unique_ptr<TypeDB::EntityType> user = txn.concepts.getEntityType("user").get();
            std::unique_ptr<TypeDB::EntityType> admin = txn.concepts.putEntityType("admin").get();
            admin.get()->setSupertype(txn, user.get()).wait();
            TypeDB::ConceptIterable<TypeDB::EntityType> entities = txn.concepts.getRootEntityType().get()->getSubtypes(txn, TypeDB::Transitivity::TRANSITIVE);
            for (std::unique_ptr<TypeDB::EntityType>& entity : entities) {
                std::cout << entity.get()->getLabel() << std::endl;
            }
            txn.commit();
        }
        // end::types-api[]
    }

    {
        // tag::rules-api[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            TypeDB::RuleIterable rules = txn.logic.getRules();
            for (TypeDB::Rule& rule : rules) {
                std::cout << rule.label() << std::endl;
                std::cout << rule.when() << std::endl;
                std::cout << rule.then() << std::endl;
            }
            TypeDB::Rule newRule = txn.logic.putRule("Employee", "{$u isa user, has email $e; $e contains '@vaticle.com';}","$u has name 'Employee'").get();
            std::cout << txn.logic.getRule("Employee").get().value().label() << std::endl;
            newRule.deleteRule(txn).get();
            txn.commit();
        }
        // end::rules-api[]
    }

    {
        // tag::data-api[]
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::unique_ptr<TypeDB::EntityType> userType = txn.concepts.getEntityType("user").get();
            TypeDB::ConceptIterable<TypeDB::Entity> users = userType -> getInstances(txn);
            for (std::unique_ptr<TypeDB::Entity>& user : users) {
                TypeDB::ConceptIterable<TypeDB::Attribute> attributes = user.get()->getHas(txn);
                std::cout << "User: " << std::endl;
                for (std::unique_ptr<TypeDB::Attribute>& attribute : attributes) {
                    std::cout << "  " << attribute.get()->getType().get()->getLabel() << ": " << attribute.get()->getValue().get()->asString() << std::endl;
                }
            }
            std::unique_ptr<TypeDB::Entity> newUser = txn.concepts.getEntityType("user").get().get()->create(txn).get();
            newUser.get()->deleteThing(txn).get();
            txn.commit();
        }
        // end::data-api[]
    }

    {
        // tag::explain-get[]
        TypeDB::Options inferOptions;
        inferOptions.infer(true);
        inferOptions.explain(true);
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, inferOptions);
        {
            TypeDB::Transaction txn = session.transaction(TypeDB::TransactionType::READ, inferOptions);
            std::string getQuery = R"(
                                    match
                                    $u isa user, has email $e, has name $n;
                                    $e contains 'Alice';
                                    get
                                    $u, $n;
                                    )";
            TypeDB::ConceptMapIterable results = txn.query.get(getQuery);
            int16_t i = 0;
            for (TypeDB::ConceptMap& cm : results) {
                i += 1;
                std::cout << "Name #" << std::to_string(i) << ": " << cm.get("n")->asAttribute()->getValue()->asString() << std::endl;
                TypeDB::StringIterable explainableRelations = cm.explainables().relations();
                for (std::string& explainable : explainableRelations) {
                    std::cout << "Explained variable " << explainable << std::endl;
                    std::cout << "Explainable part of the query " << cm.explainables().relation(explainable).conjunction() << std::endl;
                    TypeDB::ExplanationIterable explainIterator = txn.query.explain(cm.explainables().relation(explainable));
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
    return 0;
}
