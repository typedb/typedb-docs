from typedb.driver import TypeDB, Driver, TransactionType, Credentials, DriverOptions
from test.runners.base_runner import BaseRunner
from enum import Enum
from typing import List, Dict, Tuple, Union
from test.parser.parser import ParsedTest
import logging
logger = logging.getLogger('main')
# To see debug log, set logging level to debug in main.py


# Poor man's testing grammar (keywords used in .adoc files)
## .adoc attribute keys and values
FILE_CONFIG_KEY_TEST = "test-typeql"
FILE_CONFIG_KEY_TEST_ENTRY = "test-typeql-entry"
FILE_CONFIG_KEYS = [FILE_CONFIG_KEY_TEST, FILE_CONFIG_KEY_TEST_ENTRY]  # first item should be the test key

FILE_CONFIG_VAL_TEST_LINEAR = "linear"  # Run examples linearly from top to bottom
FILE_CONFIG_VAL_TEST_CUSTOM = "custom"  # Jump around in examples in custom order

## Test attributes: keys and values
TEST_NAME_KEY = "name"
TEST_TXN_SCHEMA_KEY = "schema"
TEST_TXN_WRITE_KEY = "write"
TEST_TXN_READ_KEY = "read"
TEST_ROLLBACK_KEY = "rollback"
TEST_COUNT_KEY = "count"
TEST_DOCUMENTS_KEY = "documents"
TEST_JUMP_KEY = "jump"
TEST_FAIL_KEY = "fail_at"
TEST_FAIL_COMMIT_VAL = "commit"
TEST_FAIL_RUNTIME_VAL = "runtime"


class FailureMode(Enum):
    Runtime = 1
    Commit = 2
    NoFailure = 3


