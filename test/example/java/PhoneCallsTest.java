package grakn.doc.test.example;


import grakn.client.GraknClient;
import graql.lang.Graql;
import graql.lang.common.GraqlArg;
import graql.lang.query.builder.Sortable;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.FixMethodOrder;
import org.junit.Test;
import org.junit.runners.MethodSorters;

import javax.xml.stream.XMLStreamException;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class PhoneCallsTest {

    @BeforeClass
    public static void loadPhoneCalls() {
        GraknClient client = GraknClient.core("localhost:1729");
        client.databases().create("phone_calls");
        GraknClient.Session session = client.session("phone_calls", GraknClient.Session.Type.SCHEMA);
        GraknClient.Transaction transaction = session.transaction(GraknClient.Transaction.Type.WRITE);


        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/phone-calls/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(Graql.parseQuery(query));
            transaction.commit();
            session.close();
            client.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testAPhoneCallsFirstQuery() {
        PhoneCallsFirstQuery.main(new String[]{});
    }

    @Test
    public void testBPhoneCallsSecondQuery() {
        PhoneCallsSecondQuery.main(new String[]{});
    }

    @Test
    public void testCPhoneCallsThirdQuery() {
        PhoneCallsSecondQuery.main(new String[]{});
    }

    @Test
    public void testDPhoneCallsForthQuery() {
        PhoneCallsForthQuery.main(new String[]{});
    }

    @Test
    public void testEPhoneCallsFifthQuery() {
        PhoneCallsFifthQuery.main(new String[]{});
    }

    @Test
    public void testFPhoneCallsCSVMigration() throws FileNotFoundException {
        PhoneCallsCSVMigration.main(new String[]{});
    }

    @Test
    public void testGPhoneCallsJSONMigration() throws IOException {
        PhoneCallsJSONMigration.main(new String[]{});
    }

    @Test
    public void testHPhoneCallsXMLMigration() throws FileNotFoundException, XMLStreamException {
        PhoneCallsXMLMigration.main(new String[]{});
    }

    @AfterClass
    public static void cleanPhoneCalls() {
        GraknClient client = GraknClient.core("localhost:1729");
        client.databases().get("phone_calls").delete();
        client.close();
    }
}