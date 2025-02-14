from typedb.driver import TypeDB, Driver, TransactionType, Credentials, DriverOptions
from enum import Enum
from typing import List, Dict, Tuple, Union
from code_test.parser.parser import ParsedProgram
import logging
logger = logging.getLogger('main')

# Poor man's testing grammar (keywords used in .adoc files)
## .adoc attribute keys and values
ADOC_TEST_KEY = "test-tql"
ADOC_ENTRYPOINT_KEY = "test-tql-entry"
ADOC_CONFIG_KEYS = [ADOC_TEST_KEY, ADOC_ENTRYPOINT_KEY] # first item should be the test key
TEST_MODE_LINEAR_VAL = "linear"
TEST_MODE_CUSTOM_VAL = "custom"
MODE_LIST = [TEST_MODE_LINEAR_VAL, TEST_MODE_CUSTOM_VAL]
## program attribute keys and values
PROGRAM_NAME_KEY = "name"
PROGRAM_RESET_KEY = "reset"
PROGRAM_TRANSACTION_TYPE_KEY = "type"
PROGRAM_ROLLBACK_KEY = "rollback"
PROGRAM_JUMP_KEY = "jump"
PROGRAM_FAIL_KEY = "fail_at"
PROGRAM_FAIL_COMMIT_VAL = "commit"
PROGRAM_FAIL_RUNTIME_VAL = "runtime"
PROGRAM_COUNT_KEY = "count"


class Edition(Enum):
    Cloud = 1
    Core = 2


class FailureMode(Enum):
    Runtime = 1
    Commit = 2
    NoFailure = 3


