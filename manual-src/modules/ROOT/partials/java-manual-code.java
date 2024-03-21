package org.example;
// tag::import[]
import com.vaticle.typedb.common.collection.Pair;
import com.vaticle.typedb.driver.TypeDB;
import com.vaticle.typedb.driver.api.*;
import com.vaticle.typedb.driver.api.answer.ConceptMap;
import com.vaticle.typedb.driver.api.concept.Concept;
import com.vaticle.typedb.driver.api.concept.thing.Attribute;
import com.vaticle.typedb.driver.api.concept.thing.Entity;
import com.vaticle.typedb.driver.api.concept.type.AttributeType;
import com.vaticle.typedb.driver.api.concept.type.EntityType;
import com.vaticle.typedb.driver.api.concept.type.ThingType;
import com.vaticle.typedb.driver.api.concept.value.Value;
import com.vaticle.typedb.driver.api.logic.Explanation;
import com.vaticle.typedb.driver.api.logic.Rule;
import com.vaticle.typeql.lang.TypeQL;
import com.vaticle.typeql.lang.pattern.Pattern;
import java.util.Collections;
import java.util.Set;
import java.util.stream.Stream;

// end::import[]
public class Main {
    public static void main(String[] args) {
        final String DB_NAME = "sample_db";
        final String SERVER_ADDR = "127.0.0.1:1729";

        System.out.println("TypeDB Manual sample code");
        // tag::driver[]
        TypeDBDriver driver = TypeDB.coreDriver(SERVER_ADDR);
        // end::driver[]
        // tag::list-db[]
        driver.databases().all().forEach( result -> System.out.println(result.name()));
        // end::list-db[]
        if (driver.databases().contains(DB_NAME)) {
            // tag::delete-db[]
            driver.databases().get(DB_NAME).delete();
            // end::delete-db[]
        }
        // tag::create-db[]
        driver.databases().create(DB_NAME);
        // end::create-db[]
        if (driver.databases().contains(DB_NAME)) {
            System.out.println("Database setup complete.");
        }

        try {
            /*
            // tag::connect_core[]
            TypeDBDriver driver = TypeDB.coreDriver("127.0.0.1:1729");
            // end::connect_core[]
            try {
                // tag::connect_cloud[]
                TypeDBDriver driver = TypeDB.cloudDriver("127.0.0.1:1729", new TypeDBCredential("admin", "password", true ));
                // end::connect_cloud[]
            } catch (Exception ignored) {

            }
            */
            // tag::session_open[]
            TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.SCHEMA);
            // end::session_open[]
            // tag::tx_open[]
            TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE);
            // end::tx_open[]
            // tag::tx_close[]
            tx.close();
            // end::tx_close[]
            if (tx.isOpen()) {
                // tag::tx_commit[]
                tx.commit();
                // end::tx_commit[]
            }
            ;
            // tag::session_close[]
            session.close();
            // end::session_close[]
        } finally {

        }
        // tag::define[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.SCHEMA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                String defineQuery = """
                                    define
                                    email sub attribute, value string;
                                    name sub attribute, value string;
                                    friendship sub relation, relates friend;
                                    user sub entity,
                                        owns email @key,
                                        owns name,
                                        plays friendship:friend;
                                    admin sub user;
                                    """;
                tx.query().define(defineQuery).resolve();
                tx.commit();
            }
        }
        // end::define[]
        // tag::undefine[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.SCHEMA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                String undefineQuery = "undefine admin sub user;";
                tx.query().undefine(undefineQuery).resolve();
                tx.commit();
            }
        }
        // end::undefine[]
        // tag::insert[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                String insertQuery = """
                                    insert
                                    $user1 isa user, has name "Alice", has email "alice@typedb.com";
                                    $user2 isa user, has name "Bob", has email "bob@typedb.com";
                                    $friendship (friend:$user1, friend: $user2) isa friendship;
                                    """;
                tx.query().insert(insertQuery);
                tx.commit();
            }
        }
        // end::insert[]
        // tag::match-insert[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                String matchInsertQuery = """
                                        match
                                        $u isa user, has name "Bob";
                                        insert
                                        $new-u isa user, has name "Charlie", has email "charlie@typedb.com";
                                        $f($u,$new-u) isa friendship;
                                        """;
                long response_count = tx.query().insert(matchInsertQuery).count();
                if (response_count == 1) {
                    tx.commit();
                } else {
                    tx.close();
                }
            }
        }
        // end::match-insert[]
        // tag::delete[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                String deleteQuery = """
                                    match
                                    $u isa user, has name "Charlie";
                                    $f ($u) isa friendship;
                                    delete
                                    $f isa friendship;
                                    """;
                tx.query().delete(deleteQuery).resolve();
                tx.commit();
            }
        }
        // end::delete[]
        // tag::update[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                String updateQuery = """
                                    match
                                    $u isa user, has name "Charlie", has email $e;
                                    delete
                                    $u has $e;
                                    insert
                                    $u has email "charles@typedb.com";
                                    """;
                long response_count = tx.query().update(updateQuery).count();
                if (response_count == 1) {
                    tx.commit();
                } else {
                    tx.close();
                }
            }
        }
        // end::update[]
        // tag::fetch[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.READ)) {
                String fetchQuery = """
                                    match
                                    $u isa user;
                                    fetch
                                    $u: name, email;
                                    """;
                int[] ctr = new int[1];
                tx.query().fetch(fetchQuery).forEach(result -> System.out.println("Email #" + (++ctr[0]) + ": " + result.toString()));
            }
        }
        // end::fetch[]
        // tag::get[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.READ)) {
                String getQuery = """
                                    match
                                    $u isa user, has email $e;
                                    get
                                    $e;
                                    """;
                int[] ctr = new int[1];
                tx.query().get(getQuery).forEach(result -> System.out.println("Email #" + (++ctr[0]) + ": " + result.get("e").asAttribute().getValue().toString()));
            }
        }
        // end::get[]
        // tag::infer-rule[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.SCHEMA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                String defineQuery = """
                                    define
                                    rule users:
                                    when {
                                        $u isa user;
                                    } then {
                                        $u has name "User";
                                    };
                                    """;
                tx.query().define(defineQuery).resolve();
                tx.commit();
            }
        }
        // end::infer-rule[]
        // tag::infer-fetch[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            TypeDBOptions options = new TypeDBOptions().infer(true);
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.READ, options)) {
                String fetchQuery = """
                                    match
                                    $u isa user;
                                    fetch
                                    $u: name, email;
                                    """;
                int[] ctr = new int[1];
                tx.query().fetch(fetchQuery).forEach(result -> System.out.println("Email #" + (++ctr[0]) + ": " + result.toString()));
            }
        }
        // end::infer-fetch[]
        // tag::types-editing[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.SCHEMA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                AttributeType tag = tx.concepts().putAttributeType("tag", Value.Type.STRING).resolve();
                tx.concepts().getRootEntityType().getSubtypes(tx, Concept.Transitivity.EXPLICIT).forEach(result -> {
                    System.out.println(result.getLabel().toString());
                    if (! result.isAbstract()) {
                        result.setOwns(tx,tag).resolve();
                    }
                });
                tx.commit();
            }
        }
        // end::types-editing[]
        // tag::types-api[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.SCHEMA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                EntityType userType = tx.concepts().getEntityType("user").resolve();
                EntityType adminType = tx.concepts().putEntityType("admin").resolve();
                adminType.setSupertype(tx, userType).resolve();
                EntityType root_entity = tx.concepts().getRootEntityType();
                root_entity.getSubtypes(tx, Concept.Transitivity.TRANSITIVE).forEach(result -> System.out.println(result.getLabel().name()));
                tx.commit();
            }
        }
        // end::types-api[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.SCHEMA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                // tag::get_type[]
                EntityType userType = tx.concepts().getEntityType("user").resolve();
                // end::get_type[]
                // tag::add_type[]
                EntityType adminType = tx.concepts().putEntityType("admin").resolve();
                // end::add_type[]
                // tag::set_supertype[]
                adminType.setSupertype(tx, userType).resolve();
                // end::set_supertype[]

                // tag::get_instances[]
                Stream<? extends Entity> users = userType.getInstances(tx);
                // end::get_instances[]
                Set<ThingType.Annotation> annotations = Collections.emptySet();
                users.forEach(user -> {
                    System.out.println("User");
                    // tag::get_has[]
                    Stream<? extends Attribute> attributes = user.getHas(tx, annotations);
                    // end::get_has[]
                    attributes.forEach(attribute ->
                        System.out.println(attribute.getType().getLabel().toString()+ ": " + attribute.getValue().toString())
                    );
                });
                // tag::create[]
                Entity new_user = tx.concepts().getEntityType("user").resolve().create(tx).resolve();
                // end::create[]
                // tag::delete_user[]
                new_user.delete(tx).resolve();
                // end::delete_user[]
            }
        }

        // tag::rules-api[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.SCHEMA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                tx.logic().getRules().forEach(result -> {
                    System.out.println(result.getLabel());
                    System.out.println(result.getWhen().toString());
                    System.out.println(result.getThen().toString());
                });
                Pattern condition = TypeQL.parsePattern("{$u isa user, has email $e; $e contains '@typedb.com';}");
                Pattern conclusion = TypeQL.parsePattern("$u has name 'Employee'");
                Rule newRule = tx.logic().putRule("Employee", condition, conclusion).resolve();
                Rule oldRule = tx.logic().getRule("users").resolve();
                System.out.println(oldRule.getLabel());
                newRule.delete(tx).resolve();
                tx.commit();
            }
        }
        // end::rules-api[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.SCHEMA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                // tag::get_rule[]
                Rule oldRule = tx.logic().getRule("users").resolve();
                // end::get_rule[]
                // tag::put_rule[]
                Pattern condition = TypeQL.parsePattern("{$u isa user, has email $e; $e contains '@typedb.com';}");
                Pattern conclusion = TypeQL.parsePattern("$u has name 'Employee'");
                Rule newRule = tx.logic().putRule("Employee", condition, conclusion).resolve();
                // end::put_rule[]
                // tag::get_rules[]
                tx.logic().getRules().forEach(result -> {
                    System.out.println(result.getLabel());
                    System.out.println(result.getWhen().toString());
                    System.out.println(result.getThen().toString());
                });
                // end::get_rules[]
                // tag::delete_rule[]
                newRule.delete(tx).resolve();
                // end::delete_rule[]
            }
        }

        // tag::data-api[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.WRITE)) {
                Set<ThingType.Annotation> annotations = Collections.emptySet();
                EntityType userType = tx.concepts().getEntityType("user").resolve();
                userType.getInstances(tx).forEach(user -> {
                    System.out.println("User");
                    Stream<? extends Attribute> attributes = user.getHas(tx, annotations);
                    attributes.forEach(attribute ->
                        System.out.println(attribute.getType().getLabel().toString()+ ": " + attribute.getValue().toString())
                    );
                });
                Entity new_user = tx.concepts().getEntityType("user").resolve().create(tx).resolve();
                new_user.delete(tx).resolve();
                tx.commit();
            }
        }
        // end::data-api[]
        // tag::explain-get[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            TypeDBOptions options = new TypeDBOptions().infer(true).explain(true);
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.READ, options)) {
                String getQuery = """
                                    match
                                    $u isa user, has email $e, has name $n;
                                    $e contains 'Alice';
                                    get
                                    $u, $n;
                                    """;
                int[] ctr = new int[1];
                tx.query().get(getQuery).forEach(result -> {
                    String name = result.get("n").asAttribute().getValue().toString();
                    System.out.println("Email #" + (++ctr[0]) + ": " + name);
                    Stream<Pair<String, ConceptMap.Explainable>> explainable_relations = result.explainables().relations();
                    explainable_relations.forEach(explainable -> {
                        System.out.println("Explainable variable:" + explainable.first());
                        System.out.println("Explainable part of the query:" + explainable.second().conjunction());
                        Stream<Explanation> explain_iterator = tx.query().explain(explainable.second());
                        explain_iterator.forEach(explanation -> {
                            System.out.println("Rule: " + explanation.rule().getLabel());
                            System.out.println("  Condition: " + explanation.rule().getWhen().toString());
                            System.out.println("  Conclusion: " + explanation.rule().getThen().toString());
                            explanation.queryVariables().forEach(var ->
                                System.out.println("Query variable " + var + "maps to the rule variable " + explanation.queryVariableMapping(var)));
                        });
                    });
                });
            }
        }
        // end::explain-get[]
        try (TypeDBSession session = driver.session(DB_NAME, TypeDBSession.Type.DATA)) {
            TypeDBOptions options = new TypeDBOptions().infer(true).explain(true);
            try (TypeDBTransaction tx = session.transaction(TypeDBTransaction.Type.READ, options)) {
                String getQuery = """
                                    match
                                    $u isa user, has email $e, has name $n;
                                    $e contains 'Alice';
                                    get
                                    $u, $n;
                                    """;
                int[] ctr = new int[1];
                // tag::explainables[]
                Stream<ConceptMap> response = tx.query().get(getQuery);
                response.forEach(result -> {
                // end::explainables[]
                    String name = result.get("n").asAttribute().getValue().toString();
                    System.out.println("Email #" + (++ctr[0]) + ": " + name);
                    // tag::explainables[]
                    Stream<Pair<String, ConceptMap.Explainable>> explainable_relations = result.explainables().relations();
                    // end::explainables[]
                    // tag::explain[]
                    explainable_relations.forEach(explainable -> {
                        Stream<Explanation> explain_iterator = tx.query().explain(explainable.second());
                    // end::explain[]
                        System.out.println("Explainable variable:" + explainable.first());
                        System.out.println("Explainable part of the query:" + explainable.second().conjunction());

                        // tag::explanation[]
                        explain_iterator.forEach(explanation -> {
                            System.out.println("Rule: " + explanation.rule().getLabel());
                            System.out.println("  Condition: " + explanation.rule().getWhen().toString());
                            System.out.println("  Conclusion: " + explanation.rule().getThen().toString());
                            explanation.queryVariables().forEach(var ->
                                System.out.println("Query variable " + var + "maps to the rule variable " + explanation.queryVariableMapping(var)));
                        });
                        // end::explanation[]
                    // tag::explain[]
                    });
                    // end::explain[]
                // tag::explainables[]
                });
                // end::explainables[]
            }
        }
        driver.close();
    }
}

