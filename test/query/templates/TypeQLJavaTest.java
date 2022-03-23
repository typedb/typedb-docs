package com.vaticle.doc.test.query;


import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typeql.lang.TypeQL;
import com.vaticle.typeql.lang.query.TypeQLQuery;
import com.vaticle.typeql.lang.query.TypeQLDefine;
import com.vaticle.typeql.lang.query.TypeQLUndefine;
import com.vaticle.typeql.lang.query.TypeQLMatch;
import com.vaticle.typeql.lang.query.TypeQLDelete;
import com.vaticle.typeql.lang.query.TypeQLInsert;
import com.vaticle.typeql.lang.query.TypeQLUpdate;
import com.vaticle.typeql.lang.pattern.Pattern;
import com.vaticle.typeql.lang.common.TypeQLArg;
import com.vaticle.typedb.client.api.answer.ConceptMap;
import com.vaticle.typedb.client.api.answer.ConceptMapGroup;
import com.vaticle.typedb.client.api.answer.Numeric;
import com.vaticle.typedb.client.api.answer.NumericGroup;
import org.junit.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import static com.vaticle.typeql.lang.common.TypeQLArg.Algorithm.*;
import static com.vaticle.typeql.lang.common.TypeQLArg.Order.*;
import static com.vaticle.typeql.lang.TypeQL.*;

public class TypeQLJavaTest {
    static TypeDBClient client;
    static TypeDBSession session;
    TypeDBTransaction transaction;

    private void runQuery(TypeQLQuery query) {
        List<ConceptMap> conceptMaps;
        Numeric num;
        try {
            if (query instanceof TypeQLMatch) {
                session = client.session("social_network", TypeDBSession.Type.DATA);
                transaction = session.transaction(TypeDBTransaction.Type.WRITE);
                conceptMaps = transaction.query().match(query.asMatch()).collect(Collectors.toList());
            } else if (query instanceof TypeQLMatch.Aggregate) {
                session = client.session("social_network", TypeDBSession.Type.DATA);
                transaction = session.transaction(TypeDBTransaction.Type.WRITE);
                transaction.query().match(query.asMatchAggregate()).get();
            } else if (query instanceof TypeQLMatch.Group) {
                session = client.session("social_network", TypeDBSession.Type.DATA);
                transaction = session.transaction(TypeDBTransaction.Type.WRITE);
                List<ConceptMapGroup> x = transaction.query().match(query.asMatchGroup()).collect(Collectors.toList());
            } else if (query instanceof TypeQLMatch.Aggregate) {
                session = client.session("social_network", TypeDBSession.Type.DATA);
                transaction = session.transaction(TypeDBTransaction.Type.READ);
                num = transaction.query().match(query.asMatchAggregate()).get();
            } else if (query instanceof TypeQLMatch.Group.Aggregate) {
                session = client.session("social_network", TypeDBSession.Type.DATA);
                transaction = session.transaction(TypeDBTransaction.Type.WRITE);
                List<NumericGroup> x = transaction.query().match(query.asMatchGroupAggregate()).collect(Collectors.toList());

            } else if (query instanceof TypeQLDefine) {
                session = client.session("social_network", TypeDBSession.Type.SCHEMA);
                transaction = session.transaction(TypeDBTransaction.Type.WRITE);
                transaction.query().define(query.asDefine()).get();

            } else if (query instanceof TypeQLUndefine) {
                session = client.session("social_network", TypeDBSession.Type.SCHEMA);
                transaction = session.transaction(TypeDBTransaction.Type.WRITE);
                transaction.query().undefine(query.asUndefine()).get();

            } else if (query instanceof TypeQLInsert) {
                session = client.session("social_network", TypeDBSession.Type.DATA);
                transaction = session.transaction(TypeDBTransaction.Type.WRITE);
                conceptMaps = transaction.query().insert(query.asInsert()).collect(Collectors.toList());

            } else if (query instanceof TypeQLDelete) {
                session = client.session("social_network", TypeDBSession.Type.DATA);
                transaction = session.transaction(TypeDBTransaction.Type.WRITE);
                transaction.query().delete(query.asDelete()).get();
            } else if (query instanceof TypeQLUpdate) {
                session = client.session("social_network", TypeDBSession.Type.DATA);
                transaction = session.transaction(TypeDBTransaction.Type.WRITE);
                conceptMaps = transaction.query().update(query.asUpdate()).collect(Collectors.toList());
            } else {
                throw new RuntimeException("Unknown query type: " + query.toString() + "[type = " + query.getClass() + "]");
            }
        } finally {
            if (transaction != null) {
                transaction.close();
            }
            if (session != null) {
                session.close();
            }
        }
    }


    @BeforeClass
    public static void loadSocialNetwork() throws Exception {
        String address = "localhost:1729";

        client = TypeDB.coreClient(address);
        client.databases().create("social_network");
        session = client.session("social_network", TypeDBSession.Type.SCHEMA);
        TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE);

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.tql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(TypeQL.parseQuery(query)).get();

            encoded = Files.readAllBytes(Paths.get("files/phone-calls/schema.tql"));
            query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(TypeQL.parseQuery(query)).get();

            encoded = Files.readAllBytes(Paths.get("files/negation/schema.tql"));
            query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(TypeQL.parseQuery(query)).get();

            transaction.commit();
        } catch (IOException e) {
            e.printStackTrace();
        }
        session.close();
    }

    @AfterClass
    public static void closeSession() throws Exception {
        client.databases().get("social_network").delete();
    }

    // TEST METHODS PLACEHOLDER
}
