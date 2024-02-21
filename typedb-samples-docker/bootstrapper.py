import os
import requests
import subprocess
import urllib
import yaml

from time import sleep

BOOTSTRAPPER_VERSION = "0.0.3"  # Will fail if the config.yml is of a different version.
DEFAULT_CONFIG_YML = "https://raw.githubusercontent.com/vaticle/typedb-docs/master/typedb-samples-docker/config.yml"
BOOTSTRAPPER_PORT = 1730 # during dataset loading, typedb runs on a different port to to remain unreachable.

VERBOSE = os.environ.get("BOOTSTRAPPER_VERBOSE", "false").lower() != "false"
# Overrides for testing with local files
CONFIG_OVERRIDE = os.environ.get("BOOTSTRAPPER_CONFIG", None)
DATASET_ROOT_OVERRIDE = os.environ.get("BOOTSTRAPPER_DATASET_ROOT", None)

class TypeDBBootstrapperException(Exception):
    pass

def _is_url(s):
    return s.startswith("https://") or s.startswith("http://")

def _http_get(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.text
    else:
        raise TypeDBBootstrapperException("Could not download sample.yml from: " + url)

def _console_command(cmd, silence_errors=False):
    return _run_cmd(["typedb", "console", "--core=127.0.0.1:%d"%BOOTSTRAPPER_PORT] + cmd, silence_errors)

def _run_cmd(cmd, silence_errors=False):
    stdout_to = None if VERBOSE else subprocess.DEVNULL
    stderr_to = subprocess.DEVNULL if silence_errors and not VERBOSE else None
    result = subprocess.run(cmd, stdout=stdout_to, stderr=stderr_to)
    if result.returncode != 0:
        raise TypeDBBootstrapperException("Running command failed: " + " ".join(cmd))

def load_config(config_path):
    if CONFIG_OVERRIDE is not None:
        print("BOOTSTRAPPER_CONFIG was defined. Loading config from %s"%CONFIG_OVERRIDE)
        raw_yaml = _http_get(CONFIG_OVERRIDE) if _is_url(CONFIG_OVERRIDE) else open(CONFIG_OVERRIDE, 'r').read()
    else:
        print("Loading config from %s"%config_path)
        raw_yaml = _http_get(config_path)
    return yaml.safe_load(raw_yaml)

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
    output_to = None if VERBOSE else subprocess.DEVNULL
    process = subprocess.Popen(["typedb","server", "--server.address=127.0.0.1:%d"%BOOTSTRAPPER_PORT], stdout=output_to, stderr=output_to)
    for i in range(10):
        try:
            _console_command(["--command=database list"], i != 9)
            return process
        except TypeDBBootstrapperException as e:
            sleep(2)
    raise TypeDBBootstrapperException("Could not start typedb server")

def _download_dataset(from_root, from_relative, to_path):
    if DATASET_ROOT_OVERRIDE is not None:
        content = _http_get(urllib.parse.urljoin(DATASET_ROOT_OVERRIDE, from_relative)) if _is_url(DATASET_ROOT_OVERRIDE) else open(os.path.join(DATASET_ROOT_OVERRIDE, from_relative), 'r').read()
    else:
        content = _http_get(urllib.parse.urljoin(from_root, from_relative))
    with open(to_path, "w") as f:
        f.write(content)

def install_datasets(dataset_root, datasets):
    if DATASET_ROOT_OVERRIDE is not None:
        print("BOOTSTRAPPER_DATASET_ROOT detected. Datasets will be loaded from: ", DATASET_ROOT_OVERRIDE)
    else:
        print("Loading datasets from: ", dataset_root)

    for i, dataset in enumerate(datasets, start=1):
        print("%d/%d Loading %s"%(i, len(datasets), dataset))
        schema_file = "%s.schema.tql"%dataset
        data_file = "%s.data.tql"%dataset
        _download_dataset(dataset_root, datasets[dataset]["schema"], schema_file)
        _download_dataset(dataset_root, datasets[dataset]["data"], data_file)
        _console_command(["--command=database create %s" % dataset])
        _console_command(["--command=transaction %s schema write" % dataset, "--command=source %s" % schema_file, "--command=commit"])
        _console_command(["--command=transaction %s data write" % dataset, "--command=source %s" % data_file, "--command=commit"])
        print("%d/%d Completed loading dataset: %s"%(i, len(datasets), dataset))

def main():
    try:
        config = load_config(DEFAULT_CONFIG_YML)
        if config['bootstrapper-version'] != BOOTSTRAPPER_VERSION:
            raise TypeDBBootstrapperException("This bootstrapper is outdated and will not run. Please update to version: " + config['bootstrapper-version'])
        install_typedb(config['typedb-version'])
        with start_typedb() as typedb_process:
            try:
                install_datasets(config['dataset-root'], config['datasets'])
            finally:
                print("Shutting down TypeDB.")
                typedb_process.terminate()
                typedb_process.wait()
        print("Bootstrapping complete!")
    except Exception as e:
        print("Error during bootstrapping. Run with environment variable BOOTSTRAPPER_VERBOSE=True for subcommand output")
        if VERBOSE:
            raise e
        else:
            print(str(e))
            quit(1)

if __name__ == "__main__": main()
