import io
import sys
from typing import List, Dict, Tuple, Union
from code_test.parser.parser import ParsedProgram
from code_test.runners.base_runner import BaseRunner
import logging
logger = logging.getLogger('main')

# Poor man's testing grammar (keywords used in .adoc files)
## .adoc attribute keys and values
ADOC_TEST_KEY = "test-python"
ADOC_CONFIG_KEYS = [ADOC_TEST_KEY]


class PythonRunner(BaseRunner):
    def __init__(self):
        super().__init__(adoc_keys=ADOC_CONFIG_KEYS)

    def check_config(self, adoc_config: Dict[str, str]):
        if adoc_config.get(ADOC_TEST_KEY) not in ["yes", "true"]:
            logger.info(f"adoc attribute :{ADOC_TEST_KEY}: must be set to either 'yes' or 'true' for testing")
            return False
        return True

    def run_program(self, parsed_program: ParsedProgram, adoc_path: str):
        source_code = "\n".join(parsed_program.blocks)
        # logger.info(f"Source:\n{source_code}")

        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        exec(source_code)
        output = new_stdout.getvalue()
        sys.stdout = old_stdout
        # logger.info(f"Output:\n{output}")

    def test_program(self, parsed_program: ParsedProgram, index: int, adoc_path: str):
        try:
            logger.info(f"[{adoc_path}] Running program #{index} ...")
            self.run_program(parsed_program, adoc_path)
            logger.info(f"[{adoc_path}] ... SUCCESS")
            self.success_count += 1
        except Exception as e:
            logger.info(f"[{adoc_path}] ... ERROR:\n{e}")
            self.failure_count += 1

    def test_programs(self, parsed_programs: List[ParsedProgram], adoc_path: str, config: Dict[str, str]):
        self.reset_counts()
        self.reset_local_databases()

        for (i, parsed_program) in enumerate(parsed_programs):
            self.test_program(parsed_program, i, adoc_path)