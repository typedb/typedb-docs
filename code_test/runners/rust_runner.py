import subprocess
import os
from typing import List, Dict
from code_test.parser.parser import ParsedProgram
import logging
logger = logging.getLogger('main')

# Poor man's testing grammar (keywords used in .adoc files)
## .adoc attribute keys and values
ADOC_TEST_KEY = "test-rust"
ADOC_CONFIG_KEYS = [ADOC_TEST_KEY]


class RustRunner:
    def __init__(self):
        # Required
        self.adoc_keys = ADOC_CONFIG_KEYS
        self.success_count = 0
        self.failure_count = 0

    def reset_counts(self):
        self.success_count = 0
        self.failure_count = 0

    def check_config(self, adoc_config: Dict[str, str]):
        if adoc_config.get(ADOC_TEST_KEY) not in ["yes", "true"]:
            logger.info(f"adoc attribute :{ADOC_TEST_KEY}: must be set to either 'yes' or 'true' for testing")
            return False
        return True

    def run_program(self, parsed_program: ParsedProgram, adoc_path: str):
        source_code = "\n".join(parsed_program.blocks)
        # logger.info(f"Source:\n{source_code}")

        temp_dir = "temp_rust_project"
        os.makedirs(temp_dir, exist_ok=True)

        main_rs_path = os.path.join(temp_dir, "src", "main.rs")
        os.makedirs(os.path.dirname(main_rs_path), exist_ok=True)
        with open(main_rs_path, "w") as f:
            f.write(source_code)

        cargo_toml_path = os.path.join(temp_dir, "Cargo.toml")
        with open(cargo_toml_path, "w") as f:
            f.write("""
[package]
name = "temp_rust_project"
version = "0.1.0"
edition = "2021"

[dependencies]
""")

        try:
            result = subprocess.run(["cargo", "run"], cwd=temp_dir, capture_output=True, text=True)
            output = result.stdout
            if result.returncode != 0:
                raise RuntimeError(f"Rust error:\n{result.stderr}")
            # logger.info(f"Output:\n{output}")
        except Exception as e:
            raise RuntimeError(f"Execution error:\n{e}")
        finally:
            import shutil
            shutil.rmtree(temp_dir)

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

        for (i, parsed_program) in enumerate(parsed_programs):
            self.test_program(parsed_program, i, adoc_path)