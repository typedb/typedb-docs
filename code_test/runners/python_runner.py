import io
import sys
from typing import List, Dict, Tuple, Union
from parser.parser import ParsedProgram

# Poor man's testing grammar (keywords used in .adoc files)
## .adoc attribute keys and values
ADOC_TEST_KEY = "test-python"
ADOC_CONFIG_KEYS = [ADOC_TEST_KEY]


class PythonRunner:
    def __init__(self):
        self.ADOC_CONFIG_KEYS = ADOC_CONFIG_KEYS

    def run_program(self, parsed_program: ParsedProgram, adoc_path: str):
        source_code = "\n".join(parsed_program.blocks)
        print(f"\n...... NOW RUNNING\n{source_code}")

        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        try:
            exec(source_code)
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
            print(f"Captured Output:\n{output}")
        except Exception as e:
            raise RuntimeError(f"Error executing program from {adoc_path}: {e}")

    def test_programs(self, parsed_programs: List[ParsedProgram], adoc_path: str, config: Dict[str, str]) -> None:
        for (i, parsed_program) in enumerate(parsed_programs):
            try:
                self.run_program(parsed_program, adoc_path)
            except Exception as e:
                raise ValueError(f"[{adoc_path}]: failed testing program #{i} with, caused by:\n--> {e}")

        return None