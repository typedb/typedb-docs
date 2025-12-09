import importlib
import logging
import sys
import os
from typing import Dict, List, Optional
from test.code.parser.parser import Parser, ParsedTest

# Logging config
logger = logging.getLogger('main')
logging.basicConfig(level=logging.DEBUG,  # set to logging.DEBUG for debugging
                    format="%(asctime)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


# Directories to code test
MODULE_DIRECTORIES = {
    # os.path.join(os.path.dirname(__file__), "tests"),
    "home": os.path.join(os.path.dirname(__file__), "../../home/modules/ROOT"),
    "manual": os.path.join(os.path.dirname(__file__), "../../manual/modules/ROOT"),
    "typeql": os.path.join(os.path.dirname(__file__), "../../typeql/modules/ROOT"),
    "drivers": os.path.join(os.path.dirname(__file__), "../../drivers/modules/ROOT"),
    "academy": os.path.join(os.path.dirname(__file__), "../../academy/modules/ROOT"),

    "home": os.path.join(os.path.dirname(__file__), "../../home/modules/ROOT"),
    "examples": os.path.join(os.path.dirname(__file__), "../../examples/modules/ROOT"),
    "guides": os.path.join(os.path.dirname(__file__), "../../guides/modules/ROOT"),
    "maintenance-operation": os.path.join(os.path.dirname(__file__), "../../maintenance-operation/modules/ROOT"),
    "core-concepts": os.path.join(os.path.dirname(__file__), "../../core-concepts/modules/ROOT"),
    "tools": os.path.join(os.path.dirname(__file__), "../../tools/modules/ROOT"),
    "reference": os.path.join(os.path.dirname(__file__), "../../reference/modules/ROOT"),
    "typeql-reference": os.path.join(os.path.dirname(__file__), "../../typeql-reference/modules/ROOT"),
}


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


def try_tests_in_file(runner, lang: str, adoc_path: str, adoc_config: Dict[str, Optional[str]]):
    try:
        parser = Parser(adoc_path, lang)
        parsed_tests = parser.parse_tests()
        logging.debug("Found tests:\n" + "\n\n".join([f"#{i+1}: {test}" for (i,test) in enumerate(parsed_tests)]))
        runner.try_tests(parsed_tests, adoc_path, adoc_config)
        logger.info(f"RESULTS: {runner.success_count} SUCCESSFUL, {runner.failure_count} FAILED")
        return runner.failure_count == 0
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def test_one_file(runner, lang: str, adoc_path: str):
    adoc_config = parse_adoc_config(adoc_path, runner.file_config_keys)
    if runner.check_config(adoc_config):
        try_tests_in_file(runner, lang, adoc_path, adoc_config)
    else:
        logger.info(f"[{adoc_path}]: Bad adoc attributes in file.")
    if runner.failure_count > 0:
        print("EXITING WITH code 1")
        sys.exit(1)

def test_all_files(runner, lang: str, directory: str):
    files_with_failures = []
    files_tested_counter = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".adoc"):
                adoc_path = os.path.relpath(os.path.join(root, file))
                adoc_config = parse_adoc_config(adoc_path, runner.file_config_keys)
                if adoc_config[runner.file_config_keys[0]] is not None:
                    if runner.check_config(adoc_config):
                        logger.info(f"TESTING FILE {adoc_path}")
                        if not try_tests_in_file(runner, lang, adoc_path, adoc_config):
                            files_with_failures.append(adoc_path)
                        files_tested_counter += 1
                    else:
                        logger.info(f"Bad adoc attributes in file.")

    logger.info(f"SUMMARY: {files_tested_counter} file(s) tested in '{directory}', {len(files_with_failures)} file(s) had test failures" + "".join(["\n>> " + file for file in files_with_failures]))
    if len(files_with_failures) > 0:
        print("EXITING WITH code 1")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m test.code.main <lang> [<file> or <directory>]")
        sys.exit(1)

    lang = sys.argv[1]
    path = sys.argv[2]

    try:
        module = importlib.import_module(f'test.code.runners.{lang}_runner')
        runner_class = getattr(module, f'{lang.capitalize()}Runner')
        runner = runner_class()
    except ModuleNotFoundError as e:
        print(f"Unsupported language: {lang}. msg: {e}")
        sys.exit(1)
    except AttributeError as e:
        print(f"Runner class for language '{lang}' not found. msg: {e}")
        sys.exit(1)

    if os.path.isdir(path):
        logger.info(f"START: testing {lang} in directory mode")
        test_all_files(runner, lang, path)
    else:
        logger.info(f"START: testing {lang} in single file mode")
        test_one_file(runner, lang, path)
