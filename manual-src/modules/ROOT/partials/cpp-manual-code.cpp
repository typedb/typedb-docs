#include <iostream>
#include <typedb_driver.hpp>

int main() {
    std::string dbName = "test_cpp";
    std::string serverAddress = "127.0.0.1:1729";
    TypeDB::Options options;

    TypeDB::Driver driver = TypeDB::Driver::coreDriver("127.0.0.1:1729");

    try {
        auto dbs = driver.databases.all();
        for (TypeDB::Database& db : dbs) {
            std::cout << db.name() << std::endl;
        };
        if (driver.databases.contains(dbName)) {
            driver.databases.get(dbName).deleteDatabase();
        }
        driver.databases.create(dbName);
        if (driver.databases.contains(dbName)) {
            std::cout << "Database setup complete." << std::endl;
        }
    }
    catch (TypeDB::DriverException e ) {
        std::cout << "Caught TypeDB::DriverException: " << e.code() << "\n" << e.message()  << std::endl;
        return 2;
    }

    {
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
    }

    {
        auto session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        auto transaction = session.transaction(TypeDB::TransactionType::WRITE, options);
        std::string undefineQuery = "undefine admin sub user;";
        auto result = transaction.query.undefine(undefineQuery);
        transaction.commit();
    }

    {
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
    }

    {
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
    }

    {
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
    }

    {
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
    }

    {
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
    }

    {
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
    }

    {
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
    }
    return 0;
}
