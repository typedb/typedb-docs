import os
import re
from dataclasses import dataclass
from typing import List, Dict
import logging
logger = logging.getLogger('main')
# To see debug log, set logging level to debug in main.py

# !!! Keep this synced with typedb-docs-web hidden-code.js MARKERS !!!
MARKERS = {
    "typeql": {
        "test_start": "#!test",  # may have options, e.g. '#!test[write, reset, count=3]', see README.md
        "hidden_segment_start": "#{{",
        "hidden_segment_end": "#}}",
        "segment_separator": "#---",  # used to separate non-hidden queries
    },
    "python": {
        "test_start": "#!test",
        "hidden_segment_start": "#{{",
        "hidden_segment_end": "#}}",
        "segment_separator": "#---",
    },
    "rust": {
        "test_start": "//!test",
        "hidden_segment_start": "//{{",
        "hidden_segment_end": "//}}",
        "segment_separator": "//---",
    }
}

@dataclass
class ParsedTest:
    segments: List[str]
    lang: str
    config: Dict[str, str]

    def __hash__(self):
        return hash((tuple(self.segments), self.lang, frozenset(self.config.items())))

    def __repr__(self):
        blocks_repr = "[\n" + "\n--- new segment ---\n".join(str(block) for block in self.segments) + "\n]"
        return (f"ParsedTest(lang={self.lang},\n"
                f"config={self.config},\n"
                f"segments={blocks_repr})")


