import re
import sys
from io import open

typeql_java_test_template_path, output_path, markdown_files = sys.argv[1], sys.argv[2], sys.argv[3:]

typeql_java_test_template = open(typeql_java_test_template_path, 'r').read()

typeql_java_test_method_template = """
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
        test_name = "test__{0}__typeql_java__{1}".format(page, i)
        test_method = typeql_java_test_method_template.replace("// PAGE COMMENT PLACEHOLDER", "// " + snippet.get("page"))  # change method name
        test_method = test_method.replace("test() {", test_name + "() {")  # change page name comment
        test_method = test_method.replace("// QUERY OBJECTS PLACEHOLDER", snippet.get("code"))  # add query objects

        # add execute statements
        pattern_to_find_query_object_vars = '^TypeQL[A-Z].*?\s(.*)\s='
        matches = re.findall(pattern_to_find_query_object_vars, snippet.get("code"))
        execute_statements = ""
        for variable in matches:
            execute_statements += "runQuery(" + variable + ");\n"

        test_method = test_method.replace("// EXECUTE PLACEHOLDER", execute_statements)
        test_methods += test_method

test_methods = test_methods.replace("&lt;", "<").replace("&gt;", ">")

typeql_java_test_class = typeql_java_test_template.replace("// TEST METHODS PLACEHOLDER", test_methods)


with open(output_path, "w") as output_file:
    output_file.write(typeql_java_test_class)
