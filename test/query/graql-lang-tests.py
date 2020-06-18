import re
import sys
from io import open

output_path, markdown_files = sys.argv[1], sys.argv[2:]

graql_lang_test_template = """
package grakn.doc.test.query;

import grakn.client.GraknClient;
import grakn.core.test.rule.GraknTestServer;
import graql.lang.Graql;
import graql.lang.pattern.Pattern;
import graql.lang.query.GraqlQuery;
import org.junit.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;

public class GraqlLangTest {
    @ClassRule
    public static final GraknTestServer server = new GraknTestServer(
        Paths.get("external/graknlabs_grakn_core/server/conf/grakn.properties"),
        Paths.get("test/conf/cassandra-embedded.yaml")
    );

    static GraknClient client;
    static GraknClient.Session session;
    GraknClient.Transaction transaction;


    @BeforeClass
    public static void loadSocialNetwork() {
        client = new GraknClient(server.grpcUri().toString());
        session = client.session("social_network");
        GraknClient.Transaction transaction = session.transaction().write();

        try {
            byte[] encoded = Files.readAllBytes(Paths.get("files/social-network/schema.gql"));
            String query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((GraqlQuery) Graql.parse(query)).get();

            encoded = Files.readAllBytes(Paths.get("files/phone-calls/schema.gql"));
            query = new String(encoded, StandardCharsets.UTF_8);
            transaction.execute((GraqlQuery) Graql.parse(query)).get();

            transaction.commit();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Before
    public void openTransaction() {
        transaction = session.transaction().write();
    }

    @After
    public void closeTransaction() {
        transaction.close();
    }

    @AfterClass
    public static void closeSession() {
        session.close();
    }

    // TEST METHODS PLACEHOLDER
}
"""

graql_lang_test_method_template = """
    @Test
    public void test() {
        // PAGE COMMENT PLACEHOLDER
        String queries = "// QUERIES PLACEHOLDER";
        Stream<GraqlQuery> parsedQuery = Graql.parseList(queries);
        parsedQuery.forEach(query -> transaction.execute(query).get());
    }
"""

graql_lang_pattern_test_method_template = """
    @Test
    public void test() {
        // PAGE COMMENT PLACEHOLDER
        String queries = "// QUERIES PLACEHOLDER";
        Pattern pattern = Graql.parsePattern(queries);
    }
"""

pattern_to_find_snippets = ('<!-- test-(delay|ignore|example.*) -->\n```graql\n((\n|.)+?)```'
                            +
                            '|(```graql\n' +
                            '((\n|.)+?)' +  # group containing snippet
                            '```)')

snippets = []
for markdown_file in markdown_files:
    snippets.append([])
    with open(markdown_file, encoding='utf-8') as file:
        matches = re.findall(pattern_to_find_snippets, file.read())
        for snippet in matches:
            flag_type = snippet[0]
            if snippet[4] != "":
                snippets[-1].append({"code": snippet[4], "page": markdown_file})


test_methods = ""
for snippets_in_page in snippets:
    for i, snippet in enumerate(snippets_in_page):
        page = snippet["page"]
        page = page.replace("/", "__").replace("-","_").split(".")[0]
        test_name = "test__{0}__graql_native__{1}".format(page, i)
        # turn into a singe line + remove comments + escape double quotes
        graql_lines = []
        for line in snippet.get("code").split("\n"):
            line = line.replace("\t", "")
            if "#" not in line:
                graql_lines.append(line.replace('"', "\\\""))
        final_snippet = " ".join(graql_lines)

        keywords =["match", "define", "insert", "compute"]
        if any(keyword in final_snippet for keyword in keywords):
            test_method = graql_lang_test_method_template.replace("// PAGE COMMENT PLACEHOLDER", "// " + snippet.get("page"))  # change method name
        else:
            test_method = graql_lang_pattern_test_method_template.replace("// PAGE COMMENT PLACEHOLDER", "// " + snippet.get("page"))  # change method name

        test_method = test_method.replace("test() {", test_name + "() {")  # change page name comment
        test_method = test_method.replace("// QUERIES PLACEHOLDER", final_snippet)  # add  objects
        test_methods += test_method

graql_lang_test_class = graql_lang_test_template.replace("// TEST METHODS PLACEHOLDER", test_methods)

with open(output_path, "w") as output_file:
    output_file.write(graql_lang_test_class)
