package grakn.doc.test.query;

import grakn.client.Grakn;
import grakn.client.GraknClient;
import graql.lang.Graql;
import graql.lang.query.GraqlQuery;
import graql.lang.query.GraqlCompute;
import graql.lang.query.GraqlDefine;
import graql.lang.query.GraqlUndefine;
import graql.lang.query.GraqlMatch;
import graql.lang.query.GraqlDelete;
import graql.lang.query.GraqlInsert;
import graql.lang.query.GraqlCompute.Argument;
import graql.lang.pattern.Pattern;
import graql.lang.common.GraqlArg;
import grakn.client.concept.answer.ConceptMap;
import org.junit.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

import static graql.lang.common.GraqlArg.Algorithm.*;
import static graql.lang.common.GraqlArg.Order.*;
import static graql.lang.query.GraqlCompute.Argument.*;
import static graql.lang.query.GraqlCompute.Argument.*;
import static graql.lang.Graql.*;

public class GraqlJavaTest {
    static Grakn.Client client;
    static Grakn.Session session ;
    Grakn.Transaction transaction;

    private void runQuery(Grakn.Transaction transaction, GraqlQuery query) {
        List<ConceptMap> conceptMaps;
        if (query instanceof GraqlMatch) {
            conceptMaps = transaction.query().match(query.asMatch()).collect(Collectors.toList());
        } else if (query instanceof GraqlDefine) {
            transaction.query().define(query.asDefine()).get();
        } else if (query instanceof GraqlInsert) {
            conceptMaps = transaction.query().insert(query.asInsert()).collect(Collectors.toList());
        } else if (query instanceof GraqlDelete) {
            transaction.query().delete(query.asDelete()).get();
        } else {
            throw new RuntimeException("Unknown query type: " + query.toString());
        }
    }


    @BeforeClass
    public static void loadSocialNetwork() throws Exception {
//        GraknSetup.bootup();
        String address = "localhost:1729";

        client = new GraknClient(address);
        session = client.session("social_network", Grakn.Session.Type.SCHEMA);
        Grakn.Transaction transaction = session.transaction(Grakn.Transaction.Type.WRITE);

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(Graql.parseQuery(query));

            encoded = Files.readAllBytes(Paths.get("files/phone-calls/schema.gql"));
            query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(Graql.parseQuery(query));

            transaction.commit();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Before
    public void openTransaction(){
        transaction = session.transaction(Grakn.Transaction.Type.WRITE);
    }

    @After
    public void closeTransaction(){
        transaction.close();
    }

    @AfterClass
    public static void closeSession() throws Exception {
        session.close();
//        GraknSetup.shutdown();
    }

    // TEST METHODS PLACEHOLDER
}
