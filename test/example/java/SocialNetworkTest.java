package grakn.doc.test.example;

import grakn.client.GraknClient;
import graql.lang.Graql;
import graql.lang.common.GraqlArg;
import graql.lang.query.GraqlQuery;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;

import static graql.lang.Graql.*;

import org.junit.*;

public class SocialNetworkTest {

    @BeforeClass
    public static void loadSocialNetwork() {
        GraknClient client = GraknClient.core("localhost:1729");
        client.databases().create("social_network");
        GraknClient.Session session = client.session("social_network", GraknClient.Session.Type.SCHEMA);
        GraknClient.Transaction transaction = session.transaction(GraknClient.Transaction.Type.WRITE);
        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(Graql.parseQuery(query));
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
    public void testGraknQuickstartA() { GraknQuickstartA.main(new String[]{}); }

    @Test
    public void testGraknQuickstartB() { GraknQuickstartB.main(new String[]{}); }

    @Test
    public void testGraknQuickstartC() { GraknQuickstartC.main(new String[]{}); }

    @AfterClass
    public static void cleanSocialNetwork() {
        GraknClient client = GraknClient.core("localhost:1729");
        client.databases().delete("social_network");
        System.out.println("Deleted the social_network database");
    }
}