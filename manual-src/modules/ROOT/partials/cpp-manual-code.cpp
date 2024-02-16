// tag::import[]
#include <iostream>
#include <typedb_driver.hpp>
// end::import[]
int main() {
    std::string dbName = "test_cpp";
    // tag::options[]
    TypeDB::Options options;
    // end::options[]
    // tag::driver[]
    TypeDB::Driver driver = TypeDB::Driver::coreDriver("127.0.0.1:1729");
    // end::driver[]
    try {
        // tag::list-db[]
        for (auto& db: driver.databases.all()) {
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
        auto session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
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
            auto result = transaction.query.define(defineQuery);
            transaction.commit();
        }
        // end::define[]
    }

    {   // tag::undefine[]
        auto session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string undefineQuery = "undefine admin sub user;";
            auto result = transaction.query.undefine(undefineQuery);
            transaction.commit();
        }
        // end::undefine[]
    }

    {   // tag::insert[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string insertQuery = R"(
                                    insert
                                    $user1 isa user, has name "Alice", has email "alice@vaticle.com";
                                    $user2 isa user, has name "Bob", has email "bob@vaticle.com";
                                    $friendship (friend:$user1, friend: $user2) isa friendship;
                                    )";
            auto result = transaction.query.insert(insertQuery);
            transaction.commit();
        }
        // end::insert[]
    }

    {   // tag::match-insert[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string matchInsertQuery = R"(
                                            match
                                            $u isa user, has name "Bob";
                                            insert
                                            $new-u isa user, has name "Charlie", has email "charlie@vaticle.com";
                                            $f($u,$new-u) isa friendship;
                                            )";
            auto result = transaction.query.insert(matchInsertQuery);
            auto i = 0;
            for (auto& element : result) { i+=1; }
            if (i == 1) {
                transaction.commit();
            } else {
                transaction.close();
            }
        }
        // end::match-insert[]
    }

    {   // tag::delete[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string deleteQuery = R"(
                                        match
                                        $u isa user, has name "Charlie";
                                        $f ($u) isa friendship;
                                        delete
                                        $f isa friendship;
                                        )";
            auto result = transaction.query.matchDelete(deleteQuery);
            transaction.commit();
        }
        // end::delete[]
    }

    {   // tag::update[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string updateQuery = R"(
                                        match
                                        $u isa user, has name "Charlie", has email $e;
                                        delete
                                        $u has $e;
                                        insert
                                        $u has email "charles@vaticle.com";
                                        )";
            auto result = transaction.query.update(updateQuery);
            auto i = 0;
            for (auto& element : result) { i+=1; }
            if (i == 1) {
                transaction.commit();
            } else {
                transaction.close();
            }
        }
        // end::update[]
    }

    {   // tag::fetch[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::READ, options);
            std::string fetchQuery = R"(
                                        match
                                        $u isa user;
                                        fetch
                                        $u: name, email;
                                        )";
            auto results = transaction.query.fetch(fetchQuery);
            std::vector<TypeDB::JSON> fetchResult;
            for (TypeDB::JSON& result : results) {
                fetchResult.push_back(result);
            }
        }
        // end::fetch[]
    }

    {   // tag::get[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::READ, options);
            std::string getQuery = R"(
                                    match
                                    $u isa user, has email $e;
                                    get
                                    $e;
                                    )";
            auto result = transaction.query.get(getQuery);
            auto i = 0;
            for (auto& cm : result) {
                i+=1;
                std::cout << "Email #" << std::to_string(i) << ": " << cm.get("e")->asAttribute()->getValue()->asString() << std::endl;
            }
        }
        // end::get[]
    }

    {   // tag::infer-rule[]
        auto session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            std::string defineQuery = R"(
                                        define
                                        rule users:
                                        when {
                                            $u isa user;
                                        } then {
                                            $u has name "User";
                                        };
                                        )";
            auto result = transaction.query.define(defineQuery);
            transaction.commit();
        }
        // end::infer-rule[]
        // tag::infer-fetch[]
        TypeDB::Options inferOptions;
        inferOptions.infer(true);
        auto session2 = driver.session(dbName, TypeDB::SessionType::DATA, inferOptions);
        {
            auto transaction2 = session.transaction(TypeDB::TransactionType::READ, inferOptions);
            std::string fetchQuery = R"(
                                        match
                                        $u isa user;
                                        fetch
                                        $u: name, email;
                                        )";
            auto results = transaction2.query.fetch(fetchQuery);
            std::vector<TypeDB::JSON> fetchResult;
            for (TypeDB::JSON& result : results) {
                fetchResult.push_back(result);
            }
        }
        // end::infer-fetch[]
    }

    {
        // tag::types-editing[]
        auto session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            auto tag = transaction.concepts.putAttributeType("tag", TypeDB::ValueType::STRING).get();
            auto entities = transaction.concepts.getRootEntityType().get()->getSubtypes(transaction);
            for (auto& entity : entities) {
                std::cout << entity.get()->getLabel() << std::endl;
                if (!(entity.get()->isAbstract())) {
                    (void) entity.get()->setOwns(transaction, tag.get());
                };
            }
            transaction.commit();
        }
        // end::types-editing[]
    }

    {
        // tag::types-api[]
        auto session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            auto user = transaction.concepts.getEntityType("user").get();
            auto admin = transaction.concepts.putEntityType("admin").get();
            (void) admin.get()->setSupertype(transaction, user.get());
            auto entities = transaction.concepts.getRootEntityType().get()->getSubtypes(transaction, TypeDB::Transitivity::TRANSITIVE);
            for (auto& entity : entities) {
                std::cout << entity.get()->getLabel() << std::endl;
            }
            transaction.commit();
        }
        // end::types-api[]
    }

    {
        // tag::rules-api[]
        auto session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            auto rules = transaction.logic.getRules();
            for (auto& rule : rules) {
                std::cout << rule.label() << std::endl;
                std::cout << rule.when() << std::endl;
                std::cout << rule.then() << std::endl;
            }
            auto new_rule = transaction.logic.putRule("Employee", "{$u isa user, has email $e; $e contains '@vaticle.com';}","$u has name 'Employee'");
            std::cout << transaction.logic.getRule("Employee").get().value().label() << std::endl;
            (void) new_rule.get().deleteRule(transaction).get();
            transaction.commit();
        }
        // end::rules-api[]
    }

    {
        // tag::data-api[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
            auto users = transaction.concepts.getEntityType("user").get().get()->getInstances(transaction);
            for (auto& user : users) {
                auto attributes = user.get()->getHas(transaction);
                std::cout << "User: " << std::endl;
                for (auto& attribute : attributes) {
                    std::cout << "  " << attribute.get()->getType().get()->getLabel() << ": " << attribute.get()->getValue().get()->asString() << std::endl;
                }
            }
            auto newUser = transaction.concepts.getEntityType("user").get().get()->create(transaction).get();
            newUser.get()->deleteThing(transaction).get();
            transaction.commit();
        }
        // end::data-api[]
    }

    {
        // tag::explain-get[]
        TypeDB::Options inferOptions;
        inferOptions.infer(true);
        inferOptions.explain(true);
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, inferOptions);
        {
            auto transaction = session.transaction(TypeDB::TransactionType::READ, inferOptions);
            std::string getQuery = R"(
                                    match
                                    $u isa user, has email $e, has name $n;
                                    $e contains 'Alice';
                                    get
                                    $u, $n;
                                    )";
            auto results = transaction.query.get(getQuery);
            auto i = 0;
            for (auto& cm : results) {
                i+=1;
                std::cout << "Name #" << std::to_string(i) << ": " << cm.get("n")->asAttribute()->getValue()->asString() << std::endl;
                auto explainable_relations = cm.explainables().relations();
                for (auto& explainable : explainable_relations) {
                    std::cout << "Explained variable " << explainable << std::endl;
                    std::cout << "Explainable part of the query " << cm.explainables().relation(explainable).conjunction() << std::endl;
                    auto explainIterator = transaction.query.explain(cm.explainables().relation(explainable));
                    for (auto& explanation : explainIterator) {
                        std::cout << "Rule: " << explanation.rule().label() << std::endl;
                        std::cout << "Condition: " << explanation.rule().when() << std::endl;
                        std::cout << "Conclusion: " << explanation.rule().then() << std::endl;
                        std::cout << "Variable mapping: " << std::endl;
                        for (auto& var : explanation.queryVariables()) {
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