class Parser:
    def __init__(self, adoc_path, language):
        # Stateless data
        self.adoc_path = adoc_path
        self.language = language
        self.parsed_tests = []

        # Parser states
        self.line_number = 0
        self.in_language_block = False  # an 'Antora' language block are similar
        self.in_test = False  # a test started with a test marker
        self.in_segment = False  # a code segment (e.g. individual query)

        # Stateful data
        self.current_test_config: Dict[str, str] = {}
        self.current_test_segments: List[str] = []
        self.current_segment_code: List[str] = []

    def error(self, message: str):
        raise ValueError(f"[{self.adoc_path} line {self.line_number}]: {message}")

    def parse_test_config(self, config_str: str) -> Dict[str, str]:
        config: Dict[str, str] = {}
        config_str = config_str.strip().lstrip('[').rstrip(']').strip()

        if not config_str:
            return config

        attributes = [p.strip() for p in config_str.split(',')]
        for attribute in attributes:
            if not attribute:
                continue
            if '=' in attribute:
                key, val = attribute.split('=', 1)
                config[key.strip()] = val.strip()
            else:
                config[attribute] = ""
        return config

    def retrieve_antora_include(self, include_str: str):
        # Parse Antora include
        from code_test.main import MODULE_DIRECTORIES

        antora_style_include = r'^.+?@(.+?)::(.+?)\$(.+?)\[(.*?)\]'
        relative_include = r'^include::\.\/(.+?)\[(.*?)\]'

        if re.match(antora_style_include, include_str):
            include_match = re.match(antora_style_include, include_str)
            module_name: str = include_match.group(1)
            document_type: str = include_match.group(2)
            file_rel_path: str = include_match.group(3)
            file_path: str = MODULE_DIRECTORIES[module_name] + "/" + document_type + "s/" + file_rel_path
            tags_match: str = include_match.group(4)

        elif re.match(relative_include, include_str):
            include_match = re.match(relative_include, include_str)
            relative_path = include_match.group(1)
            file_path: str = os.path.join(os.path.dirname(self.adoc_path), "./" + relative_path)
            print(f"determined file_path {file_path}")
            tags_match: str = include_match.group(2)

        else:
            raise RuntimeError(f"Parser couldn't resolve include {include_str}")

        tags: List[str] = []
        if tags_match.startswith('tag='):
            tags = [tags_match.split('=')[1]]
        if tags_match.startswith('tags='):
            tags = tags_match.split('=')[1].split(';')

        # Read tagged lines from Antora include
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        tagged_lines: Dict[str, List[str]] = {}
        current_tag = None
        for (i, line) in enumerate(lines):
            line = line.rstrip('\n')
            # logging.debug(f"... include scan of line {i}: {line}")
            if current_tag is None:
                tag_match = re.match(r'.*?tag::(.+?)\[', line)
                if tag_match:
                    tag = tag_match.group(1)
                    if tag in tags:
                        current_tag = tag
                        if tag in tagged_lines.keys():
                            self.error(f"Duplicate tag")
                        tagged_lines[tag] = []
            else:
                end_match = re.match(r'.*?end::(.+?)\[', line)
                if end_match:
                    tag = end_match.group(1)
                    if tag == current_tag:
                        current_tag = None
                    else:
                        self.error(f"Include has mismatch tag {current_tag}")
                if current_tag is not None:
                    tagged_lines[current_tag].append(line)

        logging.debug(f"... finished scanning included file, resolved tags: {tagged_lines}")

        output_lines = []
        for tag in tags:
            if tagged_lines.get(tag) is None:
                self.error(f"Include is missing tag {tag}")
            output_lines += tagged_lines[tag]

        return output_lines

    def finalize_current_segment(self):
        if self.current_segment_code:
            segment_source = "\n".join(self.current_segment_code)
            self.current_test_segments.append(segment_source)
        self.current_segment_code = []

    def reset_current_test(self):
        self.current_test_config = {}
        self.current_test_segments = []
        self.current_segment_code = []

    def finalize_current_test(self):
        self.finalize_current_segment()
        if self.current_test_segments:
            self.parsed_tests.append(ParsedTest(self.current_test_segments, self.language, self.current_test_config))
        self.reset_current_test()

    def parse_tests(self) -> List[ParsedTest]:
        with open(self.adoc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        while self.line_number < len(lines):
            line = lines[self.line_number].rstrip('\n')

            if line.startswith('[') and line.endswith(']') and line.find(self.language) > 0:
                logger.debug(f"line {self.line_number}: found language block start")
                if self.in_language_block:
                    self.error("Nested language block found")
                self.in_language_block = True
                # Forward to start, and then skip it
                self.line_number += 2
                continue

            if self.in_language_block:
                if line.startswith('----'):
                    logger.debug(f"line {self.line_number}: found language block end")
                    if self.in_segment:
                        self.error("Unfinished segment at code block end")

                    self.finalize_current_test()
                    self.in_test = False
                    self.in_language_block = False
                    self.line_number += 1
                    continue

            test_start_line = re.match(r'^\s*' + re.escape(MARKERS[self.language]['test_start']) + r'(\[.+?\])?', line)

            if self.in_language_block and test_start_line:
                logger.debug(f"line {self.line_number}: found test start")
                if self.in_segment:
                    self.error("Unfinished segment at test start")

                if self.in_test:
                    self.finalize_current_test()

                self.in_test = True

                config_str = test_start_line.group(1)
                if config_str is not None:
                    self.current_test_config = self.parse_test_config(config_str)
                else:
                    self.current_test_config = {}
                self.line_number += 1
                continue

            if self.in_language_block and self.in_test:
                if line.startswith(MARKERS[self.language]['hidden_segment_start']):
                    logger.debug(f"line {self.line_number}: found hidden segment start")
                    if self.in_segment:
                        self.error("Nested hidden segment found.")
                    self.finalize_current_segment()
                    self.in_segment = True

                elif line.startswith(MARKERS[self.language]['hidden_segment_end']):
                    logger.debug(f"line {self.line_number}: found hidden segment end")
                    if not self.in_segment:
                        self.error("No hidden segment to end found.")
                    self.finalize_current_segment()
                    self.in_segment = False

                elif line.startswith(MARKERS[self.language]['segment_separator']):
                    logger.debug(f"line {self.line_number}: found segment separator")
                    if self.in_segment:
                        self.error("Cannot separate in a hidden segment")
                    self.finalize_current_segment()

                elif line.startswith("include::"):
                    logger.debug(f"line {self.line_number}: found include")
                    included_lines = self.retrieve_antora_include(line)
                    for included_line in included_lines:
                        self.current_segment_code.append(included_line.rstrip("\n"))

                else:
                    logger.debug(f"line {self.line_number}: found code, adding to current segment")
                    self.current_segment_code.append(line)

                self.line_number += 1
                continue

            logger.debug(f"line {self.line_number}: skipping")
            self.line_number += 1

        if self.in_language_block:
            self.error("Found unclosed Antora code block at EOF")

        return self.parsed_tests
