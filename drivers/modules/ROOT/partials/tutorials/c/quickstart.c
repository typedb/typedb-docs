#include <stdio.h>
#include "../include/typedb_driver.h"

#define SERVER_ADDR "127.0.0.1:1729"
#define DB_NAME "access-management-db"

#define FAILED() check_error_may_print(__FILE__, __LINE__)

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

void delete_database_if_exists(DatabaseManager* databaseManager, const char* name) {
    if (NULL != databaseManager && databases_contains(databaseManager, name)) {
        Database* database = databases_get(databaseManager, name);
        database_delete(database);
    }
}

void createDatabase(DatabaseManager* dbManager, const char* dbName) {
    Session* session = NULL;
    Transaction* tx = NULL;
    Options* opts = options_new();
    ConceptMapIterator* response1 = NULL;
    ConceptMapIterator* response2 = NULL;
    delete_database_if_exists(dbManager, dbName);
    printf("Creating new database: %s\n", dbName);
    databases_create(dbManager, dbName);
    if (FAILED()) {
        handle_error("Database creation failed.");
        goto cleanup;
    }
    session = session_new(dbManager, dbName, Schema, opts);
    if (session == NULL || FAILED()) {
        goto cleanup;
    }
    tx = transaction_new(session, Write, opts);
    if (tx == NULL || FAILED()) {
        handle_error("Transaction failed to start.");
        goto cleanup;
    }
    void_promise_resolve(query_define(tx, "define person sub entity;", opts));
    if (FAILED()) {
        handle_error("Query execution failed.");
        transaction_close(tx);
        goto cleanup;
    }
    void_promise_resolve(query_define(tx, "define name sub attribute, value string; person owns name;", opts));
    if (FAILED()) {
        handle_error("Query execution failed.");
        transaction_close(tx);
        goto cleanup;
    }
    void_promise_resolve(transaction_commit(tx));
    if (FAILED()) {
        handle_error("Transaction commit failed.");
        goto cleanup;
    }
    printf("Schema setup complete.\n");
    session_close(session);

    session = session_new(dbManager, dbName, Data, opts);
    if (session == NULL || FAILED()) {
        goto cleanup;
    }
    tx = transaction_new(session, Write, opts);
    if (tx == NULL || FAILED()) {
        handle_error("Transaction failed to start.");
        goto cleanup;
    }
    response1 = query_insert(tx, "insert $p isa person, has name 'Alice';", opts);
    if (FAILED()) {
        handle_error("Query execution failed.");
        transaction_close(tx);
        goto cleanup;
    }
    response2 = query_insert(tx, "insert $p isa person, has name 'Bob';", opts);
    if (FAILED()) {
        handle_error("Query execution failed.");
        transaction_close(tx);
        goto cleanup;
    }
    void_promise_resolve(transaction_commit(tx));
    if (FAILED()) {
        handle_error("Transaction commit failed.");
        goto cleanup;
    }
    printf("Data setup complete.\n");
cleanup:
    concept_map_iterator_drop(response1);
    concept_map_iterator_drop(response2);
    session_close(session);
    options_drop(opts);
}

void query(DatabaseManager* dbManager, const char* dbName) {
    Session* dataSession = NULL;
    Transaction* tx = NULL;
    Options* opts = options_new();
    StringIterator* queryResult = NULL;

    dataSession = session_new(dbManager, dbName, Data, opts);
    if (dataSession == NULL || FAILED()) {
        goto cleanup;
    }
    tx = transaction_new(dataSession, Write, opts);
    if (tx == NULL || FAILED()) {
        handle_error("Transaction failed to start.");
        goto cleanup;
    }

    queryResult = query_fetch(tx, "match $p isa person, has name $n; fetch $n;", opts);
    if (queryResult == NULL || FAILED()) {
        handle_error("Query failed or no results.");
        goto cleanup;
    }

    char* userJSON = string_iterator_next(queryResult);
    int counter = 1;
    while (userJSON != NULL) {
        printf("User #%d: ", counter++);
        printf("%s \n",userJSON);
        userJSON = string_iterator_next(queryResult);
    }

    printf("Test complete.\n");
cleanup:
    string_iterator_drop(queryResult);
    transaction_close(tx);
    session_close(dataSession);
    options_drop(opts);
}

int main() {
    bool result = EXIT_FAILURE;
    Connection* connection = NULL;
    DatabaseManager* databaseManager = NULL;
    connection = connection_open_core(SERVER_ADDR);
    if (!connection || FAILED()) {
        handle_error("Failed to connect to TypeDB.");
        goto cleanup;
    }
    databaseManager = database_manager_new(connection);
    if (!databaseManager || FAILED()) {
        handle_error("Failed to get database manager.");
        goto cleanup;
    }
    createDatabase(databaseManager, DB_NAME);
    if (FAILED()) {
        handle_error("Failed to create the database.");
        goto cleanup;
    }
    query(databaseManager, DB_NAME);
    if (FAILED()) {
        handle_error("Failed to query the database.");
        goto cleanup;
    }
    result = EXIT_SUCCESS;
cleanup:
    database_manager_drop(databaseManager);
    connection_close(connection);
    exit(result);
}
