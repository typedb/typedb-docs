// tag::code[]
// tag::import[]
#include <iostream>
#include <fstream>
#include <vector>
#include <typedb_driver.hpp>
// end::import[]
// tag::constants[]
const std::string DB_NAME = "sample_app_db";
const std::string SERVER_ADDR = "127.0.0.1:1729";
enum edition { core, cloud };
edition TYPEDB_EDITION = edition::core;
const std::string CLOUD_USERNAME = "admin";
const std::string CLOUD_PASSWORD = "password";
// end::constants[]
// tag::db-schema-setup[]
void dbSchemaSetup(TypeDB::Session& schemaSession, const std::string& schemaFile = "iam-schema.tql") {
    std::string defineQuery;
    std::ifstream newfile;
    newfile.open(schemaFile, std::ios::in);
    if (newfile.is_open()){
        std::string tmp;
        while(getline(newfile, tmp)){
            defineQuery = defineQuery + tmp + "\n";
        }
        newfile.close();
    } else {
        std::cerr << "Failed to open a file. Terminating..." << std::endl;
        exit(EXIT_FAILURE);
    }
    TypeDB::Options options;
    TypeDB::Transaction tx = schemaSession.transaction(TypeDB::TransactionType::WRITE, options);
    std::cout << "Defining schema...";
    tx.query.define(defineQuery).get();
    tx.commit();
    std::cout << "OK" << std::endl;
}
// end::db-schema-setup[]
// tag::db-dataset-setup[]
void dbDatasetSetup(TypeDB::Session& dataSession, const std::string& dataFile = "iam-data-single-query.tql") {
    std::ifstream file(dataFile);
    std::string insertQuery((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    TypeDB::Options options;
    TypeDB::Transaction tx = dataSession.transaction(TypeDB::TransactionType::WRITE, options);
    std::cout << "Loading data...";
    TypeDB::ConceptMapIterable response = tx.query.insert(insertQuery);
    int16_t count = 0;
    for (TypeDB::ConceptMap& conceptMap : response) { count += 1; }
    tx.commit();
    std::cout << "OK" << std::endl;
}
// end::db-dataset-setup[]
// tag::create_new_db[]
bool createDatabase(TypeDB::Driver& driver, const std::string& dbName) {
    std::cout << "Creating a new database...";
    driver.databases.create(dbName);
    std::cout << "OK" << std::endl;
    TypeDB::Options options;
    {
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::SCHEMA, options);
        dbSchemaSetup(session);
    }
    {
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        dbDatasetSetup(session);
    }
    return true;
}
// end::create_new_db[]
// tag::replace_db[]
bool replaceDatabase(TypeDB::Driver& driver, const std::string& dbName) {
    std::cout << "Deleting an existing database...";
    driver.databases.get(dbName).deleteDatabase(); // Delete the database if it exists already
    std::cout << "OK" << std::endl;
    if (!createDatabase(driver, dbName)) {
        std::cout << "Failed to create a new database. Terminating..." << std::endl;
        exit(EXIT_FAILURE);
    }
    return true;
}
// end::replace_db[]
// tag::test-db[]
bool dbCheck(TypeDB::Session& dataSession) {
    TypeDB::Options options;
    TypeDB::Transaction tx = dataSession.transaction(TypeDB::TransactionType::READ, options);
    std::string testQuery = "match $u isa user; get $u; count;";
    std::cout << "Testing the database...";
    TypeDB::AggregateFuture response = tx.query.getAggregate(testQuery);
    int16_t result = response.get().value().get()->asLong();
    if (result == 3) {
        std::cout << "Passed" << std::endl;
        return true;
    } else {
        std::cout << "Failed with the result: " << result << "\nExpected result: 3." << std::endl;
        return false;
    }
}
// end::test-db[]
// tag::db-setup[]
bool dbSetup(TypeDB::Driver& driver, const std::string& dbName, bool dbReset = false) {
    std::cout << "Setting up the database: " << dbName << std::endl;
    if (driver.databases.contains(dbName)) {
        if (dbReset) {
            replaceDatabase(driver, dbName);
        } else {
            std::string answer;
            std::cout << "Found a pre-existing database. Do you want to replace it? (Y/N) ";
            std::cin >> answer;
            if (answer == "Y" || answer == "y") {
                replaceDatabase(driver, dbName);
            } else {
                std::cout << "Reusing an existing database." << std::endl;
            }
        }
    } else {
        if (!createDatabase(driver, dbName)) {
            std::cout << "Failed to create a new database. Terminating..." << std::endl;
            exit(EXIT_FAILURE);
        }
    }
    TypeDB::Options options;
    if (driver.databases.contains(dbName)) {
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        return dbCheck(session);
    } else {
        std::cout << "Failed to find the database. Terminating..." << std::endl;
        exit(EXIT_FAILURE);
    }
}
// end::db-setup[]
// tag::json[]
void printJSON(TypeDB::JSON json) {
    if (json.isString()) {
        std::cout << "'" << json.asString() << "'" << std::endl;
    }
    if (json.isMap()) {
        TypeDB::JSONMap jsonMap = json.asMap();
        for (const auto& p : jsonMap ) {
                std::cout << p.first << ": "<< std::endl;
                printJSON(p.second);
            }
    }
}
// end::json[]
// tag::fetch[]
std::vector<TypeDB::JSON> fetchAllUsers(TypeDB::Driver& driver, const std::string& dbName) {
    std::vector<TypeDB::JSON> users;
    TypeDB::Options options;
    {
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::READ, options);
        TypeDB::JSONIterable queryResult = tx.query.fetch("match $u isa user; fetch $u: full-name, email;");
        int16_t c = 1;
        for (TypeDB::JSON user : queryResult) {
                users.push_back(user);
                std::cout << "User #" << c++ << " ";
                printJSON(user);
                std::cout << std::endl;
        }
    }
    return users;
}
// end::fetch[]
// tag::insert[]
std::vector<TypeDB::ConceptMap> insertNewUser(TypeDB::Driver& driver, const std::string& dbName, const std::string& name, const std::string& email) {
    std::vector<TypeDB::ConceptMap> response;
    TypeDB::Options options;
    {
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
        TypeDB::ConceptMapIterable response = tx.query.insert("insert $p isa person, has full-name $fn, has email $e; $fn == '" + name + "'; $e == '" + email + "';");
        for (TypeDB::ConceptMap& conceptMap : response) {
            std::string name = conceptMap.get("fn")->asAttribute()->getValue()->asString();
            std::string email = conceptMap.get("e")->asAttribute()->getValue()->asString();
            std::cout << "Added new user. Name: " << name << ", E-mail: " << email << std::endl;
        }
        tx.commit();
    }
    return response;
}
// end::insert[]
// tag::get[]
std::vector<std::string> getFilesByUser(TypeDB::Driver& driver, const std::string& dbName, const std::string& name, bool inference = false) {
    TypeDB::Options options;
    options.infer(inference);
    {
        std::vector<std::string> files;
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::READ, options);
        TypeDB::ConceptMapIterable users = tx.query.get("match $u isa user, has full-name '" + name + "'; get;");
        int16_t userCount = 0;
        for (TypeDB::ConceptMap& user : users) {userCount += 1;}
        if (userCount > 1) {
            std::cout << "Error: Found more than one user with that name." << std::endl;
            return files;
        } else if (userCount == 1) {
            TypeDB::ConceptMapIterable response = tx.query.get(R"(
                                                                match
                                                                $fn == ')" + name + R"(';
                                                                $u isa user, has full-name $fn;
                                                                $p($u, $pa) isa permission;
                                                                $o isa object, has path $fp;
                                                                $pa($o, $va) isa access;
                                                                $va isa action, has name 'view_file';
                                                                get $fp; sort $fp asc;
                                                                )");
            int16_t resultCounter = 0;
            for (TypeDB::ConceptMap& cm : response) {
                resultCounter += 1;
                files.push_back(cm.get("fp") ->asAttribute()->getValue()->asString());
                std::cout << "File #" << std::to_string(resultCounter) << ": " << cm.get("fp") ->asAttribute()->getValue()->asString() << std::endl;
            }
            if (resultCounter == 0) {
                std::cout << "No files found. Try enabling inference." << std::endl;
            }
            return files;
        } else {
            std::cout << "Error: No users found with that name." << std::endl;
            return files;
        }
    }
}
// end::get[]
// tag::update[]
int16_t updateFilePath(TypeDB::Driver& driver, const std::string& dbName, const std::string& oldPath, const std::string& newPath) {
    std::vector<TypeDB::ConceptMap> response;
    int16_t count = 0;
    {
        TypeDB::Options options;
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
        TypeDB::ConceptMapIterable response = tx.query.update(R"(
                                                                match
                                                                $f isa file, has path $old_path;
                                                                $old_path = ')" + oldPath + R"(';
                                                                delete
                                                                $f has $old_path;
                                                                insert
                                                                $f has path $new_path;
                                                                $new_path = ')" + newPath + R"(';
                                                                )");
        for (TypeDB::ConceptMap& conceptMap : response) { count += 1; }
        if (count > 0) {
            tx.commit();
            std::cout << "Total number of paths updated: " << count << "." << std::endl;
        } else {
            std::cout << "No matched paths: nothing to update." << std::endl;
        }
    }
    return count;
}
// end::update[]
// tag::delete[]
bool deleteFile(TypeDB::Driver& driver, const std::string& dbName, const std::string& path) {
    {
        TypeDB::Options options;
        TypeDB::Session session = driver.session(dbName, TypeDB::SessionType::DATA, options);
        TypeDB::Transaction tx = session.transaction(TypeDB::TransactionType::WRITE, options);
        TypeDB::ConceptMapIterable response = tx.query.get(R"(
                                                            match
                                                            $f isa file, has path ')" + path + R"(';
                                                            get;
                                                            )");
        int16_t count = 0;
        for (TypeDB::ConceptMap& conceptMap : response) { count += 1; }
        if (count == 1) {
            tx.query.matchDelete(R"(
                                match
                                $f isa file, has path ')" + path + R"(';
                                delete
                                $f isa file;
                                )").get();
            tx.commit();
            std::cout << "The file has been deleted." << std::endl;
            return true;
        } else if (count > 1) {
            std::cout << "Matched more than one file with the same path." << std::endl;
            std::cout << "No files were deleted." << std::endl;
            return false;
        } else {
            std::cout << "No files matched in the database." << std::endl;
            std::cout << "No files were deleted." << std::endl;
            return false;
        }
    }
}
// end::delete[]
// tag::queries[]
void queries(TypeDB::Driver& driver, const std::string& dbName) {
    std::cout << "\nRequest 1 of 6: Fetch all users as JSON objects with full names and emails" << std::endl;
    std::vector<TypeDB::JSON> users = fetchAllUsers(driver, dbName);

    std::string newName = "Jack Keeper";
    std::string newEmail = "jk@typedb.com";
    std::cout << "\nRequest 2 of 6: Add a new user with the full-name " << newName << " and email " << newEmail << std::endl;
    insertNewUser(driver, dbName, newName, newEmail);

    std::string name = "Kevin Morrison";
    std::cout << "\nRequest 3 of 6: Find all files that the user " << name << " has access to view (no inference)" << std::endl;
    std::vector<std::string> noFiles = getFilesByUser(driver, dbName, name);

    std::cout << "\nRequest 4 of 6: Find all files that the user " << name << " has access to view (with inference)" << std::endl;
    std::vector<std::string> files = getFilesByUser(driver, dbName, name, true);

    std::string oldPath = "lzfkn.java";
    std::string newPath = "lzfkn2.java";
    std::cout << "\nRequest 5 of 6: Update the path of a file from " << oldPath << " to " << newPath << std::endl;
    int16_t updatedFiles = updateFilePath(driver, dbName, oldPath, newPath);

    std::string filePath = "lzfkn2.java";
    std::cout << "\nRequest 6 of 6: Delete the file with path " << filePath << std::endl;
    bool deleted = deleteFile(driver, dbName, filePath);
}
// end::queries[]
// tag::connection[]
TypeDB::Driver connectToTypeDB(const edition typedb_edition,
                                const std::string& addr,
                                const std::string& username=CLOUD_USERNAME,
                                const std::string& password=CLOUD_PASSWORD,
                                const bool encryption = true) {
    if (typedb_edition == edition::core) { return TypeDB::Driver::coreDriver(addr); };
    if (typedb_edition == edition::cloud) { return TypeDB::Driver::cloudDriver({addr}, TypeDB::Credential(username, password, encryption));; };
    exit(EXIT_FAILURE);
}
// end::connection[]
// tag::main[]
int main() {
    TypeDB::Driver driver = connectToTypeDB(TYPEDB_EDITION, SERVER_ADDR);
    if (driver.isOpen()) {
        if (dbSetup(driver, DB_NAME)) {
            queries(driver, DB_NAME);
            return EXIT_SUCCESS;
        } else {
            std::cerr << "Failed to set up the database. Terminating..." << std::endl;
            exit(EXIT_FAILURE);
        }
    } else {
        std::cerr << "Failed to connect to TypeDB server. Terminating..." << std::endl;
        exit(EXIT_FAILURE);
    }
}
// end::main[]
// end::code[]
