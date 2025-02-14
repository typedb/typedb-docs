import re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Union

# Parser config
PROGRAM_START_MARKER = "program"
PROGRAM_END_MARKER = "run"
CODE_BLOCK_START_MARKER = "++"
CODE_BLOCK_END_MARKER = "--"

@dataclass
class ParsedProgram:
    blocks: List[str]
    lang: str
    config: Dict[str, str]

    def __hash__(self):
        return hash((tuple(self.blocks), self.lang, frozenset(self.config.items())))

    def __repr__(self):
        blocks_repr = "[\n" + "\n==block-separator==\n".join(str(block) for block in self.blocks) + "\n]"
        return (f"\nParsedProgram(lang={self.lang},\n"
                f"blocks={blocks_repr},\n"
                f"config={self.config})")


def parse_config(config_str: str, adoc_path: str) -> Dict[str, str]:
    config: Dict[str, str] = {}
    config_str = config_str.strip().lstrip('[').rstrip(']').strip()

    if not config_str:
        return config

    parts = [p.strip() for p in config_str.split(',')]
    for part in parts:
        if not part:
            continue
        if '=' not in part:
            raise ValueError(f"[Adoc: {adoc_path}]: Provided attribute '{part}' is not in key=value form.")
        key, val = part.split('=', 1)
        config[key.strip()] = val.strip()
    return config


def parse_programs(adoc_path: str, language: str) -> List[ParsedProgram]:
    parsed_programs = []
    in_program = False
    in_code_block = False
    program_config = {}

    with open(adoc_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    line_number = 0
    while line_number < len(lines):
        line = lines[line_number].rstrip('\n')

        program_opened = re.match(r'^\s*//!' + PROGRAM_START_MARKER + r'(\[.+?\])', line)
        if program_opened:
            if in_program:
                raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Nested programs not supported.")
            attr_str = program_opened.group(1)  # e.g. "[key=val, ...]"
            program_config = parse_config(attr_str, adoc_path)
            if not program_config["lang"]:
                raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Any program needs a language attribute 'lang'")
            if program_config["lang"] == language:
                in_program = True
                program_code_blocks: List[str] = []
            line_number += 1
            continue

        if in_program:
            if line.strip().startswith(f'//!{PROGRAM_END_MARKER}'):
                if not program_code_blocks:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Found empty program (i.e. no code blocks)")
                parsed_programs.append(ParsedProgram(program_code_blocks, program_config["lang"], program_config))
                if in_code_block:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Cannot run without closing code blocks")
                in_program = False
                program_config = {}
                program_code_blocks = []
                line_number += 1
                continue

            if line.strip().startswith(f'//!{CODE_BLOCK_START_MARKER}'):
                if in_code_block:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Found nested code block")
                in_code_block = True
                query_lines: List[str] = []
                line_number += 1
                continue

            if line.strip().startswith(f'//!{CODE_BLOCK_END_MARKER}'):
                if not query_lines:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Found empty query")
                program_code_blocks.append("\n".join(query_lines))
                in_code_block = False
                query_lines = []
                line_number += 1
                continue

            if line.strip().startswith('////'):
                original_line = line_number
                individual_code_block = False
                line_number += 1

                if not in_code_block:
                    individual_code_block = True
                    query_lines: List[str] = []

                while True:
                    if line_number >= len(lines):
                        raise ValueError(f"[Adoc: {adoc_path}#{original_line}]: unclosed code snippet '////'.")
                        break
                    if lines[line_number].strip().startswith('////'):
                        line_number += 1
                        break
                    query_lines.append(lines[line_number].rstrip())
                    line_number += 1

                if individual_code_block:
                    program_code_blocks.append("\n".join(query_lines))
                    query_lines = []

                continue

            if line.strip().startswith('----'):
                original_line = line_number
                line_number += 1

                while True:
                    if line_number >= len(lines):
                        raise ValueError(f"[Adoc: {adoc_path}#{original_line}]: unclosed code block '----'.")
                        break
                    if lines[line_number].strip().startswith('----'):
                        line_number += 1
                        break
                    query_lines.append(lines[line_number].rstrip())
                    line_number += 1

                continue

        line_number += 1

    if in_program:
        raise ValueError(
            f"[Adoc: {adoc_path}#{line_number}]: Program wasn't closed by end of file (use '//!run')")

    return parsed_programs