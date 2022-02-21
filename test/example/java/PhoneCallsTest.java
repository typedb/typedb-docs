package com.vaticle.doc.test.example;


import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typeql.lang.TypeQL;
import com.vaticle.typeql.lang.common.TypeQLArg;
import com.vaticle.typeql.lang.query.builder.Sortable;
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
        TypeDBClient client = TypeDB.coreClient("localhost:1729");
        client.databases().create("phone_calls");
        TypeDBSession session = client.session("phone_calls", TypeDBSession.Type.SCHEMA);
        TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE);

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/phone-calls/schema.tql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.query().define(TypeQL.parseQuery(query));
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
        TypeDBClient client = TypeDB.coreClient("localhost:1729");
        client.databases().get("phone_calls").delete();
        client.close();
    }
}
