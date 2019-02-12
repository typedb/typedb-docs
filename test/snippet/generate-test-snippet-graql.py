import re
import sys

generated_test_path, markdown_files = sys.argv[1], sys.argv[2:]

graql_snippet_test_class_template = """
package generated;

import grakn.core.client.GraknClient;
import grakn.core.rule.GraknTestServer;
import grakn.core.server.Transaction;
import org.junit.*;

import grakn.core.graql.query.Graql;
import grakn.core.graql.query.query.GraqlQuery;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;

public class TestSnippetGraql {
    @ClassRule
    public static final GraknTestServer server = new GraknTestServer(
        Paths.get("test/grakn-test-server/conf/grakn.properties"), 
        Paths.get("test/grakn-test-server/conf/cassandra-embedded.yaml")
    );

    static GraknClient client;
    static GraknClient.Session session;
    GraknClient.Transaction transaction;


    @BeforeClass
    public static void loadSocialNetwork() {
        client = new GraknClient(server.grpcUri().toString());
        session = client.session("social_network");
        GraknClient.Transaction transaction = session.transaction(Transaction.Type.WRITE);

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((GraqlQuery) Graql.parse(query));
            transaction.commit();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Before
    public void openTransaction() {
        transaction = session.transaction(Transaction.Type.WRITE);
    }

    @After
    public void abortTransaction() {
        transaction.abort();
    }

    @AfterClass
    public static void closeSession() {
        session.close();
    }

    // TEST METHODS PLACEHOLDER
}
"""

graql_snippet_test_method_template = """
    @Test
    public void test() {
        // PAGE COMMENT PLACEHOLDER
        String queries = "// QUERIES PLACEHOLDER";
        Stream<GraqlQuery> parsedQuery = Graql.parseList(queries);
        parsedQuery.forEach(query -> transaction.execute(query));
    }
"""

pattern_to_find_snippets = ('<!-- test-(ignore|standalone.*) -->\n```graql\n((\n|.)+?)```'
                            +
                            '|(```graql\n' +
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

    # turn into a singe line + remove comments + escape double quotes
    graql_lines = []
    for line in snippet.get("code").split("\n"):
        line = line.replace("\t", "")
        if "#" not in line:
            graql_lines.append(line.replace('"', "\\\""))
    final_snippet = " ".join(graql_lines)

    test_method = graql_snippet_test_method_template.replace("// PAGE COMMENT PLACEHOLDER", "// " + snippet.get("page"))  # change method name
    test_method = test_method.replace("test() {", "test_" + str(i) + "() {")  # change page name comment
    test_method = test_method.replace("// QUERIES PLACEHOLDER", final_snippet)  # add query objects
    test_methods += test_method

graql_snippet_test_class = graql_snippet_test_class_template.replace("// TEST METHODS PLACEHOLDER", test_methods)

with open(generated_test_path, "w") as generated_test_file:
    generated_test_file.write(graql_snippet_test_class)
