package grakn.doc.test.example;

import grakn.client.Grakn;
import grakn.client.rpc.GraknClient;
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
        Grakn.Client client = new GraknClient("localhost:1729");
        Grakn.Session session = client.session("social_network", Grakn.Session.Type.DATA);
        Grakn.Transaction transaction = session.transaction(Grakn.Transaction.Type.WRITE);
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
        Grakn.Client client = new GraknClient("localhost:1729");
        client.databases().delete("social_network");
        System.out.println("Deleted the social_network database");
    }
}