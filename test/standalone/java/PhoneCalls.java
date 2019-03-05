package generated;

import grakn.client.GraknClient;
import graql.lang.Graql;
import graql.lang.query.GraqlQuery;
import grakn.core.rule.GraknTestServer;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.junit.*;
import org.junit.runners.MethodSorters;

import javax.xml.stream.XMLStreamException;

@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class TestStandalonePhoneCalls {

    @ClassRule
    public static final GraknTestServer server = new GraknTestServer(
            Paths.get("test/grakn-test-server/conf/grakn.properties"),
            Paths.get("test/grakn-test-server/conf/cassandra-embedded.yaml")
    );

    @BeforeClass
    public static void loadPhoneCalls() {
        GraknClient client = new GraknClient(server.grpcUri().toString());
        GraknClient.Session session = client.session("phone_calls");
        GraknClient.Transaction transaction = session.transaction().write();

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/phone-calls/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((GraqlQuery) Graql.parse(query));
            transaction.commit();
            session.close();
            client.close();
            System.out.println("Loaded the phone_calls schema");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testAPhoneCallsFirtstQuery() {
        String[] args = { server.grpcUri().toString() };
        PhoneCallsFirstQuery.main(args);
    }

    @Test
    public void testBPhoneCallsSecondQuery() {
        String[] args = { server.grpcUri().toString() };
        PhoneCallsSecondQuery.main(args);
    }

    @Test
    public void testCPhoneCallsThirdQuery() {
        String[] args = { server.grpcUri().toString() };
        PhoneCallsSecondQuery.main(args);
    }

    @Test
    public void testDPhoneCallsForthQuery() {
        String[] args = { server.grpcUri().toString() };
        PhoneCallsForthQuery.main(args);
    }

    @Test
    public void testEPhoneCallsFifthQuery() {
        String[] args = { server.grpcUri().toString() };
        PhoneCallsFifthQuery.main(args);
    }

    @Test
    public void testFPhoneCallsCSVMigration() throws FileNotFoundException {
        String[] args = { server.grpcUri().toString() };
        PhoneCallsCSVMigration.main(args);
    }

    @Test
    public void testGPhoneCallsJSONMigration() throws IOException {
        String[] args = { server.grpcUri().toString() };
        PhoneCallsJSONMigration.main(args);
    }

    @Test
    public void testHPhoneCallsXMLMigration() throws FileNotFoundException, XMLStreamException {
        String[] args = { server.grpcUri().toString() };
        PhoneCallsXMLMigration.main(args);
    }

    @AfterClass
    public static void cleanPhoneCalls() {
        GraknClient client = new GraknClient(server.grpcUri().toString());
        client.keyspaces().delete("phone_calls");
        client.close();
        System.out.println("Deleted the phone_calls keyspace");
    }
}