import re
import sys
import json
from pathlib import Path
from typedb.driver import TypeDB, Driver, TransactionType, Credentials, DriverOptions
from enum import Enum
from typing import List, Dict, Tuple, Union

# Config
TEST_ATTRIBUTE = "test-typeql"
TEST_ENTRYPOINT = "test-entrypoint"
USERNAME = "admin"
PASSWORD = "password"
TEST_DB_NAME = "sample_app_db"
SERVER_ADDR = "127.0.0.1:1729"


class Edition(Enum):
    Cloud = 1
    Core = 2


TYPEDB_EDITION = Edition.Core


def create_driver(edition: Edition, uri: str, username: str = USERNAME, password: str = PASSWORD) -> Driver:
    if edition is Edition.Core:
        driver = TypeDB.core_driver(uri, Credentials(username, password), DriverOptions(False, None))
        return driver
    if edition is Edition.Cloud:
        driver = TypeDB.cloud_driver([uri], Credentials(username, password), DriverOptions(False, None))
        return driver


def setup_test_database(driver: Driver, db_name: str, reset: bool = True) -> bool:
    if reset and driver.databases.contains(db_name):
        driver.databases.get(db_name).delete()
    driver.databases.create(db_name)
    return True


def run_and_commit_queries(driver: Driver, queries: List[str], transaction_type: TransactionType) -> None:
    with driver.transaction(transaction_type) as tx:
        promises = []
        for q in queries:
            promises += [tx.query(q)]
        for p in promises:
            p.resolve()
        tx.commit()


def run_failing_queries(driver: Driver, queries: List[str], transaction_type: TransactionType) -> str:
    with driver.transaction(transaction_type) as tx:
        try:
            promises = []
            for q in queries:
                promises += [tx.query(q)]
            for p in promises:
                p.resolve()
        except:
            return "runtime"
        try:
            tx.commit()
        except:
            return "commit"
    return "success"


def run_counted_queries(driver: Driver, queries: List[str], expected_count: int, transaction_type: TransactionType) -> int:
    count_var_name = "automatic_test_count"
    queries[-1] = queries[-1] + f"\nreduce ${count_var_name}=count;"
    with driver.transaction(transaction_type) as tx:
        promises = []
        results = []
        for q in queries:
            promises += [tx.query(q)]
        for p in promises:
            results.append(p.resolve())
        result = list(results[-1].as_concept_rows())
        count = result[0].get(count_var_name).get_integer()
        return count


def test_transactions(test_attribute: str, test_entrypoint: str, parsed_code_blocks: List[Dict[str, Union[str, Dict[str, str]]]]) -> None:
    linear_mode = True if test_attribute == "linear" else False
    # TODO
    return None


def parse_attributes(attr_string: str, adoc_path: str) -> Dict[str, str]:
    attributes = {}
    attr_string = attr_string.strip().lstrip('[').rstrip(']').strip()

    if not attr_string:
        return attributes

    parts = [p.strip() for p in attr_string.split(',')]
    for part in parts:
        if not part:
            continue
        if '=' not in part:
            raise ValueError(f"[Adoc: {adoc_path}]: Provided attribute '{part}' is not in key=value form.")
        key, val = part.split('=', 1)
        attributes[key.strip()] = val.strip()
    return attributes


