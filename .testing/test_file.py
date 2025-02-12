import re
import sys
import json
from dataclasses import dataclass
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

@dataclass
class ParsedTransaction:
    queries: List[str]
    type: str
    config: Dict[str, str]

    def __hash__(self):
        return hash((tuple(self.queries), self.type, frozenset(self.config.items())))

    def __repr__(self):
        return (f"ParsedTransaction(type={self.type}, "
                f"queries={self.queries}, "
                f"config={self.config})")

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


def run_transaction(parsed_transaction: ParsedTransaction):
    print(f"running {parsed_transaction}")
    return None

def test_transactions_in_order(test_attribute: str, test_entrypoint: str, parsed_transactions: List[ParsedTransaction], adoc_path: str) -> None:
    linear_mode = True if test_attribute == "linear" else False
    if linear_mode:
        # run transactions in linear order
        for parsed_transaction in parsed_transactions:
            run_transaction(parsed_transaction)
    else:
        # populate name lookup table
        name_lookup = {}
        for (i,parsed_transaction) in enumerate(parsed_transactions):
            if parsed_transaction.config["name"]:
                name = parsed_transaction.config["name"]
                if not name_lookup[name]:
                    name_lookup[name] = i
                else:
                    raise ValueError(f"[{adoc_path}]: Detected duplicate transaction name: {name}")

        # Now run transactions in custom order
        remaining_indices = set(range(0, len(parsed_transactions)))
        completed_indices = set()
        current_transaction_index = name_lookup[test_entrypoint] if name_lookup[test_entrypoint] else None

        if not current_transaction_index:
            raise ValueError(f"[{adoc_path}]: Didn't find test entrypoint {test_entrypoint}")

        while True:
            if current_transaction_index in completed_indices:
                raise ValueError(f"[{adoc_path}]: attempted to execute the same transaction (with index #{current_transaction_index}) twice")

            if current_transaction_index >= len(parsed_transactions):
                raise ValueError(f"[{adoc_path}]: tried to execute beyond last transaction before completion of all other transactions")

            current_transaction = parsed_transactions[current_transaction_index]
            run_transaction(current_transaction)
            remaining_indices.remove(current_transaction_index)
            completed_indices.add(current_transaction_index)

            if current_transaction.config["jump_to"]:
                current_transaction_index = name_lookup[current_transaction.config["jump_to"]]
            if len(remaining_indices) == 0:
                break
            current_transaction += 1

    return None


def parse_config(config_str: str, adoc_path: str) -> Dict[str, str]:
    config = {}
    config_str = config_str.strip().lstrip('[').rstrip(']').strip()

    if not config_str:
        return config

    parts = [p.strip() for p in config_str.split(',')]
    for part in parts:
        if not part:
            continue
        if '=' not in part:
            raise ValueError(f"[Adoc: {adoc_path}]: Provided attribute '{part}' is not in key=value form.")
        key, val = part.split('=', 1)
        config[key.strip()] = val.strip()
    return config


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


def parse_transactions_from_adoc(adoc_path: str) -> List[ParsedTransaction]:
    parsed_transactions = []
    in_transaction = False
    in_query = False
    transaction_config = {}

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
            transaction_config = parse_config(attr_str, adoc_path)
            if not transaction_config["type"]:
                raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Any transaction needs a type")
            transaction_queries = []
            line_number += 1
            continue

        if in_transaction:
            if line.strip().startswith('//#!commit'):
                if not transaction_queries:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Found empty transaction")
                parsed_transactions.append({
                    ParsedTransaction(transaction_queries, transaction_config["type"], transaction_config)
                })
                if in_query:
                    raise ValueError( f"[Adoc: {adoc_path}#{line_number}]: Trying to //#!commit while still in //#!start(ed) query")
                in_transaction = False
                transaction_config = {}
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
            f"[Adoc: {adoc_path}#{line_number}]: Reached end of file but transaction was completed with //#!commit")

    return parsed_transactions


def parse_adoc_for_code_tests(adoc_path: str) -> Tuple[str, str, List[ParsedTransaction]]:
    test_attribute, test_entrypoint = extract_adoc_attributes(adoc_path)
    parsed_transactions = parse_transactions_from_adoc(adoc_path)
    return test_attribute, test_entrypoint, parsed_transactions


def test_file(adoc_path: str) -> None:

    # Parse
    try:
        test_attribute, test_entrypoint, parsed_transactions = parse_adoc_for_code_tests(adoc_path)
        # Print or return as needed. For now, just print in JSON
        print(parsed_transactions)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Test
    try:
        test_transactions_in_order(test_attribute, test_entrypoint, parsed_transactions, adoc_path)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_code_test.py <path-to-adoc-file>")
        sys.exit(1)

    adoc_path = sys.argv[1]
    test_file(adoc_path)