package grakn.doc.test.query;

import grakn.client.Grakn;
import grakn.client.GraknClient;
import grakn.client.concept.answer.ConceptMap;
import grakn.client.concept.answer.ConceptMapGroup;
import grakn.client.concept.answer.Numeric;
import grakn.client.concept.answer.NumericGroup;
import graql.lang.Graql;
import graql.lang.pattern.Pattern;
import graql.lang.query.*;
import org.junit.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;
import java.util.stream.Collectors;
import java.util.List;

public class GraqlLangTest {
    static Grakn.Client client;
    static Grakn.Session session;
    Grakn.Transaction transaction;

    private void runQuery(Grakn.Transaction transaction, GraqlQuery query) {
        List<ConceptMap> conceptMaps;
        Numeric num;
        if (query instanceof GraqlMatch) {
            session = client.session("social_network", Grakn.Session.Type.DATA);
            transaction = session.transaction(Grakn.Transaction.Type.WRITE);
            conceptMaps = transaction.query().match(query.asMatch()).collect(Collectors.toList());
            transaction.close();
            session.close();
        } else if (query instanceof GraqlMatch.Aggregate) {
            session = client.session("social_network", Grakn.Session.Type.DATA);
            transaction = session.transaction(Grakn.Transaction.Type.WRITE);
            transaction.query().match(query.asMatchAggregate()).get();
            transaction.close();
            session.close();
        } else if (query instanceof GraqlMatch.Group) {
            session = client.session("social_network", Grakn.Session.Type.DATA);
            transaction = session.transaction(Grakn.Transaction.Type.WRITE);
            List<ConceptMapGroup> x = transaction.query().match(query.asMatchGroup()).collect(Collectors.toList());
            transaction.close();
            session.close();
        } else if (query instanceof GraqlMatch.Aggregate) {
            session = client.session("social_network", Grakn.Session.Type.DATA);
            transaction = session.transaction(Grakn.Transaction.Type.WRITE);
            num = transaction.query().match(query.asMatchAggregate()).get();
            transaction.close();
            session.close();
        } else if (query instanceof GraqlMatch.Group.Aggregate) {
            session = client.session("social_network", Grakn.Session.Type.DATA);
            transaction = session.transaction(Grakn.Transaction.Type.WRITE);
            List<NumericGroup> x = transaction.query().match(query.asMatchGroupAggregate()).collect(Collectors.toList());
            transaction.close();
            session.close();
        } else if (query instanceof GraqlDefine) {
            session = client.session("social_network", Grakn.Session.Type.SCHEMA);
            transaction = session.transaction(Grakn.Transaction.Type.WRITE);
            transaction.query().define(query.asDefine()).get();
            transaction.close();
            session.close();
        } else if (query instanceof GraqlUndefine) {
            session = client.session("social_network", Grakn.Session.Type.SCHEMA);
            transaction = session.transaction(Grakn.Transaction.Type.WRITE);
            transaction.query().undefine(query.asUndefine()).get();
            transaction.close();
            session.close();
        } else if (query instanceof GraqlInsert) {
            session = client.session("social_network", Grakn.Session.Type.DATA);
            transaction = session.transaction(Grakn.Transaction.Type.WRITE);
            conceptMaps = transaction.query().insert(query.asInsert()).collect(Collectors.toList());
            transaction.close();
            session.close();
        } else if (query instanceof GraqlDelete) {
            session = client.session("social_network", Grakn.Session.Type.DATA);
            transaction = session.transaction(Grakn.Transaction.Type.WRITE);
            transaction.query().delete(query.asDelete()).get();
            transaction.close();
            session.close();
        } else if (query instanceof GraqlCompute) {
            // FIXME(vmax): we dunno how to run them yet
        } else {
            throw new RuntimeException("Unknown query type: " + query.toString() + "[type = " + query.getClass() + "]");
        }
    }


    @BeforeClass
    public static void loadSocialNetwork() throws Exception {
        String address = "localhost:1729";

        client = GraknClient.core(address);
        client.databases().create("social_network");
        session = client.session("social_network", Grakn.Session.Type.SCHEMA);
        Grakn.Transaction transaction = session.transaction(Grakn.Transaction.Type.WRITE);

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(Graql.parseQuery(query)).get();

            encoded = Files.readAllBytes(Paths.get("files/phone-calls/schema.gql"));
            query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(Graql.parseQuery(query)).get();

            encoded = Files.readAllBytes(Paths.get("files/negation/schema.gql"));
            query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(Graql.parseQuery(query)).get();

            transaction.commit();
        } catch (IOException e) {
            e.printStackTrace();
        }
        session.close();
    }

    @AfterClass
    public static void closeSession() throws Exception {
        client.databases().delete("social_network");
    }

    // TEST METHODS PLACEHOLDER
}
