import re
import os

SRC_PATH = './src/'
ADOC_PATH = './adoc/'


def parse_java_source(source):
    # Update the class_pattern to accurately capture class contents extends ErrorMessage
    class_pattern = re.compile(r'^\s*public (static )?class (\w+) extends ([\w\.]+)?ErrorMessage \{(.*?)^\s*}', re.DOTALL | re.MULTILINE)
    # Template for field pattern, requiring adjustment for class name
    field_pattern_template = r'^\s*public static final {class_name} (\w+) =\s*new {class_name}\((\d+), "(.*?)"\);'
    # Updated prefix_pattern to match both public and private modifiers for codePrefix
    prefix_pattern = re.compile(r'\s*(public|private) static final String codePrefix = "(.*?)";.*?private static final String messagePrefix = "(.*?)";', re.DOTALL)

    total_field_count = 0  # Initialize total field count
    docs = []
    for class_match in class_pattern.finditer(source):
        class_body = class_match.group(4)  # Extracted class body content
        class_name = class_match.group(2)
        field_count = 0  # Initialize field count for this class

        # Search for codePrefix and messagePrefix within the class body
        prefix_match = prefix_pattern.search(class_body)
        if not prefix_match:
            continue  # Skip this class if prefixes are not found
        # code_prefix captures the second group due to the inclusion of the access modifier group
        _, code_prefix, message_prefix = prefix_match.groups()

        class_docs = [f"== {message_prefix}\n\n"]  # Initialize class documentation using messagePrefix
        # Dynamically create the field pattern for each class
        field_pattern = re.compile(field_pattern_template.format(class_name=class_name), re.DOTALL | re.MULTILINE)
        for field_match in field_pattern.finditer(class_body):
            field_name = field_match.group(1)
            number = field_match.group(2)
            message = field_match.group(3).replace('\n', '\\n')
            class_docs.append(f"`{field_name}`::\n[{code_prefix}{number}] {message_prefix}: {message}\n\n")
            field_count += 1  # Increment the field count
        total_field_count += field_count  # Add to total field count
        docs.extend(class_docs)
        docs.append(f"// Number of fields in {class_name}: {field_count}\n\n")
    # Prepend the total field count at the beginning of the AsciiDoc
    docs.insert(0, f"// Total number of fields across all classes: {total_field_count}\n\n")
    return "".join(docs)


def main():
    for dirpath, dirnames, filenames in os.walk(SRC_PATH):
        for filename in filenames:
            file_path = os.path.join(SRC_PATH, filename)
            try:
                # Open the source file
                with open(file_path, 'r') as data:
                    java_source = data.read()
                # Generate AsciiDoc from the Java source
                asciidoc = parse_java_source(java_source)
                # print(asciidoc)
                # Save the adoc file
                new_file_path = os.path.join(ADOC_PATH, filename + '.adoc')
                with open(new_file_path, 'w') as data:
                    data.write(asciidoc)
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
