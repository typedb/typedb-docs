import re
import sys
from io import open

output_path, markdown_files = sys.argv[1], sys.argv[2:]

graql_java_test_template = """
package grakn.doc.test.query;

import grakn.client.GraknClient;
import grakn.core.rule.GraknTestServer;

import graql.lang.Graql;
import graql.lang.query.GraqlQuery;
import graql.lang.query.GraqlCompute;
import graql.lang.query.GraqlDefine;
import graql.lang.query.GraqlUndefine;
import graql.lang.query.GraqlGet;
import graql.lang.query.GraqlDelete;
import graql.lang.query.GraqlInsert;
import graql.lang.query.GraqlCompute.Argument;
import graql.lang.pattern.Pattern;
import org.junit.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDate;

import static graql.lang.Graql.*;
import static graql.lang.Graql.Token.Compute.Algorithm.*;
import static graql.lang.Graql.Token.Order.*;
import static graql.lang.query.GraqlCompute.Argument.*;

public class GraqlJavaTest {
    @ClassRule
    public static final GraknTestServer server = new GraknTestServer(
        Paths.get("external/graknlabs_grakn_core/server/conf/grakn.properties"), 
        Paths.get("test/conf/cassandra-embedded.yaml")
    );

    static GraknClient client;
    static GraknClient.Session session ;
    GraknClient.Transaction transaction;


    @BeforeClass
    public static void loadSocialNetwork() {
        client = new GraknClient(server.grpcUri().toString());
        session = client.session("social_network");
        GraknClient.Transaction transaction = session.transaction().write();

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((GraqlQuery) Graql.parse(query));
            
            encoded = Files.readAllBytes(Paths.get("files/phone-calls/schema.gql"));
            query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((GraqlQuery) Graql.parse(query));
            
            transaction.commit();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Before
    public void openTransaction(){
        transaction = session.transaction().write();
    }

    @After
    public void closeTransaction(){
        transaction.close();
    }

    @AfterClass
    public static void closeSession() {
        session.close();
    }

    // TEST METHODS PLACEHOLDER
}
"""

graql_java_test_method_template = """
    @Test
    public void test() {
        // PAGE COMMENT PLACEHOLDER
        // QUERY OBJECTS PLACEHOLDER
        // EXECUTE PLACEHOLDER
    }
"""

pattern_to_find_snippets = ('<!-- test-(delay|ignore|example.*) -->\n```java\n((\n|.)+?)```'
                            +
                            '|(```java\n' +
                            '((\n|.)+?)' +  # group containing snippet
                            '```)')

snippets = []
for markdown_file in markdown_files:
    with open(markdown_file, encoding='utf-8') as file:
        matches = re.findall(pattern_to_find_snippets, file.read())
        for snippet in matches:
            flag_type = snippet[0]
            if snippet[4] != "":
                snippets.append({"code": snippet[4], "page": markdown_file})


test_methods = ""
for i, snippet in enumerate(snippets):
    test_method = graql_java_test_method_template.replace("// PAGE COMMENT PLACEHOLDER", "// " + snippet.get("page"))  # change method name
    test_method = test_method.replace("test() {", "test_" + str(i) + "() {")  # change page name comment
    test_method = test_method.replace("// QUERY OBJECTS PLACEHOLDER", snippet.get("code"))  # add query objects

    # add execute statements
    pattern_to_find_query_object_vars = '^Graql[A-Z].*?\s(.*)\s='
    matches = re.findall(pattern_to_find_query_object_vars, snippet.get("code"))
    execute_statements = ""
    for variable in matches:
        execute_statements += "transaction.execute(" + variable + ");\n"

    test_method = test_method.replace("// EXECUTE PLACEHOLDER", execute_statements)
    test_methods += test_method

test_methods = test_methods.replace("&lt;", "<").replace("&gt;", ">")

graql_java_test_class = graql_java_test_template.replace("// TEST METHODS PLACEHOLDER", test_methods)


with open(output_path, "w") as output_file:
    output_file.write(graql_java_test_class)
