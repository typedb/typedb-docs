import re
import sys

generated_test_path, markdown_files = sys.argv[1], sys.argv[2:]

java_snippet_test_class_template = """
package generated;

import grakn.core.client.GraknClient;
import grakn.core.rule.GraknTestServer;
import grakn.core.server.Transaction;
import org.junit.Test;
import org.junit.ClassRule;

import grakn.core.graql.query.*;

import static grakn.core.graql.query.Graql.var;
import static grakn.core.graql.query.Graql.type;
import static grakn.core.graql.query.Graql.and;
import static grakn.core.graql.query.Graql.or;


import static grakn.core.graql.query.ComputeQuery.Method.*;
import static grakn.core.graql.query.ComputeQuery.Algorithm.*;
import static grakn.core.graql.query.ComputeQuery.Argument.*;
import static grakn.core.graql.query.predicate.Predicates.*;
import grakn.core.graql.query.Query.DataType;

import grakn.core.graql.concept.ConceptId;

import grakn.core.graql.answer.ConceptSet;

import java.time.LocalDate;

public class JavaSnippetTest {
    @ClassRule
    public static final GraknTestServer server = new GraknTestServer();

    // TEST METHODS PLACEHOLDER
}
"""

java_snippet_test_method_template = """
    @Test
    public void test() {
        try (GraknClient.Transaction transaction = new GraknClient(server.grpcUri().toString()).session("grakn").transaction(Transaction.Type.WRITE)) {
            // QUERY OBJECTS PLACEHOLDER
            // EXECUTE PLACEHOLDER
        }
    }
"""

pattern_to_find_snippets = '(?<!<!-- ignore-test -->\n)```java\n((\n|.)+?)```'


snippets = []
for markdown_file in markdown_files:
    with open(markdown_file) as file:
        matches = re.findall(pattern_to_find_snippets, file.read())
        for snippet in matches:
            snippets.append(snippet[0])


test_methods = ""
for i, snippet in enumerate(snippets):
    test_method = java_snippet_test_method_template.replace("test() {", "test_" + str(i) + "() {")  # change method name
    test_method = test_method.replace("// QUERY OBJECTS PLACEHOLDER", snippet)  # add query objects

    # add execute statements
    pattern_to_find_query_object_vars = 'Query\s(.*)\s='
    matches = re.findall(pattern_to_find_query_object_vars, snippet)
    execute_statements = ""
    for variable in matches:
        execute_statements += "transaction.execute(" + variable + ");\n"

    test_method = test_method.replace("// EXECUTE PLACEHOLDER", execute_statements)
    test_methods += test_method

java_snippet_test_class = java_snippet_test_class_template.replace("// TEST METHODS PLACEHOLDER", test_methods)

with open(generated_test_path, "w") as generated_test_file:
    generated_test_file.write(java_snippet_test_class)
