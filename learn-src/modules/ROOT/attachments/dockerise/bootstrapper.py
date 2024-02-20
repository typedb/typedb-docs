import argparse
import requests
import subprocess
import urllib
import yaml

from os import environ
from time import sleep

BOOTSTRAPPER_VERSION = "1.0.0"
DEFAULT_CONFIG_YML = "https://raw.githubusercontent.com/vaticle/typedb-docs/master/learn-src/modules/ROOT/attachments/config.yml"
PRINT_DEBUG = environ.get("DEBUG_BOOTSTRAPPER", "false").lower() != "false"
BOOTSTRAPPER_PORT = 1730

class TypeDBBootstrapperException(Exception):
    pass

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_yml', required=False, help="Override the config.yml used")
    parser.add_argument('--dataset_root', required=False, help="Override the dataset root")
    return parser.parse_args()

def http_get(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.text
    else:
        raise TypeDBBootstrapperException("Could not download sample.yml from: ", url)

def download_to_file(url, filepath):
    content = http_get(url)
    with open(filepath, "w") as f:
        f.write(content)


def _run_cmd(cmd, silent=None):
    if silent is None:
        silent = not PRINT_DEBUG
    output_to = subprocess.DEVNULL if silent else None
    result = subprocess.run(cmd, stdout=output_to, stderr=output_to)
    if result.returncode != 0:
        raise TypeDBBootstrapperException("Running command failed: " + " ".join(cmd))


def install_typedb(version):
    print("Installing TypeDB: " + version)
    _run_cmd(["apt", "update", "-y"])
    _run_cmd(["apt", "install", "-y", "default-jre", "typedb=%s"%version])
    version_output = subprocess.check_output(["typedb", "server", "--version"])
    version_line = version_output.decode().strip().split("\n")[-1]
    installed_version= version_line[len("Version:"):].strip()
    assert installed_version == version
    print("Successfully installed TypeDB: " + installed_version)

def start_typedb():
    print("Starting TypeDB for bootstrap")
    output_to = None if PRINT_DEBUG else subprocess.DEVNULL
    process = subprocess.Popen(["typedb","server", "--server.address=127.0.0.1:%d"%BOOTSTRAPPER_PORT], stdout=output_to, stderr=output_to )
    for i in range(10):
        try:
            console_command(["--command=database list"], i!=9)
            return process
        except TypeDBBootstrapperException as e:
            sleep(2)
    raise TypeDBBootstrapperException("Could not start typedb server")

def console_command(cmd, silent=True):
    return _run_cmd(["typedb", "console", "--core=127.0.0.1:%d"%BOOTSTRAPPER_PORT] + cmd, silent)

def install_datasets(dataset_root, datasets):
    for i, dataset in enumerate(datasets, start=1):
        print("%d/%d Loading %s"%(i, len(datasets), dataset))
        schema_file = "%s.schema.tql"%dataset
        data_file = "%s.data.tql"%dataset
        download_to_file(urllib.parse.urljoin(dataset_root, datasets[dataset]["schema"]), schema_file)
        download_to_file(urllib.parse.urljoin(dataset_root, datasets[dataset]["data"]), data_file)
        console_command(["--command=database create %s"%dataset])
        console_command(["--command=transaction %s schema write"%dataset, "--command=source %s"%schema_file, "--command=commit"])
        console_command(["--command=transaction %s data write"%dataset, "--command=source %s"%data_file, "--command=commit"])
        print("%d/%d Completed loading dataset: %s"%(i, len(datasets), dataset))
def main():
    try:
        args = parse_args()
        raw_yaml = http_get(DEFAULT_CONFIG_YML) if args.config_yml is None else open(args.config_yml, 'r').read()
        config = yaml.safe_load(raw_yaml)
        if config['bootstrapper-version'] != BOOTSTRAPPER_VERSION:
            raise TypeDBBootstrapperException("This bootstrapper is outdated and will not run. Please update to version: " + config['boostrapper-version'])
        if args.dataset_root is not None: config['dataset-root'] = args.dataset_root
        install_typedb(config['typedb-version'])
        with start_typedb() as typedb_process:
            try:
                install_datasets(config['dataset-root'], config['datasets'])
            finally:
                typedb_process.terminate()
                typedb_process.wait()
        print("Bootstrapping complete!")
    except Exception as e:
        print("Error during bootstrapping: " + str(e))
        raise e

if __name__ == "__main__": main()
