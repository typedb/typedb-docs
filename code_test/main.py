import importlib
import sys
from typing import Dict
from parser.parser import parse_programs


def parse_adoc_config(adoc_path: str, key_names: Dict[str, str]) -> Dict[str, str]:
    adoc_config = {}

    with open(adoc_path, 'r', encoding='utf-8') as f:
        for line in f:
            for key in key_names.keys():
                if line.strip().startswith(f':{key_names[key]}:'):
                    parts = line.strip().split(f':{key_names[key]}:', 1)
                    adoc_config[key] = parts[1].strip()
            if len(adoc_config.keys()) == len(key_names.keys()):
                break

    for key in key_names.keys():
        if not adoc_config.get(key):
            adoc_config[key] = None

    return adoc_config


def test_one_file(runner, lang: str, adoc_path: str) -> None:
    # Parse
    adoc_config = parse_adoc_config(adoc_path, runner.ADOC_CONFIG_NAMES)

    # Test
    try:
        parsed_programs = parse_programs(adoc_path, lang)
        runner.test_programs(parsed_programs, adoc_path, adoc_config)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def test_all_files(runner, lang: str):
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_code_test.py <lang> [<path-to-file>]\n(lang can be 'tql', 'rust', 'python')")
        sys.exit(1)

    lang = sys.argv[1]

    try:
        module = importlib.import_module(f'runners.{lang}_runner')
        runner_class = getattr(module, f'{lang.capitalize()}Runner')
        runner = runner_class()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except ModuleNotFoundError:
        print(f"Unsupported language: {lang}")
        sys.exit(1)
    except AttributeError:
        print(f"Runner class for language '{lang}' not found")
        sys.exit(1)

    if sys.argv[2]:
        file_path = sys.argv[2]
        test_one_file(runner, lang, file_path)
    else:
        test_all_files(runner, lang)