// tag::code[]
// tag::import[]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "include/typedb_driver.h"
// end::import[]
// tag::constants[]
#define SERVER_ADDR "127.0.0.1:1729"
#define DB_NAME "sample_app_db"
#define CLOUD_USERNAME "admin"
#define CLOUD_PASSWORD "password"
#define FAILED() check_error_may_print(__FILE__, __LINE__)

typedef enum { CORE, CLOUD } edition;
edition TYPEDB_EDITION = CORE;
// end::constants[]
// tag::error_handling[]
void handle_error(const char* message) {
    fprintf(stderr, "%s\n", message);
    exit(EXIT_FAILURE);
}

bool check_error_may_print(const char* filename, int lineno) {
    if (check_error()) {
        Error* error = get_last_error();
        char* errcode = error_code(error);
        char* errmsg = error_message(error);
        fprintf(stderr, "Error!\nCheck called at %s:%d\n%s: %s\n", filename, lineno, errcode, errmsg);
        string_free(errmsg);
        string_free(errcode);
        error_drop(error);
        return true;
    } else return false;
}
// end::error_handling[]
// tag::db-schema-setup[]
void dbSchemaSetup(Session* schemaSession, const char* schemaFile) {
    Transaction* tx = NULL;
    Options* opts = options_new();
    char defineQuery[4096] = {0};
    FILE* file = fopen(schemaFile, "r");
    if (FAILED()) goto cleanup;
    if (!file) handle_error("Failed to open schema file.");
    char line[512];
    while (fgets(line, sizeof(line), file)) strcat(defineQuery, line);
    fclose(file);

    tx = transaction_new(schemaSession, Write, opts);
    if (tx == NULL || FAILED()) {
        handle_error("Transaction failed to start.");
        goto cleanup;
    }
    void_promise_resolve(query_define(tx, defineQuery, opts));
    if (FAILED()) {
        handle_error("Query execution failed.");
        goto cleanup;
    }
    void_promise_resolve(transaction_commit(tx));
    if (FAILED()) {
        handle_error("Transaction commit failed.");
        goto cleanup;
    }
    printf("Schema setup complete.\n");
cleanup:
    options_drop(opts);
}
// end::db-schema-setup[]
// tag::db-dataset-setup[]
void dbDatasetSetup(Session* dataSession, const char* dataFile) {
    bool result = false;
    Transaction* tx = NULL;
    Options* opts = options_new();
    char insertQuery[4096] = {0};
    FILE* file = fopen(dataFile, "r");
    if (!file) handle_error("Failed to open data file.");

    char line[512];
    while (fgets(line, sizeof(line), file)) strcat(insertQuery, line);
    fclose(file);

    tx = transaction_new(dataSession, Write, opts);
    if (tx == NULL || FAILED()) {
        handle_error("Transaction failed to start.");
        goto cleanup;
    }
    ConceptMapIterator* insertResult = query_insert(tx, insertQuery, opts);
    if (FAILED()) {
        handle_error("Query execution failed.");
        goto cleanup;
    }
    void_promise_resolve(transaction_commit(tx));
    if (FAILED()) {
        handle_error("Transaction commit failed.");
        goto cleanup;
    }
    printf("Dataset setup complete.\n");
    result = true;
cleanup:
    concept_map_iterator_drop(insertResult);
    // transaction_close(tx);
    options_drop(opts);
}
// end::db-dataset-setup[]
// tag::create_new_db[]
bool createDatabase(DatabaseManager* dbManager, const char* dbName) {
    Session* schemaSession = NULL;
    Session* dataSession = NULL;
    Options* opts = options_new();
    bool result = false;
    printf("Creating new database: %s\n", dbName);
    databases_create(dbManager, dbName);
    if (FAILED()) {
        handle_error("Database creation failed.");
        goto cleanup;
    }
    schemaSession = session_new(dbManager, dbName, Schema, opts);
    if (schemaSession == NULL || FAILED()) {
        goto cleanup;
    }
    dbSchemaSetup(schemaSession, "iam-schema.tql");
    session_close(schemaSession);
    dataSession = session_new(dbManager, dbName, Data, opts);
    if (dataSession == NULL || FAILED()) {
        goto cleanup;
    }
    dbDatasetSetup(dataSession, "iam-data-single-query.tql");
    session_close(dataSession);
    result = true;
cleanup:
    options_drop(opts);
    return result;
}
// end::create_new_db[]
// tag::replace_db[]
void delete_database_if_exists(DatabaseManager* databaseManager, const char* name) {
    if (NULL != databaseManager && databases_contains(databaseManager, name)) {
        Database* database = databases_get(databaseManager, name);
        database_delete(database);
    }
}