def extract_adoc_attributes(adoc_path: str) -> Tuple[str, str]:
    test_attribute = None
    test_entrypoint = None

    with open(adoc_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith(f':{TEST_ATTRIBUTE}:'):
                parts = line.strip().split(f':{TEST_ATTRIBUTE}:', 1)
                test_attribute = parts[1].strip()
                if test_attribute == "linear":
                    break
            elif line.strip().startswith(f':{TEST_ENTRYPOINT}:'):
                parts = line.strip().split(f':{TEST_ENTRYPOINT}:', 1)
                test_entrypoint = parts[1].strip()
                break  # assume that test_attribute comes before test_entrypoint in .adoc attribute preamble

    if not test_attribute:
        raise ValueError(f"[Adoc: {adoc_path}]: No ':{TEST_ATTRIBUTE}:' attribute found in file")

    if not test_attribute == "linear" and not test_attribute == "custom":
        raise ValueError(f"[Adoc: {adoc_path}]: Wrong value for ':{TEST_ATTRIBUTE}:' (can be either 'linear' or 'custom'")

    if test_attribute == "custom" and not test_entrypoint:
        raise ValueError(f"[Adoc: {adoc_path}]: ':{TEST_ATTRIBUTE}:' set to 'custom' but no ':test-entrypoint' given")

    # Could add more validation if you want to be certain
    return test_attribute, test_entrypoint


def parse_transactions_from_adoc(adoc_path: str) -> List[Dict[str, Union[str, List[str]]]]:
    parsed_transactions = []
    in_transaction = False
    in_query = False
    transaction_attributes = {}

    with open(adoc_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    line_number = 0
    while line_number < len(lines):
        line = lines[line_number].rstrip('\n')

        start_match = re.match(r'^\s*//#!open(\[.+?\])', line)
        if start_match:
            if in_transaction:
                raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Found //#!open while already in a transaction block. Nested transactions not supported.")
            in_transaction = True
            attr_str = start_match.group(1)  # e.g. "[key=val, ...]"
            transaction_attributes = parse_attributes(attr_str, adoc_path)
            transaction_queries = []
            line_number += 1
            continue

        if in_transaction:
            if line.strip().startswith('//#!commit'):
                if not transaction_queries:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Found empty transaction")
                parsed_transactions.append({
                    "queries": transaction_queries,
                    "attributes": transaction_attributes
                })
                if in_query:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Trying to //#!commit while still in //#!start(ed) query")
                in_transaction = False
                transaction_attributes = {}
                transaction_queries = []
                line_number += 1
                continue

            if line.strip().startswith('//#!q-start'):
                if in_query:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Found nested //#!start.")
                in_query = True
                query_lines = []
                line_number += 1
                continue

            if line.strip().startswith('//#!q-end'):
                if not query_lines:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Found empty query")
                transaction_queries.append("\n".join(query_lines))
                in_query = False
                query_lines = []
                line_number += 1
                continue

            if line.strip().startswith('//#!snip'):
                line_number += 1

                if line_number >= len(lines) or not lines[line_number].strip().startswith('////'):
                    raise ValueError(
                        f"[Adoc: {adoc_path}#{line_number}]: //#!snip must be followed by a comment block starting with '////'")
                line_number += 1

                while line_number < len(lines):
                    if lines[line_number].strip().startswith('////'):
                        line_number += 1
                        break
                    query_lines.append(lines[line_number].rstrip())
                    line_number += 1

                continue

            if line.strip().startswith('[') and ',typeql' in line and line.strip().endswith(']'):
                line_number += 1

                if line_number >= len(lines) or not lines[line_number].strip().startswith('----'):
                    raise ValueError(
                        f"[Adoc: {adoc_path}#{line_number}]: [,typeql] block enclosed in '----' or similar.")
                line_number += 1

                while line_number < len(lines):
                    if lines[line_number].strip().startswith('----'):
                        line_number += 1
                        break
                    query_lines.append(lines[line_number].rstrip())
                    line_number += 1

                continue

        line_number += 1

    if in_transaction:
        raise ValueError(
            f"[Adoc: {adoc_path}#{line_number}]: Reached end of file but a //#!commit was never found for the last block.")

    return parsed_transactions


def parse_adoc_for_code_tests(adoc_path: str) -> Tuple[str, str, List[Dict[str, Union[str, Dict[str, str]]]]]:
    test_attribute, test_entrypoint = extract_adoc_attributes(adoc_path)
    parsed_code_blocks = parse_transactions_from_adoc(adoc_path)
    return test_attribute, test_entrypoint, parsed_code_blocks


def test_file(adoc_path: str) -> None:

    # Parse
    try:
        test_attribute, test_entrypoint, parsed_code_blocks = parse_adoc_for_code_tests(adoc_path)
        # Print or return as needed. For now, just print in JSON
        print(json.dumps(parsed_code_blocks, indent=2))
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Test
    try:
        test_transactions(test_attribute, test_entrypoint, parsed_code_blocks)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_code_test.py <path-to-adoc-file>")
        sys.exit(1)

    adoc_path = sys.argv[1]
    test_file(adoc_path)