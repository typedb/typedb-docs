import subprocess
import os
import shutil
from typing import List, Dict
from test.code.parser.parser import ParsedTest
from test.code.runners.base_runner import BaseRunner
import logging

logger = logging.getLogger('main')

# Poor man's testing grammar (keywords used in .adoc files)
## .adoc attribute keys and values
FILE_CONFIG_KEY_TEST = "test-rust"
FILE_CONFIG_KEYS = [FILE_CONFIG_KEY_TEST]

RUST_TEST_TOML = "rust_cargo_toml.toml"


class RustRunner(BaseRunner):
    def __init__(self):
        super().__init__(file_config_keys=FILE_CONFIG_KEYS)
        self.temp_dir = None

    def check_config(self, adoc_config: Dict[str, str]):
        if adoc_config.get(FILE_CONFIG_KEY_TEST) not in ["yes", "true"]:
            logger.info(
                f"adoc attribute :{FILE_CONFIG_KEY_TEST}: must be set to either 'yes' or 'true' for testing"
            )
            return False
        return True

    def run_test(self, parsed_test: ParsedTest, adoc_path: str):
        if not self.temp_dir:
            raise RuntimeError("No temporary directory set. Make sure to run inside try_tests().")
        self.before_run_test(parsed_test)

        source_code = "\n".join(parsed_test.segments)
        main_rs_path = os.path.join(self.temp_dir, "src", "main.rs")

        os.makedirs(os.path.dirname(main_rs_path), exist_ok=True)

        with open(main_rs_path, "w") as f:
            f.write(source_code)

        try:
            result = subprocess.run(
                ["cargo", "run"],
                cwd=self.temp_dir,
                capture_output=True,
                text=True
            )
            output = result.stdout
            if result.returncode != 0:
                raise RuntimeError(f"Rust error:\n{result.stderr}")
            # logger.info(f"Output:\n{output}")
        except Exception as e:
            raise RuntimeError(f"Execution error:\n{e}")
        finally:
            self.after_run_test(parsed_test)

    def try_test(self, parsed_test: ParsedTest, index: int, adoc_path: str):
        try:
            logger.info(f"[{adoc_path}] Running test #{index} ...")
            self.run_test(parsed_test, adoc_path)
            logger.info(f"[{adoc_path}] ... SUCCESS")
            self.success_count += 1
        except Exception as e:
            logger.info(f"[{adoc_path}] ... ERROR:\n{e}")
            self.failure_count += 1

    def try_tests(self, parsed_tests: List[ParsedTest], adoc_path: str, config: Dict[str, str]):
        self.reset_counts()
        self.reset_local_databases()

        self.temp_dir = "temp_rust_project"
        os.makedirs(self.temp_dir, exist_ok=True)

        cargo_toml_path = os.path.join(self.temp_dir, "Cargo.toml")
        if not os.path.exists(cargo_toml_path):
            shutil.copyfile(
                os.path.join(os.path.dirname(__file__), RUST_TEST_TOML),
                cargo_toml_path,
            )

        src_dir = os.path.join(self.temp_dir, "src")
        os.makedirs(src_dir, exist_ok=True)

        try:
            for i, parsed_test in enumerate(parsed_tests):
                self.try_test(parsed_test, i, adoc_path)
        finally:
            if os.path.isdir(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            self.temp_dir = None  # Reset so we can't accidentally reuse
