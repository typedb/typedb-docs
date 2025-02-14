import importlib
import logging
import sys
import os
from typing import Dict, List, Optional
from code_test.parser.parser import parse_programs

# Logging config
logger = logging.getLogger('main')
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


# Directories to code test
DIRECTORIES = [
    # os.path.join(os.path.dirname(__file__), "tests"),
    os.path.join(os.path.dirname(__file__), "../home/modules/ROOT/pages"),
    os.path.join(os.path.dirname(__file__), "../manual/modules/ROOT/pages"),
    os.path.join(os.path.dirname(__file__), "../typeql/modules/ROOT/pages"),
    os.path.join(os.path.dirname(__file__), "../drivers/modules/ROOT/pages"),
    os.path.join(os.path.dirname(__file__), "../academy/modules/ROOT/pages")
]


def parse_adoc_config(adoc_path: str, key_names: List[str]) -> Dict[str, Optional[str]]:
    adoc_config: Dict[str, Optional[str]] = {}

    with open(adoc_path, 'r', encoding='utf-8') as f:
        for line in f:
            for key in key_names:
                if line.strip().startswith(f':{key}:'):
                    parts = line.strip().split(f':{key}:', 1)
                    adoc_config[key] = parts[1].strip()
            if len(adoc_config.keys()) == len(key_names):
                break

    for key in key_names:
        if not adoc_config.get(key):
            adoc_config[key] = None

    return adoc_config


def test_programs_in_file(runner, lang: str, adoc_path: str, adoc_config: Dict[str, Optional[str]]):
    try:
        parsed_programs = parse_programs(adoc_path, lang)
        runner.test_programs(parsed_programs, adoc_path, adoc_config)
        logger.info(f"RESULTS: {runner.success_count} SUCCESSFUL, {runner.failure_count} FAILED")
        return runner.failure_count == 0
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def test_one_file(runner, lang: str, adoc_path: str):
    adoc_config = parse_adoc_config(adoc_path, runner.adoc_keys)
    if runner.check_config(adoc_config):
        test_programs_in_file(runner, lang, adoc_path, adoc_config)
    else:
        logger.info(f"[{adoc_path}]: Bad adoc attributes in file.")


def test_all_files(runner, lang: str):
    files_with_failures = []
    files_tested_counter = 0
    for directory in DIRECTORIES:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".adoc"):
                    adoc_path = os.path.relpath(os.path.join(root, file))
                    adoc_config = parse_adoc_config(adoc_path, runner.adoc_keys)
                    if adoc_config[runner.adoc_keys[0]] is not None:
                        if runner.check_config(adoc_config):
                            logger.info(f"TESTING FILE {adoc_path}")
                            if not test_programs_in_file(runner, lang, adoc_path, adoc_config):
                                files_with_failures.append(adoc_path)
                            files_tested_counter += 1
                        else:
                            logger.info(f"Bad adoc attributes in file.")

    logger.info(f"SUMMARY: {files_tested_counter} file(s) tested, {len(files_with_failures)} file(s) had test failures" + "".join(["\n>> " + file for file in files_with_failures]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_code_test.py <lang> [<path-to-file>]\n(lang can be 'tql', 'rust', 'python')")
        sys.exit(1)

    lang = sys.argv[1]

    try:
        module = importlib.import_module(f'code_test.runners.{lang}_runner')
        runner_class = getattr(module, f'{lang.capitalize()}Runner')
        runner = runner_class()
    except ModuleNotFoundError as e:
        print(f"Unsupported language: {lang}. msg: {e}")
        sys.exit(1)
    except AttributeError as e:
        print(f"Runner class for language '{lang}' not found. msg: {e}")
        sys.exit(1)

    if len(sys.argv) > 2:
        logger.info(f"START: testing {lang} in single file mode")
        file_path = sys.argv[2]
        test_one_file(runner, lang, file_path)
    else:
        logger.info(f"START: testing {lang} in multi-file mode")
        test_all_files(runner, lang)