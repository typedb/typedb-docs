import re
import sys

markdown_files = []
generated_test_paths = []
for arg in sys.argv:
    if arg[-3:] == ".md":
        markdown_files.append(arg)
    else:
        generated_test_paths.append(arg)

pattern_to_find_standalones = ('<!-- test-standalone ' +
                               '(.*)' +  # group containing filename
                               '\s-->\n```.*\n+' +
                               '((\n|.)+?)' +  # group containing standalone
                               '```')
generated_path_bazel_prefix = "bazel-out/darwin-fastbuild/genfiles/test/generated/"

standalones = []
for markdown_file in markdown_files:
    with open(markdown_file) as file:
        matches = re.findall(pattern_to_find_standalones, file.read())
        for standalone in matches:
            standalone_filename = standalone[0]
            if generated_path_bazel_prefix + standalone_filename in generated_test_paths:
                with open(generated_path_bazel_prefix + standalone_filename, "w") as generated_file:
                    standalone = standalone[1].replace("&lt;", "<").replace("&gt;", ">")  # replace html unicodes
                    standalone = re.sub(r"package .*?;", "package generated;", standalone)  # replace package name with that of bazel's
                    generated_file.write(standalone)


# test_methods = ""
# for i, standalone in enumerate(standalones):
#
#     # turn into a singe line + remove comments + escape double quotes
#     graql_lines = []
#     for line in standalone.get("code").split("\n"):
#         line = line.replace("\t", "")
#         if "#" not in line:
#             graql_lines.append(line.replace('"', "\\\""))
#     final_standalone = " ".join(graql_lines)
#
#     test_method = graql_standalone_test_method_template.replace("// PAGE COMMENT PLACEHOLDER", "// " + standalone.get("page"))  # change method name
#     test_method = test_method.replace("test() {", "test_" + str(i) + "() {")  # change page name comment
#     test_method = test_method.replace("// QUERIES PLACEHOLDER", final_standalone)  # add query objects
#     test_methods += test_method
#
# graql_standalone_test_class = graql_standalone_test_class_template.replace("// TEST METHODS PLACEHOLDER", test_methods)
#
# with open(generated_test_path, "w") as generated_test_file:
#     generated_test_file.write(graql_standalone_test_class)
