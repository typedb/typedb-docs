// tag::import[]
#include <stdio.h>
#include "../include/typedb_driver.h"
// end::import[]
#define DB_NAME "manual_db"
#define SERVER_ADDR "127.0.0.1:1729"

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

int main() {
    bool result = EXIT_FAILURE;
    Connection* connection = NULL;
    DatabaseManager* databaseManager = NULL;
    Session* session = NULL;
    Transaction* tx = NULL;
    // tag::options[]
    Options* opts = options_new();
    // end::options[]
    // tag::connect_core[]
    connection = connection_open_core(SERVER_ADDR);
    // end::connect_core[]
    if (!connection || FAILED()) {
        handle_error("Failed to connect to TypeDB.");
        goto cleanup;
    }
    /*
    // tag::connect_cloud[]
    Credential* credential = credential_new(
            CLOUD_USERNAME,
            CLOUD_PASSWORD,
            "path/to/tls_root_ca",
            true);
    const char* addrs[] = {addr, NULL};
    connection = connection_open_cloud(addrs, credential);
    credential_drop(credential);
    // end::connect_cloud[]
    */
    databaseManager = database_manager_new(connection);
    if (!databaseManager || FAILED()) {
        handle_error("Failed to get database manager.");
        goto cleanup;
    }
    DatabaseIterator* allDatabases = databases_all(databaseManager);
    // tag::list-db[]
    Database* db = NULL;
    while ((db = database_iterator_next(allDatabases)) != NULL) {
        printf("%s\n", database_get_name(db));
    }
    // end::list-db[]
    if (databases_contains(databaseManager, DB_NAME)) {
        // tag::delete-db[]
        database_delete(databases_get(databaseManager, DB_NAME));
        // end::delete-db[]
    }

    // tag::create-db[]
    databases_create(databaseManager, DB_NAME);
    // end::create-db[]
    printf("Database created.\n");
    // tag::session_open[]
    session = session_new(databaseManager, DB_NAME, Data, opts);
    // end::session_open[]
    // tag::tx_open[]
    tx = transaction_new(session, Read, opts);
    // end::tx_open[]
    // tag::tx_close[]
    transaction_close(tx);
    // end::tx_close[]
    /*
    if (transaction_is_open(tx)) {
        // tag::tx_commit[]
        void_promise_resolve(transaction_commit(tx));
        // end::tx_commit[]
    }
    */
    // tag::session_close[]
    session_close(session);
    // end::session_close[]
    {
        // tag::define[]
        session = session_new(databaseManager, DB_NAME, Schema, opts);
        tx = transaction_new(session, Write, opts);
        if (tx == NULL || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "define email sub attribute, value string; name sub attribute, value string; friendship sub relation, relates friend; user sub entity, owns email @key, owns name, plays friendship:friend; admin sub user;");
        void_promise_resolve(query_define(tx, query, opts));
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        void_promise_resolve(transaction_commit(tx));
        if (FAILED()) {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::define[]
    }
    {
        // tag::undefine[]
        session = session_new(databaseManager, DB_NAME, Schema, opts);
        tx = transaction_new(session, Write, opts);
        if (tx == NULL || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "undefine admin sub user;");
        void_promise_resolve(query_undefine(tx, query, opts));
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        void_promise_resolve(transaction_commit(tx));
        if (FAILED()) {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::undefine[]
    }
    {
        // tag::insert[]
        session = session_new(databaseManager, DB_NAME, Data, opts);
        tx = transaction_new(session, Write, opts);
        if (tx == NULL || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "insert $user1 isa user, has name 'Alice', has email 'alice@vaticle.com'; $user2 isa user, has name 'Bob', has email 'bob@vaticle.com'; $friendship (friend:$user1, friend: $user2) isa friendship;");
        ConceptMapIterator* insertResult = query_insert(tx, query, opts);
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        void_promise_resolve(transaction_commit(tx));
        if (FAILED()) {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::insert[]
    }
    {
        // tag::match-insert[]
        session = session_new(databaseManager, DB_NAME, Data, opts);
        tx = transaction_new(session, Write, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "match $u isa user, has name 'Bob'; insert $new-u isa user, has name 'Charlie', has email 'charlie@vaticle.com'; $f($u,$new-u) isa friendship;");
        ConceptMapIterator* insertResult = query_insert(tx, query, opts);
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        ConceptMap* insertedCM = NULL;
        int16_t counter = 0;
        while ((insertedCM = concept_map_iterator_next(insertResult)) != NULL) {
            counter++;
        }
        if ((counter == 1) || FAILED()) void_promise_resolve(transaction_commit(tx));
        else {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::match-insert[]
    }
    {
        // tag::delete[]
        session = session_new(databaseManager, DB_NAME, Data, opts);
        tx = transaction_new(session, Write, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "match $u isa user, has name 'Charlie'; $f ($u) isa friendship; delete $f isa friendship;");
        void_promise_resolve(query_delete(tx, query, opts));
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        void_promise_resolve(transaction_commit(tx));
        if (FAILED()) {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::delete[]
    }
    {
        // tag::update[]
        session = session_new(databaseManager, DB_NAME, Data, opts);
        tx = transaction_new(session, Write, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "match $u isa user, has name 'Charlie', has email $e; delete $u has $e; insert $u has email 'charles@vaticle.com';");
        ConceptMapIterator* insertResult = query_update(tx, query, opts);
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        ConceptMap* insertedCM = NULL;
        int16_t counter = 0;
        while ((insertedCM = concept_map_iterator_next(insertResult)) != NULL) {
            counter++;
        }
        if ((counter == 1) || FAILED()) void_promise_resolve(transaction_commit(tx));
        else {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::update[]
    }
    {
        // tag::fetch[]
        session = session_new(databaseManager, DB_NAME, Data, opts);
        tx = transaction_new(session, Read, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "match $u isa user; fetch $u: name, email;");
        StringIterator* users = query_fetch(tx, query, opts);
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        char *userJSON;
        while ((userJSON = string_iterator_next(users)) != NULL) {
            printf("%s %s\n", "User:", userJSON);
        }
        transaction_close(tx);
        session_close(session);
        // end::fetch[]
    }
    {
        // tag::get[]
        session = session_new(databaseManager, DB_NAME, Data, opts);
        tx = transaction_new(session, Read, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "match $u isa user, has email $e; get $e;");
        ConceptMapIterator* response = query_get(tx, query, opts);
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        ConceptMap* CM;
        while ((CM = concept_map_iterator_next(response)) != NULL) {
            Concept* emailConcept = concept_map_get(CM, "e");
            printf("%s %s\n", "User:", value_get_string(attribute_get_value(emailConcept)));
        }
        transaction_close(tx);
        session_close(session);
        // end::get[]
    }
    {
        // tag::infer-rule[]
        session = session_new(databaseManager, DB_NAME, Schema, opts);
        tx = transaction_new(session, Write, opts);
        if (tx == NULL || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char queryRule[512];
        snprintf(queryRule, sizeof(queryRule), "define rule users: when { $u isa user; } then { $u has name 'User'; };");
        void_promise_resolve(query_define(tx, queryRule, opts));
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        void_promise_resolve(transaction_commit(tx));
        if (FAILED()) {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::infer-rule[]
        // tag::infer-fetch[]
        session = session_new(databaseManager, DB_NAME, Data, opts);
        Options* optsInfer = options_new();
        options_set_infer(optsInfer, true);
        tx = transaction_new(session, Read, optsInfer);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char queryInfer[512];
        snprintf(queryInfer, sizeof(queryInfer), "match $u isa user; fetch $u: name, email;");
        StringIterator* users = query_fetch(tx, queryInfer, opts);
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        char *userJSON;
        while ((userJSON = string_iterator_next(users)) != NULL) {
            printf("%s %s\n", "User:", userJSON);
        }
        transaction_close(tx);
        session_close(session);
        options_drop(optsInfer);
        // end::infer-fetch[]
    }
    {
        // tag::types-editing[]
        session = session_new(databaseManager, DB_NAME, Schema, opts);
        tx = transaction_new(session, Write, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        Concept* tag = concept_promise_resolve(concepts_put_attribute_type(tx, "tag", String));
        ConceptIterator* entities = entity_type_get_subtypes(tx, concepts_get_root_entity_type(), Explicit);
        Concept* entity;
        while ((entity = concept_iterator_next(entities)) != NULL) {
            printf("Direct subtype of the entity root type: %s\n", thing_type_get_label(entity));
            if (!thing_type_is_abstract(entity)) {
                const struct Annotation* emptyAnnotations[] = {NULL};
                thing_type_set_owns(tx, entity, tag, NULL, emptyAnnotations);
            }
        }
        transaction_close(tx);
        if (FAILED()) {
            handle_error("Transaction close failed.");
            goto cleanup;
        }
        session_close(session);
        // end::types-editing[]
    }
    {
        // tag::types-api[]
        session = session_new(databaseManager, DB_NAME, Schema, opts);
        tx = transaction_new(session, Write, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        Concept* userType = concept_promise_resolve(concepts_get_entity_type(tx, "user"));
        Concept* adminType = concept_promise_resolve(concepts_put_entity_type(tx, "admin"));
        entity_type_set_supertype(tx, adminType, userType);
        ConceptIterator* entities = entity_type_get_subtypes(tx, concepts_get_root_entity_type(), Transitive);
        Concept* entity;
        while ((entity = concept_iterator_next(entities)) != NULL) {
            printf("%s\n", thing_type_get_label(entity));
        }
        void_promise_resolve(transaction_commit(tx));
        if (FAILED()) {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::types-api[]
    }
    {
        session = session_new(databaseManager, DB_NAME, Schema, opts);
        tx = transaction_new(session, Write, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        // tag::get_type[]
        Concept* userType = concept_promise_resolve(concepts_get_entity_type(tx, "user"));
        // end::get_type[]
        // tag::add_type[]
        Concept* adminType = concept_promise_resolve(concepts_put_entity_type(tx, "admin"));
        // end::add_type[]
        // tag::set_supertype[]
        entity_type_set_supertype(tx, adminType, userType);
        // end::set_supertype[]
        // tag::get_instances[]
        ConceptIterator* users = entity_type_get_instances(tx, userType, Explicit);
        // end::get_instances[]
        Concept* user;
        while ((user = concept_iterator_next(users)) != NULL) {
            printf("%s\n", "User:");
            // tag::get_has[]
            const struct Concept *const attribute_types[] = {NULL};
            const struct Annotation* emptyAnnotations[] = {NULL};
            ConceptIterator* attributes = thing_get_has(tx, user, attribute_types, emptyAnnotations);

            // end::get_has[]
            Concept* attribute;
            while ((attribute = concept_iterator_next(attributes)) != NULL) {
                printf("%s: %s\n", thing_type_get_label(attribute_get_type(attribute)), value_get_string(attribute_get_value(attribute)));
            }
        }
        // tag::create[]
        Concept* newUser = concept_promise_resolve(entity_type_create(tx, concept_promise_resolve(concepts_get_entity_type(tx, "user"))));
        // end::create[]
        // tag::delete_user[]
        void_promise_resolve(thing_delete(tx, newUser));
        // end::delete_user[]
        transaction_close(tx);
        if (FAILED()) {
            handle_error("Transaction close failed.");
            goto cleanup;
        }
        session_close(session);
    }
    {
        // tag::rules-api[]
        session = session_new(databaseManager, DB_NAME, Schema, opts);
        tx = transaction_new(session, Write, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        RuleIterator* rules = logic_manager_get_rules(tx);
        Rule* rule;
        while ((rule = rule_iterator_next(rules)) != NULL) {
            printf("%s\n%s\n%s\n", rule_get_label(rule), rule_get_when(rule), rule_get_then(rule));
        }
        Rule* newRule = rule_promise_resolve(logic_manager_put_rule(tx, "Employee", "{$u isa user, has email $e; $e contains '@vaticle.com';}", "$u has name 'Employee'"));
        Rule* oldRule = rule_promise_resolve(logic_manager_get_rule(tx, "users"));
        printf("%s\n", rule_get_label(oldRule));
        rule_delete(tx, newRule);
        void_promise_resolve(transaction_commit(tx));
        if (FAILED()) {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::rules-api[]
    }
    {
        session = session_new(databaseManager, DB_NAME, Schema, opts);
        tx = transaction_new(session, Write, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        // tag::get_rules[]
        RuleIterator* rules = logic_manager_get_rules(tx);
        Rule* rule;
        while ((rule = rule_iterator_next(rules)) != NULL) {
            printf("%s\n%s\n%s\n", rule_get_label(rule), rule_get_when(rule), rule_get_then(rule));
        }
        // end::get_rules[]
        // tag::put_rule[]
        Rule* newRule = rule_promise_resolve(logic_manager_put_rule(tx, "Employee", "{$u isa user, has email $e; $e contains '@vaticle.com';}", "$u has name 'Employee'"));
        // end::put_rule[]
        // tag::get_rule[]
        Rule* oldRule = rule_promise_resolve(logic_manager_get_rule(tx, "users"));
        // end::get_rule[]
        printf("%s\n", rule_get_label(oldRule));
        // tag::delete_rule[]
        rule_delete(tx, newRule);
        // end::delete_rule[]
        void_promise_resolve(transaction_commit(tx));
        if (FAILED()) {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
    }
    {
        // tag::data-api[]
        session = session_new(databaseManager, DB_NAME, Schema, opts);
        tx = transaction_new(session, Write, opts);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        Concept* userType = concept_promise_resolve(concepts_get_entity_type(tx, "user"));
        ConceptIterator* users = entity_type_get_instances(tx, userType, Explicit);
        Concept* user;
        while ((user = concept_iterator_next(users)) != NULL) {
            printf("%s \n", "User:");
            const struct Concept *const attribute_types[] = {NULL};
            const struct Annotation* emptyAnnotations[] = {NULL};
            ConceptIterator* attributes = thing_get_has(tx, user, attribute_types, emptyAnnotations);
            Concept* attribute;
            while ((attribute = concept_iterator_next(attributes)) != NULL) {
                printf("%s: %s\n", thing_type_get_label(attribute_get_type(attribute)), value_get_string(attribute_get_value(attribute)));
            }
        }
        Concept* newUser = concept_promise_resolve(entity_type_create(tx, concept_promise_resolve(concepts_get_entity_type(tx, "user"))));
        void_promise_resolve(thing_delete(tx, newUser));
        void_promise_resolve(transaction_commit(tx));
        if (FAILED()) {
            handle_error("Transaction commit failed.");
            goto cleanup;
        }
        session_close(session);
        // end::data-api[]
    }
    {
        // tag::explain-get[]
        session = session_new(databaseManager, DB_NAME, Data, opts);
        Options* optsInferExplain = options_new();
        options_set_infer(optsInferExplain, true);
        options_set_explain(optsInferExplain, true);
        tx = transaction_new(session, Read, optsInferExplain);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "match $u isa user, has email $e, has name $n; $e contains 'Alice'; get $u, $n;");
        ConceptMapIterator* response = query_get(tx, query, opts);
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        ConceptMap* CM;
        int16_t i = 0;
        while ((CM = concept_map_iterator_next(response)) != NULL) {
            i++;
            Concept* nameConcept = concept_map_get(CM, "n");
            printf("%s %d: %s\n", "Name#", i, value_get_string(attribute_get_value(nameConcept)));
            Explainables* explainables = concept_map_get_explainables(CM);
            StringIterator* explainableRelations = explainables_get_relations_keys(explainables);
            char* explainableKey;
            while ((explainableKey = string_iterator_next(explainableRelations)) != NULL) {
                printf("Explained variable: %s\n Explainable part of the query: %s\n", explainableKey, explainable_get_conjunction( explainables_get_relation(explainables, explainableKey)));
                ExplanationIterator* explainIterator = query_explain(tx, explainables_get_relation(explainables, explainableKey), opts);
                Explanation* explanation;
                while ((explanation = explanation_iterator_next(explainIterator)) != NULL) {
                    Rule* rule = explanation_get_rule(explanation);
                    printf("Rule: %s\nCondition: %s\nConclusion: %s\nVariable mapping:\n", rule_get_label(rule), rule_get_when(rule), rule_get_then(rule));
                    char* var;
                    while ((var = string_iterator_next(explanation_get_mapped_variables(explanation))) != NULL) {
                        printf("Query variable: %s maps to the rule variable(s)", var);
                        char* ruleVar;
                        while ((ruleVar = string_iterator_next(explanation_get_mapping(explanation, var))) != NULL) {
                            printf(" %s", ruleVar);
                        }
                    }
                }
            }
        }
        transaction_close(tx);
        session_close(session);
        options_drop(optsInferExplain);
        // end::explain-get[]
    }
    {
        session = session_new(databaseManager, DB_NAME, Data, opts);
        Options* optsInferExplain = options_new();
        options_set_infer(optsInferExplain, true);
        options_set_explain(optsInferExplain, true);
        tx = transaction_new(session, Read, optsInferExplain);
        if ((tx == NULL) || FAILED()) {
            handle_error("Transaction failed to start.");
            goto cleanup;
        }
        char query[512];
        snprintf(query, sizeof(query), "match $u isa user, has email $e, has name $n; $e contains 'Alice'; get $u, $n;");
        // tag::explainables[]
        ConceptMapIterator* response = query_get(tx, query, opts);
        // end::explainables[]
        if (FAILED()) {
            handle_error("Query execution failed.");
            goto cleanup;
        }
        int16_t i = 0;
        // tag::explainables[]
        ConceptMap* CM = NULL;
        Concept* nameConcept = NULL;
        while ((CM = concept_map_iterator_next(response)) != NULL) {
            // end::explainables[]
            i++;
            nameConcept = concept_map_get(CM, "n");
            printf("%s %d: %s\n", "Name#", i, value_get_string(attribute_get_value(nameConcept)));
            // tag::explainables[]
            Explainables* explainables = concept_map_get_explainables(CM);
            StringIterator* explainableRelations = explainables_get_relations_keys(explainables);
            // end::explainables[]
            // tag::explain[]
            char* explainableKey;
            while ((explainableKey = string_iterator_next(explainableRelations)) != NULL) {
                ExplanationIterator* explainIterator = query_explain(tx, explainables_get_relation(explainables, explainableKey), opts);
                // end::explain[]
                printf("Explained variable: %s\n Explainable part of the query: %s\n", explainableKey, explainable_get_conjunction( explainables_get_relation(explainables, explainableKey)));
                // tag::explanation[]
                Explanation* explanation;
                while ((explanation = explanation_iterator_next(explainIterator)) != NULL) {
                    Rule* rule = explanation_get_rule(explanation);
                    printf("Rule: %s\nCondition: %s\nConclusion: %s\nVariable mapping:\n", rule_get_label(rule), rule_get_when(rule), rule_get_then(rule));
                    char* var;
                    while ((var = string_iterator_next(explanation_get_mapped_variables(explanation))) != NULL) {
                        printf("Query variable: %s maps to the rule variable(s)", var);
                        char* ruleVar;
                        while ((ruleVar = string_iterator_next(explanation_get_mapping(explanation, var))) != NULL) {
                            printf(" %s", ruleVar);
                        }
                    }
                }
                // end::explanation[]
            // tag::explain[]
            }
            // end::explain[]
        // tag::explainables[]
        }
        // end::explainables[]
        transaction_close(tx);
        session_close(session);
    }
    result = EXIT_SUCCESS;
cleanup:
    database_manager_drop(databaseManager);
    connection_close(connection);
    exit(result);
}
