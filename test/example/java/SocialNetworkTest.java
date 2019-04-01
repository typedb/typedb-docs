package grakn.doc.test.example;

import grakn.client.GraknClient;
import graql.lang.Graql;
import graql.lang.query.GraqlQuery;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.junit.*;

public class SocialNetworkTest {

    @BeforeClass
    public static void loadSocialNetwork() {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("social_network");
        GraknClient.Transaction transaction = session.transaction().write();

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((GraqlQuery) Graql.parse(query));
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
        GraknClient client = new GraknClient("localhost:48555");
        client.keyspaces().delete("social_network");
        System.out.println("Deleted the social_network keyspace");
    }
}