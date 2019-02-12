package generated;

import grakn.core.client.GraknClient;
import grakn.core.graql.query.Graql;
import grakn.core.graql.query.query.GraqlQuery;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.junit.Before;
import org.junit.FixMethodOrder;
import org.junit.Test;
import org.junit.runners.MethodSorters;

@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class TestStandaloneSocialNetwork {

    @Before
    public void loadSocialNetwork() {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("social_network");
        GraknClient.Transaction transaction = session.transaction(GraknClient.Transaction.Type.WRITE);

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((GraqlQuery) Graql.parse(query));
            transaction.commit();
            session.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testASocialNetworkQuery() {
        SocialNetworkQuery.main(new String[]{});
    }
}