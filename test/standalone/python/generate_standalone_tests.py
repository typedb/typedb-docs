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
standalones = []
for markdown_file in markdown_files:
    with open(markdown_file) as file:
        matches = re.findall(pattern_to_find_standalones, file.read())
        for standalone in matches:
            standalone_filename = standalone[0]
            standalone = standalone[1]

            corresponding_path = None
            for path in generated_test_paths:
                if standalone_filename in path:
                    corresponding_path = path

            if corresponding_path:
                with open(corresponding_path, "w") as generated_file:
                    generated_file.write(standalone)
