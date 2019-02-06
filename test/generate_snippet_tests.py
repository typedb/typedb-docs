import re
import sys

lang, base_template_path, test_template_path, generated_test_path, markdown_files = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]

PLACEHOLDER = "// PLACEHOLDER"

snippets = []
code_snippet_counter = 0
for markdown_file in markdown_files:
    with open(markdown_file) as file:
        pattern = '(?<!<!-- ignore-test -->\n)```([^\n]+)((\n|.)+?)```'
        matches = re.findall(pattern, file.read())
        for match in matches:
            if match[0] == lang:
                snippets.append({"code": match[1], "test_method_name": "test_" + str(code_snippet_counter) + "()"})
                code_snippet_counter += 1
print("identified " + str(code_snippet_counter) + " " + lang + " code snippets.")

test_methods = ""
with open(test_template_path, "r") as test_template_file:
    test_template = test_template_file.read()
    for snippet in snippets:
        if lang == "graql":
            # remove comment lines and escape double quotes
            graql_lines = []
            for line in snippet.get("code").split("\n"):
                line = line.replace("\t", "")
                if "#" not in line:
                    graql_lines.append(line.replace('"', "\\\""))
            final_snippet = " ".join(graql_lines)
        else:
            final_snippet = snippet.get("code")

        new_test_method = test_template.replace(PLACEHOLDER, final_snippet).replace("test()", snippet.get("test_method_name"))
        test_methods += new_test_method
print("generated all " + str(code_snippet_counter) + " " + lang + " test methods.")

# replace html unicodes
test_methods = test_methods.replace("&lt;", "<").replace("&gt;", ">")

with open(base_template_path, "r") as base_template_file:
    new_template_content = base_template_file.read().replace(PLACEHOLDER, test_methods)
    with open(generated_test_path, "w") as generated_test_file:
        generated_test_file.write(new_template_content)
print("generated " + lang + " test file is ready!")
