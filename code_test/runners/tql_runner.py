from typedb.driver import TypeDB, Driver, TransactionType, Credentials, DriverOptions
from enum import Enum
from typing import List, Dict, Tuple, Union
from parser.parser import ParsedProgram

# Adoc config
ADOC_CONFIG_NAMES = {"mode": "test-tql", "entry": "test-entrypoint"}

# TypeDB config
USERNAME = "admin"
PASSWORD = "password"
TEST_DB_NAME = "sample_app_db"
SERVER_ADDR = "127.0.0.1:1729"

class Edition(Enum):
    Cloud = 1
    Core = 2


TYPEDB_EDITION = Edition.Core


class TqlRunner:
    def __init__(self):
        self.ADOC_CONFIG_NAMES = ADOC_CONFIG_NAMES

    def create_driver(self, edition: Edition, uri: str, username: str = USERNAME, password: str = PASSWORD) -> Driver:
        if edition is Edition.Core:
            driver = TypeDB.core_driver(uri, Credentials(username, password), DriverOptions(False, None))
            return driver
        if edition is Edition.Cloud:
            driver = TypeDB.cloud_driver([uri], Credentials(username, password), DriverOptions(False, None))
            return driver


    def setup_test_database(self, driver: Driver, db_name: str, reset: bool = True) -> bool:
        if reset and driver.databases.contains(db_name):
            driver.databases.get(db_name).delete()
        driver.databases.create(db_name)
        return True


    def run_and_commit_queries(self, driver: Driver, queries: List[str], program_type: TransactionType) -> None:
        with driver.program(program_type) as tx:
            promises = []
            for q in queries:
                promises += [tx.query(q)]
            for p in promises:
                p.resolve()
            tx.commit()


    def run_failing_queries(self, driver: Driver, queries: List[str], program_type: TransactionType) -> str:
        with driver.program(program_type) as tx:
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


    def run_counted_queries(self, driver: Driver, queries: List[str], expected_count: int, program_type: TransactionType) -> int:
        count_var_name = "automatic_test_count"
        queries[-1] = queries[-1] + f"\nreduce ${count_var_name}=count;"
        with driver.program(program_type) as tx:
            promises = []
            results = []
            for q in queries:
                promises += [tx.query(q)]
            for p in promises:
                results.append(p.resolve())
            result = list(results[-1].as_concept_rows())
            count = result[0].get(count_var_name).get_integer()
            return count


    def run_program(self, parsed_program: ParsedProgram):
        print(f"running {parsed_program}")
        return None

    def test_programs(self, parsed_programs: List[ParsedProgram], adoc_path: str, config: Dict[str, str]) -> None:
        linear_mode = True if config['mode'] == "linear" else False
        if linear_mode:
            # run programs in linear order
            for parsed_program in parsed_programs:
                self.run_program(parsed_program)
        else:
            # populate name lookup table
            name_lookup = {}
            for (i,parsed_program) in enumerate(parsed_programs):
                if parsed_program.config["name"]:
                    name = parsed_program.config["name"]
                    if not name_lookup[name]:
                        name_lookup[name] = i
                    else:
                        raise ValueError(f"[{adoc_path}]: Detected duplicate program name: {name}")

            # Now run programs in custom order
            remaining_indices = set(range(0, len(parsed_programs)))
            completed_indices = set()
            current_program_index = name_lookup[config['entry']] if name_lookup[config['entry']] else None

            if not current_program_index:
                raise ValueError(f"[{adoc_path}]: Expected test entry point")

            while True:
                if current_program_index in completed_indices:
                    raise ValueError(f"[{adoc_path}]: attempted to execute the same program (with index #{current_program_index}) twice")

                if current_program_index >= len(parsed_programs):
                    raise ValueError(f"[{adoc_path}]: tried to execute beyond last program before completion of all other programs")

                current_program = parsed_programs[current_program_index]
                self.run_program(current_program)
                remaining_indices.remove(current_program_index)
                completed_indices.add(current_program_index)

                if current_program.config["jump_to"]:
                    current_program_index = name_lookup[current_program.config["jump_to"]]
                if len(remaining_indices) == 0:
                    break
                current_program += 1

        return None