bool replaceDatabase(DatabaseManager* dbManager, const char* dbName) {
    printf("Deleting an existing database...");
    delete_database_if_exists(dbManager, dbName);
    if (FAILED()) {
        printf("Failed to delete the database. Terminating...\n");
        exit(EXIT_FAILURE);
    }
    printf("OK\n");

    if (!createDatabase(dbManager, dbName)) {
        printf("Failed to create a new database. Terminating...\n");
        exit(EXIT_FAILURE);
    }
    return true;
}
// end::replace_db[]
// tag::test-db[]
bool dbCheck(Session* dataSession) {
    printf("Testing the database...");
    bool result = false;
    Transaction* tx = NULL;
    Options* opts = options_new();
    tx = transaction_new(dataSession, Read, opts);
    if (tx == NULL || FAILED()) {
        handle_error("Transaction failed to start.");
        goto cleanup;
    }
    const char* testQuery = "match $u isa user; get $u; count;";
    Concept* response = concept_promise_resolve(query_get_aggregate(tx, testQuery, opts));
    if (response == NULL || FAILED()) {
        handle_error("Query execution failed.");
        goto cleanup;
    }
    long answer = value_get_long(response);
    if (FAILED()) {
        handle_error("Value convertion failed.");
        goto cleanup;
    }

    if (answer == 3) {
        printf("Passed\n");
        result = true;
    } else {
        printf("Failed with the result: %ld\nExpected result: 3.\n", answer);
        exit(EXIT_FAILURE);
    }
cleanup:
    concept_drop(response);
    transaction_close(tx);
    options_drop(opts);
    return result;
}
// end::test-db[]
// tag::db-setup[]
bool dbSetup(DatabaseManager* dbManager, const char* dbName, bool dbReset) {
    printf("Setting up the database: %s\n", dbName);
    bool result = false;
    Options* opts = options_new();

    if (databases_contains(dbManager, dbName)) {
        if (dbReset) {
            if (!replaceDatabase(dbManager, dbName)) {
                printf("Failed to replace the database. Terminating...\n");
                exit(EXIT_FAILURE);
            }
        } else {
            char answer[10];
            printf("Found a pre-existing database. Do you want to replace it? (Y/N) ");
            scanf("%s", answer);
            if (strcmp(answer, "Y") == 0 || strcmp(answer, "y") == 0) {
                if (!replaceDatabase(dbManager, dbName)) {
                    printf("Failed to replace the database. Terminating...\n");
                    exit(EXIT_FAILURE);
                }
            } else {
                printf("Reusing an existing database.\n");
            }
        }
    } else {
        if (!createDatabase(dbManager, dbName)) {
            printf("Failed to create a new database. Terminating...\n");
            exit(EXIT_FAILURE);
        }
    }

    if (databases_contains(dbManager, dbName)) {
        Session* session = session_new(dbManager, dbName, Data, opts);
        if (session == NULL || FAILED()) {
            printf("Failed to open a session. Terminating...\n");
            exit(EXIT_FAILURE);
        }
        result = dbCheck(session);
        session_close(session);
        return result;
    } else {
        printf("Failed to find the database after creation. Terminating...\n");
        exit(EXIT_FAILURE);
    }
    return result;
}
// end::db-setup[]
// tag::fetch[]
int fetchAllUsers(DatabaseManager* dbManager, const char* dbName) {
    Options* opts = options_new();
    Transaction* tx = NULL;
    StringIterator* queryResult = NULL;
    Session* session = session_new(dbManager, dbName, Data, opts);
    if (session == NULL || FAILED()) {
        fprintf(stderr, "Failed to open session.\n");
        exit(EXIT_FAILURE);
    }
    tx = transaction_new(session, Read, opts);
    if (tx == NULL || FAILED()) {
        fprintf(stderr, "Failed to start transaction.\n");
        session_close(session);
        exit(EXIT_FAILURE);
    }

    const char* query = "match $u isa user; fetch $u: full-name, email;";
    queryResult = query_fetch(tx, query, opts);
    if (queryResult == NULL || FAILED()) {
        fprintf(stderr, "Query failed or no results.\n");
        transaction_close(tx);
        session_close(session);
        exit(EXIT_FAILURE);
    }

    char* userJSON = string_iterator_next(queryResult);
    int counter = 1;
    while (userJSON != NULL) {
        printf("User #%d: ", counter++);
        printf("%s \n",userJSON);
        userJSON = string_iterator_next(queryResult);
    }
cleanup:
    string_iterator_drop(queryResult);
    transaction_close(tx);
    session_close(session);
    return counter-1;
}
// end::fetch[]
// tag::insert[]
int insertNewUser(DatabaseManager* dbManager, const char* dbName, const char* name, const char* email) {
    Options* opts = options_new();
    Transaction* tx = NULL;
    Session* session = NULL;
    ConceptMapIterator* response = NULL;
    ConceptMap* conceptMap = NULL;

    session = session_new(dbManager, dbName, Data, opts);
    if (session == NULL || FAILED()) {
        fprintf(stderr, "Failed to open session.\n");
        exit(EXIT_FAILURE);
    }

    tx = transaction_new(session, Write, opts);
    if (tx == NULL || FAILED()) {
        fprintf(stderr, "Failed to start transaction.\n");
        session_close(session);
        exit(EXIT_FAILURE);
    }

    char query[512];
    snprintf(query, sizeof(query), "insert $p isa person, has full-name $fn, has email $e; $fn == '%s'; $e == '%s';", name, email);
    response = query_insert(tx, query, opts);
    if (response == NULL || FAILED()) {
        fprintf(stderr, "Failed to execute insert query.\n");
        transaction_close(tx);
        session_close(session);
        exit(EXIT_FAILURE);
    }

    int insertedCount = 0;
    while ((conceptMap = concept_map_iterator_next(response)) != NULL) {
        Concept* fnConcept = concept_map_get(conceptMap, "fn");
        Concept* eConcept = concept_map_get(conceptMap, "e");
        const char* fullName = value_get_string(attribute_get_value(fnConcept));
        const char* userEmail = value_get_string(attribute_get_value(eConcept));
        printf("Added new user. Name: %s, E-mail: %s\n", fullName, userEmail);
        concept_drop(fnConcept);
        concept_drop(eConcept);
        concept_map_drop(conceptMap);
        insertedCount++;
    }
    concept_map_iterator_drop(response);
    void_promise_resolve(transaction_commit(tx));
    session_close(session);
    return insertedCount;
}
// end::insert[]
// tag::get[]
int getFilesByUser(DatabaseManager* dbManager, const char* dbName, const char* name, bool inference) {
    Transaction* tx = NULL;
    Session* session = NULL;
    ConceptMapIterator* userResult = NULL;
    ConceptMapIterator* response = NULL;
    ConceptMap* cm = NULL;
    Options* opts = options_new();

    session = session_new(dbManager, dbName, Data, opts);
    if (session == NULL || FAILED()) {
        fprintf(stderr, "Failed to open session.\n");
        options_drop(opts);
        exit(EXIT_FAILURE);
    }

    options_set_infer(opts, inference);
    tx = transaction_new(session, Read, opts);
    if (tx == NULL || FAILED()) {
        fprintf(stderr, "Failed to start transaction.\n");
        options_drop(opts);
        session_close(session);
        exit(EXIT_FAILURE);
    }

    char query[512];
    snprintf(query, sizeof(query), "match $u isa user, has full-name '%s'; get;", name);
    userResult = query_get(tx, query, options_new());
    int userCount = 0;
    while (concept_map_iterator_next(userResult) != NULL) { userCount++; }
    concept_map_iterator_drop(userResult);

    if (userCount > 1) {
        fprintf(stderr, "Error: Found more than one user with that name.\n");
    } else if (userCount == 1) {
        snprintf(query, sizeof(query), "match $fn == '%s'; $u isa user, has full-name $fn; $p($u, $pa) isa permission; $o isa object, has path $fp; $pa($o, $va) isa access;$va isa action, has name 'view_file'; get $fp; sort $fp asc;", name);
        response = query_get(tx, query, options_new());
        int fileCount = 0;
        while ((cm = concept_map_iterator_next(response)) != NULL) {
            Concept* filePathConcept = concept_map_get(cm, "fp");
            const char* filePath = value_get_string(attribute_get_value(filePathConcept));
            printf("File #%d: %s\n", ++fileCount, filePath);
            concept_drop(filePathConcept);
            concept_map_drop(cm);
        }
        concept_map_iterator_drop(response);
        if (fileCount == 0) {
            printf("No files found. Try enabling inference.\n");
        }
    } else {
        fprintf(stderr, "Error: No users found with that name.\n");
    }

    transaction_close(tx);
    options_drop(opts);
    session_close(session);
    return userCount;
}
// end::get[]
// tag::update[]
int16_t updateFilePath(DatabaseManager* dbManager, const char* dbName, const char* oldPath, const char* newPath) {
    Transaction* tx = NULL;
    Session* session = NULL;
    Options* opts = options_new();
    ConceptMapIterator* response = NULL;
    session = session_new(dbManager, dbName, Data, opts);
    if (session == NULL || FAILED()) {
        fprintf(stderr, "Failed to open session.\n");
        exit(EXIT_FAILURE);
    }

    tx = transaction_new(session, Write, opts);
    if (tx == NULL || FAILED()) {
        fprintf(stderr, "Failed to start transaction.\n");
        session_close(session);
        exit(EXIT_FAILURE);
    }

    char query[512];
    snprintf(query, sizeof(query), "match $f isa file, has path $old_path; $old_path = '%s'; delete $f has $old_path; insert $f has path $new_path; $new_path = '%s';", oldPath, newPath);

    response = query_update(tx, query, opts);
    if (response == NULL || FAILED()) {
        fprintf(stderr, "Query failed or no results.\n");
        transaction_close(tx);
        session_close(session);
        exit(EXIT_FAILURE);
    }

    int16_t count = 0;
    while (concept_map_iterator_next(response) != NULL) {
        count++;
    }
    concept_map_iterator_drop(response);

    if (count > 0) {
        void_promise_resolve(transaction_commit(tx));
        printf("Total number of paths updated: %d.\n", count);
    } else {
        printf("No matched paths: nothing to update.\n");
    }

    session_close(session);
    return count;
}
// end::update[]
// tag::delete[]
bool deleteFile(DatabaseManager* dbManager, const char* dbName, const char* path) {
    bool result = false;
    Transaction* tx = NULL;
    Session* session = NULL;
    Options* opts = options_new();
    ConceptMapIterator* response = NULL;

    session = session_new(dbManager, dbName, Data, opts);
    if (session == NULL || FAILED()) {
        fprintf(stderr, "Failed to open session.\n");
        exit(EXIT_FAILURE);
    }

    tx = transaction_new(session, Write, opts);
    if (tx == NULL || FAILED()) {
        fprintf(stderr, "Failed to start transaction.\n");
        session_close(session);
        exit(EXIT_FAILURE);
    }

    char query[256];
    snprintf(query, sizeof(query), "match $f isa file, has path '%s'; get;", path);
    response = query_get(tx, query, opts);
    if (response == NULL || FAILED()) {
        fprintf(stderr, "Query failed or no results.\n");
        transaction_close(tx);
        session_close(session);
        exit(EXIT_FAILURE);
    }

    int16_t count = 0;
    while (concept_map_iterator_next(response) != NULL) {
        count++;
    }
    concept_map_iterator_drop(response);

    if (count == 1) { // Delete the file if exactly one was found
        snprintf(query, sizeof(query), "match $f isa file, has path '%s'; delete $f isa file;", path);
        if (query_delete(tx, query, opts) == NULL || FAILED()) {
            fprintf(stderr, "Failed to delete file.\n");
            transaction_close(tx);
            session_close(session);
            exit(EXIT_FAILURE);
        }
        void_promise_resolve(transaction_commit(tx));
        printf("The file has been deleted.\n");
        result = true;
    } else if (count > 1) fprintf(stderr, "Matched more than one file with the same path.\nNo files were deleted.\n");
    else fprintf(stderr, "No files matched in the database.\nNo files were deleted.\n");

    session_close(session);
    return result;
}
// end::delete[]
// tag::connection[]
Connection* connectToTypeDB(edition typedb_edition, const char* addr) {
    Connection* connection = NULL;
    if (typedb_edition == CORE) {
        connection = connection_open_core(addr);
    } else {
        Credential* credential = credential_new(
            CLOUD_USERNAME,
            CLOUD_PASSWORD,
            "path/to/tls_root_ca",
            true);
        const char* addrs[] = {addr, NULL};
        connection = connection_open_cloud(addrs, credential);
        credential_drop(credential);
    }
    if (!connection) handle_error("Failed to connect to TypeDB server.");
    return connection;
}
// end::connection[]
// tag::queries[]
bool queries(DatabaseManager* dbManager, const char* dbName) {
    printf("\nRequest 1 of 6: Fetch all users as JSON objects with full names and emails\n");
    int userCount = fetchAllUsers(dbManager, dbName);

    const char* newName = "Jack Keeper";
    const char* newEmail = "jk@typedb.com";
    printf("\nRequest 2 of 6: Add a new user with the full-name %s and email %s\n", newName, newEmail);
    int newUserAdded = insertNewUser(dbManager, dbName, newName, newEmail);

    const char* name = "Kevin Morrison";
    printf("\nRequest 3 of 6: Find all files that the user %s has access to view (no inference)\n", name);
    int noFilesCount = getFilesByUser(dbManager, dbName, name, false);

    printf("\nRequest 4 of 6: Find all files that the user %s has access to view (with inference)\n", name);
    int filesCount = getFilesByUser(dbManager, dbName, name, true);

    const char* oldPath = "lzfkn.java";
    const char* newPath = "lzfkn2.java";
    printf("\nRequest 5 of 6: Update the path of a file from %s to %s\n", oldPath, newPath);
    int16_t updatedFiles = updateFilePath(dbManager, dbName, oldPath, newPath);

    const char* filePath = "lzfkn2.java";
    printf("\nRequest 6 of 6: Delete the file with path %s\n", filePath);
    bool deleted = deleteFile(dbManager, dbName, filePath);

    return true;
}
// end::queries[]
// tag::main[]
int main() {
    bool result = EXIT_FAILURE;
    Connection* connection = NULL;
    DatabaseManager* databaseManager = NULL;
    connection = connectToTypeDB(TYPEDB_EDITION, SERVER_ADDR);
    if (!connection || FAILED()) {
        handle_error("Failed to connect to TypeDB.");
        goto cleanup;
    }
    databaseManager = database_manager_new(connection);
    if (!databaseManager || FAILED()) {
        handle_error("Failed to get database manager.");
        goto cleanup;
    }
    if (!dbSetup(databaseManager, DB_NAME, false)) {
        handle_error("Failed to set up the database.");
        goto cleanup;
    }
    if (!queries(databaseManager, DB_NAME)) {
        handle_error("Failed to query the database.");
        goto cleanup;
    }
    result = EXIT_SUCCESS;
cleanup:
    database_manager_drop(databaseManager);
    connection_close(connection);
    exit(result);
}
// end::main[]
// end::code[]
