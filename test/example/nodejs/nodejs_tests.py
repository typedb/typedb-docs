import re
import sys

test_template_path = sys.argv[1]
generated_path = sys.argv[2]
markdown_files = sys.argv[3:]

pattern_to_find_standalones = ('<!-- test-example ' +
                               '(.*)' +  # group containing filename
                               '\s-->\n```.*\n+' +
                               '((\n|.)+?)' +  # group containing standalone
                               '```')
standalones = []

with open(test_template_path, "r") as template_file:
    template_content = template_file.read()

for markdown_file in markdown_files:
    with open(markdown_file, "r", encoding="utf-8") as file:
        matches = re.findall(pattern_to_find_standalones, file.read())
        for standalone in matches:
            standalone_filename = standalone[0]
            standalone_content = standalone[1]
            standalone_extension = standalone[0].split(".")[1]

            if standalone_extension == "js":
                standalone = re.sub(r"(^[^\s\(]+\(.*\))", r"await \g<1>", standalone_content, flags=re.MULTILINE)
                template_content = template_content.replace("// " + standalone_filename, standalone)

with open(generated_path, "w") as generated_file:
    generated_file.write(template_content)
