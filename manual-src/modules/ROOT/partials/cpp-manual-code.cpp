// tag::import[]
#include <iostream>
#include <typedb_driver.hpp>
// end::import[]
int main() {
    std::string dbName = "test_cpp";
    std::string serverAddress = "127.0.0.1:1729";
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
        // end::define[]
    }

    {   // tag::undefine[]
        auto session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
        std::string undefineQuery = "undefine admin sub user;";
        auto result = transaction.query.undefine(undefineQuery);
        transaction.commit();
        // end::undefine[]
    }

    {   // tag::insert[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
        std::string insertQuery = R"(
                                insert
                                $user1 isa user, has name "Alice", has email "alice@vaticle.com";
                                $user2 isa user, has name "Bob", has email "bob@vaticle.com";
                                $friendship (friend:$user1, friend: $user2) isa friendship;
                                )";
        auto result = transaction.query.insert(insertQuery);
        transaction.commit();
        // end::insert[]
    }

    {   // tag::match-insert[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
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
        // end::match-insert[]
    }

    {   // tag::delete[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
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
        // end::delete[]
    }

    {   // tag::update[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
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
        // end::update[]
    }

    {   // tag::fetch[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
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
        // end::fetch[]
    }

    {   // tag::get[]
        auto session = driver.session(dbName, TypeDB::SessionType::DATA, options);
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
        // end::get[]
    }

    {   // tag::infer[]
        auto session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
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

        TypeDB::Options inferOptions;
        inferOptions.infer(true);
        auto session2 = driver.session(dbName, TypeDB::SessionType::DATA, inferOptions);
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
        // end::infer[]
    }
    return 0;
}