class TqlRunner:
    def __init__(self):
        # Required
        self.adoc_keys = ADOC_CONFIG_KEYS
        self.success_count = 0
        self.failure_count = 0

        # Tql specific
        self.edition = Edition.Core
        self.username = "admin"
        self.password = "password"
        self.db = "docs_test"
        self.uri = "127.0.0.1:1729"
        self.driver = self.create_driver()

    def create_driver(self) -> Driver:
        if self.edition is Edition.Core:
            driver = TypeDB.core_driver(self.uri, Credentials(self.username, self.password), DriverOptions(False, None))
            return driver
        if self.edition is Edition.Cloud:
            driver = TypeDB.cloud_driver([self.uri], Credentials(self.username, self.password), DriverOptions(False, None))
            return driver

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
        if adoc_config.get(ADOC_TEST_KEY) not in ["linear", "custom"]:
            logger.info(f"adoc attribute :{ADOC_TEST_KEY}: must be set to either 'linear' or 'custom'")
            return False
        elif adoc_config[ADOC_TEST_KEY] == "custom" and adoc_config.get(ADOC_ENTRYPOINT_KEY) is None:
            logger.info(f"adoc attribute :{ADOC_ENTRYPOINT_KEY}: must be set to some program name for 'custom' test")
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

    def run_queries(self, queries: List[str], type: TransactionType, counted=False, rollback=False) -> Union[int, None]:
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
                    tx.close()
                else:
                    tx.commit()
                if counted:
                    result = list(results[-1].as_concept_rows())
                    count = result[0].get(count_var_name).get_integer()
                    return count
            except Exception as e:
                raise Exception(f"{e}") from e

    def run_program(self, parsed_program: ParsedProgram, adoc_path: str):
        # logger.info(f"... program source:\n{parsed_program}")

        type = None
        if parsed_program.config.get(PROGRAM_TRANSACTION_TYPE_KEY):
            match parsed_program.config[PROGRAM_TRANSACTION_TYPE_KEY]:
                case "schema":
                    type = TransactionType.SCHEMA
                case "write":
                    type = TransactionType.WRITE
                case "read":
                    type = TransactionType.READ

        if type is None:
            raise ValueError(f"[{adoc_path}]: Missing '{PROGRAM_TRANSACTION_TYPE_KEY}' attribute from program")

        rollback = False
        if parsed_program.config.get(PROGRAM_ROLLBACK_KEY):
            rollback = True

        if parsed_program.config.get(PROGRAM_RESET_KEY):
            self.setup_db(reset=True)

        counted = False
        if parsed_program.config.get(PROGRAM_COUNT_KEY):
            reference_count = int(parsed_program.config[PROGRAM_COUNT_KEY])
            counted = True

        if parsed_program.config.get(PROGRAM_FAIL_KEY):
            ref_failure_mode = FailureMode.NoFailure
            match parsed_program.config[PROGRAM_FAIL_KEY]:
                case x if x == PROGRAM_FAIL_RUNTIME_VAL:
                    ref_failure_mode = FailureMode.Runtime
                case x if x == PROGRAM_FAIL_COMMIT_VAL:
                    ref_failure_mode = FailureMode.Commit
            failure_mode = self.run_failing_queries(parsed_program.blocks, type)
            if failure_mode != ref_failure_mode:
                raise RuntimeError(f"[{adoc_path}]: Failure mode: expected {ref_failure_mode} but got {failure_mode}")
        elif counted == True:
            count = self.run_queries(parsed_program.blocks, type, counted, rollback)
            if count != reference_count:
                raise RuntimeError(f"[{adoc_path}]: Query count: expected {reference_count} but got {count}")
        else:
            self.run_queries(parsed_program.blocks, type, counted, rollback)

        return None

    def test_program(self, parsed_program: ParsedProgram, index: int, adoc_path: str):
        try:
            logger.info(f"[{adoc_path}] Running program #{index} ...")
            self.run_program(parsed_program, adoc_path)
            logger.info(f"[{adoc_path}] ... SUCCESS")
            self.success_count += 1
        except Exception as e:
            logger.info(f"[{adoc_path}] ... ERROR:\n{e}")
            self.failure_count += 1

    def test_programs(self, parsed_programs: List[ParsedProgram], adoc_path: str, config: Dict[str, str]) -> None:
        self.setup_db(reset=True)  # Resets the database
        self.reset_counts()

        if config[ADOC_TEST_KEY] == TEST_MODE_LINEAR_VAL:
            # run programs in linear order
            for (i, parsed_program) in enumerate(parsed_programs):
                self.test_program(parsed_program, i, adoc_path)

        elif config[ADOC_TEST_KEY] == TEST_MODE_CUSTOM_VAL:
            # populate name lookup table
            name_lookup = {}
            for (i,parsed_program) in enumerate(parsed_programs):
                if parsed_program.config.get(PROGRAM_NAME_KEY):
                    name = parsed_program.config[PROGRAM_NAME_KEY]
                    if not name_lookup.get(name):
                        name_lookup[name] = i
                    else:
                        raise ValueError(f"[{adoc_path}]: Detected duplicate program name: {name}")

            # Now run programs in custom order
            remaining_indices = set(range(0, len(parsed_programs)))
            completed_indices = set()
            if name_lookup.get(config[ADOC_ENTRYPOINT_KEY]):
                logger.info(f"[{adoc_path}] [INFO: Page entry point is '{config[ADOC_ENTRYPOINT_KEY]}']")
                current_program_index = name_lookup[config[ADOC_ENTRYPOINT_KEY]]
            else:
                raise ValueError(f"[{adoc_path}]: Didn't find declared test entry point")

            while True:
                if current_program_index in completed_indices:
                    raise ValueError(f"[{adoc_path}]: Attempted to execute the same program (number {current_program_index} on the page) twice")

                if current_program_index >= len(parsed_programs):
                    raise ValueError(f"[{adoc_path}]: Finished execution at end of page before running all programs")

                current_program = parsed_programs[current_program_index]
                self.test_program(current_program, current_program_index, adoc_path)
                remaining_indices.remove(current_program_index)
                completed_indices.add(current_program_index)

                if current_program.config.get(PROGRAM_JUMP_KEY):
                    if name_lookup.get(current_program.config[PROGRAM_JUMP_KEY]) is not None:
                        logger.info(f"[{adoc_path}] [INFO: jumping to '{current_program.config[PROGRAM_JUMP_KEY]}']")
                        current_program_index = name_lookup[current_program.config[PROGRAM_JUMP_KEY]]
                        continue
                    else:
                        raise ValueError(f"[{adoc_path}]: No program named {current_program.config[PROGRAM_JUMP_KEY]} to jump to.")

                if len(remaining_indices) == 0:
                    break

                current_program_index += 1

        return None