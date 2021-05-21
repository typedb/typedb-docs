import re
import sys
from io import open

typeql_lang_test_template_path, output_path, markdown_files = sys.argv[1], sys.argv[2], sys.argv[3:]

typeql_lang_test_template = open(typeql_lang_test_template_path, 'r').read()

typeql_lang_test_method_template = """
    @Test
    public void test() {
        // PAGE COMMENT PLACEHOLDER
        String queries = "// QUERIES PLACEHOLDER";
        Stream<TypeQLQuery> parsedQuery = TypeQL.parseQueries(queries);
        parsedQuery.forEach(query -> {
            System.err.println("before executing in test()" + query);
           runQuery(query);
           System.err.println("after executing in test()" + query);
        });
    }
"""

typeql_lang_pattern_test_method_template = """
    @Test
    public void test() {
        // PAGE COMMENT PLACEHOLDER
        String queries = "// QUERIES PLACEHOLDER";
        Pattern pattern = TypeQL.parsePattern(queries);
    }
"""

pattern_to_find_snippets = ('<!-- test-(delay|ignore|example.*) -->\n```typeql\n((\n|.)+?)```'
                            +
                            '|(```typeql\n' +
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
        test_name = "test__{0}__typeql_native__{1}".format(page, i)
        # turn into a singe line + remove comments + escape double quotes
        typeql_lines = []
        for line in snippet.get("code").split("\n"):
            line = line.replace("\t", "")
            if "#" not in line:
                typeql_lines.append(line.replace('"', "\\\""))
        final_snippet = " ".join(typeql_lines)

        keywords =["match", "define", "insert", "compute"]
        if any(keyword in final_snippet for keyword in keywords):
            test_method = typeql_lang_test_method_template.replace("// PAGE COMMENT PLACEHOLDER", "// " + snippet.get("page"))  # change method name
        else:
            test_method = typeql_lang_pattern_test_method_template.replace("// PAGE COMMENT PLACEHOLDER", "// " + snippet.get("page"))  # change method name

        test_method = test_method.replace("test()", test_name + "()")  # change page name comment
        test_method = test_method.replace("// QUERIES PLACEHOLDER", final_snippet)  # add  objects
        test_methods += test_method

typeql_lang_test_class = typeql_lang_test_template.replace("// TEST METHODS PLACEHOLDER", test_methods)

with open(output_path, "w") as output_file:
    output_file.write(typeql_lang_test_class)
