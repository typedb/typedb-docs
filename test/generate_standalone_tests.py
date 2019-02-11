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