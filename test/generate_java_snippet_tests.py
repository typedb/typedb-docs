import re
import sys

generated_test_path, markdown_files = sys.argv[1], sys.argv[2:]

java_snippet_test_class_template = """
package generated;

import grakn.core.client.GraknClient;
import grakn.core.rule.GraknTestServer;
import grakn.core.server.Transaction;
import org.junit.*;

import grakn.core.graql.query.*;

import static grakn.core.graql.query.Graql.*;

import static grakn.core.graql.query.ComputeQuery.Method.*;
import static grakn.core.graql.query.ComputeQuery.Algorithm.*;
import static grakn.core.graql.query.ComputeQuery.Argument.*;
import grakn.core.graql.query.Query.DataType;

import grakn.core.graql.concept.ConceptId;

import grakn.core.graql.answer.ConceptSet;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDate;

public class JavaSnippetTest {
    @ClassRule
    public static final GraknTestServer server = new GraknTestServer(
        "test/grakn-test-server/conf/grakn.properties", 
        "test/grakn-test-server/conf/cassandra-embedded.yaml"
    );

    static GraknClient client;
    static GraknClient.Session session ;
    GraknClient.Transaction transaction;


    @BeforeClass
    public static void loadSocialNetwork() {
        client = new GraknClient(server.grpcUri().toString());
        session = client.session("social_network");
        GraknClient.Transaction transaction = session.transaction(Transaction.Type.WRITE);

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network-schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((Query) Graql.parse(query));
            transaction.commit();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Before
    public void openTransaction(){
        transaction = session.transaction(Transaction.Type.WRITE);
    }

    @After
    public void abortTransaction(){
        transaction.abort();
    }

    @AfterClass
    public static void closeSession() {
        session.close();
    }

    // TEST METHODS PLACEHOLDER
}
"""

java_snippet_test_method_template = """
    @Test
    public void test() {
        // PAGE COMMENT PLACEHOLDER
        // QUERY OBJECTS PLACEHOLDER
        // EXECUTE PLACEHOLDER
    }
"""

# pattern_to_find_snippets = '(?<!<!-- test-ignore -->)\n```java\n((\n|.)+?)```'

pattern_to_find_snippets = ('<!-- test-(ignore|standalone.*) -->\n```java\n((\n|.)+?)```'
                            +
                            '|(```java\n' +
                            '((\n|.)+?)' +  # group containing snippet
                            '```)')

snippets = []
for markdown_file in markdown_files:
    with open(markdown_file) as file:
        matches = re.findall(pattern_to_find_snippets, file.read())
        for snippet in matches:
            flag_type = snippet[0]
            if "ignore" not in flag_type and "standalone" not in flag_type:
                snippets.append({"code": snippet[4], "page": markdown_file})


test_methods = ""
for i, snippet in enumerate(snippets):
    test_method = java_snippet_test_method_template.replace("// PAGE COMMENT PLACEHOLDER", "// " + snippet.get("page"))  # change method name
    test_method = test_method.replace("test() {", "test_" + str(i) + "() {")  # change page name comment
    test_method = test_method.replace("// QUERY OBJECTS PLACEHOLDER", snippet.get("code"))  # add query objects

    # add execute statements
    pattern_to_find_query_object_vars = 'Query\s(.*)\s='
    matches = re.findall(pattern_to_find_query_object_vars, snippet.get("code"))
    execute_statements = ""
    for variable in matches:
        execute_statements += "transaction.execute(" + variable + ");\n"

    test_method = test_method.replace("// EXECUTE PLACEHOLDER", execute_statements)
    test_methods += test_method

test_methods = test_methods.replace("&lt;", "<").replace("&gt;", ">")

java_snippet_test_class = java_snippet_test_class_template.replace("// TEST METHODS PLACEHOLDER", test_methods)


with open(generated_test_path, "w") as generated_test_file:
    generated_test_file.write(java_snippet_test_class)
