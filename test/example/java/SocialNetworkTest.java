package com.vaticle.doc.test.example;

import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typeql.lang.TypeQL;
import com.vaticle.typeql.lang.common.TypeQLArg;
import com.vaticle.typeql.lang.query.TypeQLQuery;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;

import static com.vaticle.typeql.lang.TypeQL.*;

import org.junit.*;

public class SocialNetworkTest {

    @BeforeClass
    public static void loadSocialNetwork() {
        TypeDBClient client = TypeDB.coreClient("localhost:1729");
        client.databases().create("social_network");
        TypeDBSession session = client.session("social_network", TypeDBSession.Type.SCHEMA);
        TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE);
        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.tql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(TypeQL.parseQuery(query));
            transaction.commit();
            session.close();
            System.out.println("Loaded the social_network schema");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testSocialNetworkQuickstartQuery() { SocialNetworkQuickstartQuery.main(new String[]{}); }

    @Test
    public void testTypeDBQuickstartA() { TypeDBQuickstartA.main(new String[]{}); }

    @Test
    public void testTypeDBQuickstartB() { TypeDBQuickstartB.main(new String[]{}); }

    @Test
    public void testTypeDBQuickstartC() { TypeDBQuickstartC.main(new String[]{}); }

    @AfterClass
    public static void cleanSocialNetwork() {
        TypeDBClient client = TypeDB.coreClient("localhost:1729");
        client.databases().get("social_network").delete();
        System.out.println("Deleted the social_network database");
    }
}