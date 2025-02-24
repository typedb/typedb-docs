import subprocess
import os
import shutil
from typing import List, Dict
from code_test.parser.parser import ParsedTest
from code_test.runners.base_runner import BaseRunner
import logging

logger = logging.getLogger('main')

# Poor man's testing grammar (keywords used in .adoc files)
## .adoc attribute keys and values
ADOC_TEST_KEY = "test-rust"
ADOC_CONFIG_KEYS = [ADOC_TEST_KEY]


class RustRunner(BaseRunner):
    def __init__(self):
        super().__init__(adoc_keys=ADOC_CONFIG_KEYS)
        self.temp_dir = None

    def check_config(self, adoc_config: Dict[str, str]):
        if adoc_config.get(ADOC_TEST_KEY) not in ["yes", "true"]:
            logger.info(
                f"adoc attribute :{ADOC_TEST_KEY}: must be set to either 'yes' or 'true' for testing"
            )
            return False
        return True

    def run_test(self, parsed_test: ParsedTest, adoc_path: str):
        if not self.temp_dir:
            raise RuntimeError("No temporary directory set. Make sure to run inside try_tests().")

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
            with open(cargo_toml_path, "w") as f:
                f.write(
                    """
[package]
name = "temp_rust_project"
version = "0.1.0"
edition = "2021"

[dependencies]
serde_json = "1.0.114"
typedb-driver = { version = "3.0.5" }
tokio = "1.43.0"
futures-util = "0.3.31"
"""
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
