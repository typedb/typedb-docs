package generated;

import grakn.client.GraknClient;
import graql.lang.Graql;
import graql.lang.query.GraqlQuery;
import grakn.core.rule.GraknTestServer;


import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.junit.*;

public class TestStandaloneSocialNetwork {

    @ClassRule
    public static final GraknTestServer server = new GraknTestServer(
            Paths.get("test/grakn-test-server/conf/grakn.properties"),
            Paths.get("test/grakn-test-server/conf/cassandra-embedded.yaml")
    );

    @BeforeClass
    public static void loadSocialNetwork() {
        GraknClient client = new GraknClient(server.grpcUri().toString());
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
    public void testSocialNetworkQuickstartQuery() {
        String[] args = { server.grpcUri().toString() };
        SocialNetworkQuickstartQuery.main(args);
    }

    @Test
    public void testGraknQuickstartA() {
        String[] args = { server.grpcUri().toString() };
        GraknQuickstartA.main(args);
    }

    @Test
    public void testGraknQuickstartB() {
        String[] args = { server.grpcUri().toString() };
        GraknQuickstartB.main(args);
    }

    @Test
    public void testGraknQuickstartC() {
        String[] args = { server.grpcUri().toString() };
        GraknQuickstartC.main(args);
    }

    @AfterClass
    public static void cleanSocialNetwork() {
        GraknClient client = new GraknClient(server.grpcUri().toString());
        client.keyspaces().delete("social_network");
        System.out.println("Deleted the social_network keyspace");
    }
}