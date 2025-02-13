import subprocess
import os
from typing import List, Dict
from parser.parser import ParsedProgram

# Poor man's testing grammar (keywords used in .adoc files)
## .adoc attribute keys and values
ADOC_TEST_KEY = "test-rust"
ADOC_CONFIG_KEYS = [ADOC_TEST_KEY]


class RustRunner:
    def __init__(self):
        self.ADOC_CONFIG_KEYS = ["test-rust"]

    def run_program(self, parsed_program: ParsedProgram, adoc_path: str):
        source_code = "\n".join(parsed_program.blocks)
        print(f"\n...... NOW RUNNING\n{source_code}")

        # Create a temporary directory for the Rust project
        temp_dir = "temp_rust_project"
        os.makedirs(temp_dir, exist_ok=True)

        # Write the source code to main.rs
        main_rs_path = os.path.join(temp_dir, "src", "main.rs")
        os.makedirs(os.path.dirname(main_rs_path), exist_ok=True)
        with open(main_rs_path, "w") as f:
            f.write(source_code)

        # Write a basic Cargo.toml file
        cargo_toml_path = os.path.join(temp_dir, "Cargo.toml")
        with open(cargo_toml_path, "w") as f:
            f.write("""
[package]
name = "temp_rust_project"
version = "0.1.0"
edition = "2021"

[dependencies]
""")

        # Run the Rust program using cargo
        try:
            result = subprocess.run(["cargo", "run"], cwd=temp_dir, capture_output=True, text=True)
            print(f"Captured output:\n{result.stdout}")
            if result.returncode != 0:
                print(f"Captured error:\n{result.stderr}")
                raise RuntimeError(f"Error executing program from {adoc_path}")
        except Exception as e:
            raise RuntimeError(f"Error executing program from {adoc_path}: {e}")
        finally:
            # Clean up the temporary directory
            import shutil
            shutil.rmtree(temp_dir)

    def test_programs(self, parsed_programs: List[ParsedProgram], adoc_path: str, config: Dict[str, str]) -> None:
        for (i, parsed_program) in enumerate(parsed_programs):
            try:
                self.run_program(parsed_program, adoc_path)
            except Exception as e:
                raise ValueError(f"[{adoc_path}]: failed testing program #{i} with, caused by:\n--> {e}")

        return None