class TypeqlRunner(BaseRunner):
    def __init__(self):
        super().__init__(file_config_keys=FILE_CONFIG_KEYS)
        # Required
        self.success_count = 0
        self.failure_count = 0

        # Tql specific
        self.username = "admin"
        self.password = "password"
        self.db = "typeql_docs_test"
        self.uri = "127.0.0.1:1729"
        self.driver = self.create_driver()

    def create_driver(self) -> Driver:
        return TypeDB.driver(self.uri, Credentials(self.username, self.password), DriverOptions(False, None))

    def delete_db(self):
        if self.driver.databases.contains(self.db):
            self.driver.databases.get(self.db).delete()

    def setup_db(self, reset: bool = True) -> bool:
        if reset:
            self.delete_db()
        self.driver.databases.create(self.db)
        return True

    def reset_counts(self):
        self.success_count = 0
        self.failure_count = 0

    def check_config(self, adoc_config: Dict[str, str]):
        if adoc_config.get(FILE_CONFIG_KEY_TEST) not in ["linear", "custom"]:
            logger.info(f"adoc attribute :{FILE_CONFIG_KEY_TEST}: must be set to either 'linear' or 'custom'")
            return False
        elif adoc_config[FILE_CONFIG_KEY_TEST] == "custom" and adoc_config.get(FILE_CONFIG_KEY_TEST_ENTRY) is None:
            logger.info(f"adoc attribute :{FILE_CONFIG_KEY_TEST_ENTRY}: must be set to some test name for 'custom' test")
            return False
        return True

    def run_failing_queries(self, queries: List[str], type: TransactionType) -> str:
        with self.driver.transaction(self.db, type) as tx:
            try:
                promises = []
                for q in queries:
                    promises += [tx.query(q)]
                for p in promises:
                    p.resolve()
            except:
                return FailureMode.Runtime
            try:
                tx.commit()
            except:
                return FailureMode.Commit
        return FailureMode.NoFailure

    def run_transaction(self, queries: List[str], type: TransactionType, counted=False, rollback=False, documents=False) -> Union[int, None]:
        count_var_name = "automatic_test_count"
        if counted:
            queries[-1] = queries[-1] + f"\nreduce ${count_var_name} = count;"
        with self.driver.transaction(self.db, type) as tx:
            try:
                promises = []
                results = []
                for q in queries:
                    promises.append(tx.query(q))
                for p in promises:
                    results.append(p.resolve())
                if rollback:
                    tx.rollback()
                    tx.close()
                elif type == TransactionType.READ:
                    for r in results:
                        if documents:
                            consumed_iterator = list(r.as_concept_documents())
                        else:
                            consumed_iterator = list(r.as_concept_rows())
                    tx.close()
                else:
                    tx.commit()
                if counted:
                    if documents:
                        raise Exception("Counting currently relies on Reduce, which is not compatible with Documents")
                    if type == TransactionType.READ:
                        count = consumed_iterator[0].get(count_var_name).get_integer()
                    else:
                        last_result = list(results[-1].as_concept_rows())
                        count = last_result[0].get(count_var_name).get_integer()
                    return count
            except Exception as e:
                raise Exception(f"{e}") from e

    def run_test(self, parsed_test: ParsedTest, adoc_path: str):
        self.before_run_test(parsed_test)

        logger.debug(f"... test source:\n{parsed_test}")

        type = None
        if parsed_test.config.get(TEST_TXN_SCHEMA_KEY) is not None:
            type = TransactionType.SCHEMA
        elif parsed_test.config.get(TEST_TXN_WRITE_KEY) is not None:
            type = TransactionType.WRITE
        elif parsed_test.config.get(TEST_TXN_READ_KEY) is not None:
            type = TransactionType.READ
        if type is None:
            raise ValueError(f"[{adoc_path}]: Missing transaction type from test, see README.md")

        rollback = False
        if parsed_test.config.get(TEST_ROLLBACK_KEY) is not None:
            rollback = True

        counted = False
        if parsed_test.config.get(TEST_COUNT_KEY):
            reference_count = int(parsed_test.config[TEST_COUNT_KEY])
            counted = True

        documents = False
        if parsed_test.config.get(TEST_DOCUMENTS_KEY) is not None:
            documents = True

        if parsed_test.config.get(TEST_FAIL_KEY):
            ref_failure_mode = FailureMode.NoFailure
            match parsed_test.config[TEST_FAIL_KEY]:
                case x if x == TEST_FAIL_RUNTIME_VAL:
                    ref_failure_mode = FailureMode.Runtime
                case x if x == TEST_FAIL_COMMIT_VAL:
                    ref_failure_mode = FailureMode.Commit
            failure_mode = self.run_failing_queries(parsed_test.segments, type)
            if failure_mode != ref_failure_mode:
                raise RuntimeError(f"[{adoc_path}]: Failure mode: expected {ref_failure_mode} but got {failure_mode}")
        elif counted == True:
            count = self.run_transaction(parsed_test.segments, type, counted, rollback, documents)
            if count != reference_count:
                raise RuntimeError(f"[{adoc_path}]: Query count: expected {reference_count} but got {count}")
        else:
            self.run_transaction(parsed_test.segments, type, counted, rollback, documents)

        self.after_run_test(parsed_test)

    def try_test(self, parsed_test: ParsedTest, index: int, adoc_path: str):
        try:
            if parsed_test.config.get(TEST_NAME_KEY):
                logger.info(f"[{adoc_path}]: Running test '{parsed_test.config[TEST_NAME_KEY]}' ...")
            else:
                logger.info(f"[{adoc_path}]: Running test #{index} ...")
            self.run_test(parsed_test, adoc_path)
            logger.info(f"[{adoc_path}] ... SUCCESS")
            self.success_count += 1
        except Exception as e:
            logger.info(f"[{adoc_path}] ... ERROR:\n{e}")
            self.failure_count += 1

    def try_tests(self, parsed_tests: List[ParsedTest], adoc_path: str, file_config: Dict[str, str]) -> None:
        self.setup_db(reset=True)  # Resets the database
        self.reset_counts()

        if file_config[FILE_CONFIG_KEY_TEST] == FILE_CONFIG_VAL_TEST_LINEAR:
            # try tests in linear order
            for (i, parsed_test) in enumerate(parsed_tests):
                self.try_test(parsed_test, i, adoc_path)

        elif file_config[FILE_CONFIG_KEY_TEST] == FILE_CONFIG_VAL_TEST_CUSTOM:
            # populate name lookup table
            name_lookup = {}
            for (i,parsed_test) in enumerate(parsed_tests):
                if parsed_test.config.get(TEST_NAME_KEY):
                    name = parsed_test.config[TEST_NAME_KEY]
                    if not name_lookup.get(name):
                        name_lookup[name] = i
                    else:
                        raise ValueError(f"[{adoc_path}]: Detected duplicate test name: {name}")

            # Now run tests in custom order
            remaining_indices = set(range(0, len(parsed_tests)))
            completed_indices = set()
            if name_lookup.get(config[FILE_CONFIG_KEY_TEST_ENTRY]):
                logger.info(f"[{adoc_path}] [INFO: Page entry point is '{config[FILE_CONFIG_KEY_TEST_ENTRY]}']")
                current_test_index = name_lookup[config[FILE_CONFIG_KEY_TEST_ENTRY]]
            else:
                raise ValueError(f"[{adoc_path}]: Didn't find declared test entry point")

            while True:
                if current_test_index in completed_indices:
                    raise ValueError(f"[{adoc_path}]: Attempted to execute the same test (number {current_test_index} on the page) twice")

                if current_test_index >= len(parsed_tests):
                    raise ValueError(f"[{adoc_path}]: Finished execution at end of page before running all tests")

                current_test = parsed_tests[current_test_index]
                self.try_test(current_test, current_test_index, adoc_path)
                remaining_indices.remove(current_test_index)
                completed_indices.add(current_test_index)

                if current_test.config.get(TEST_JUMP_KEY):
                    if name_lookup.get(current_test.config[TEST_JUMP_KEY]) is not None:
                        logger.info(f"[{adoc_path}] [INFO: jumping to '{current_test.config[TEST_JUMP_KEY]}']")
                        current_test_index = name_lookup[current_test.config[TEST_JUMP_KEY]]
                        continue
                    else:
                        raise ValueError(f"[{adoc_path}]: No test named {current_test.config[TEST_JUMP_KEY]} to jump to.")

                if len(remaining_indices) == 0:
                    break

                current_test_index += 1

        return None