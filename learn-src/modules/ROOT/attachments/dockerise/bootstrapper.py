import requests
import subprocess
import yaml

SAMPLE_YML = "https://raw.githubusercontent.com/vaticle/typedb-docs/master/learn-src/modules/ROOT/attachments/samples.yml"
BOOTSTRAPPER_VERSION = "1.0.0"

def get_sample_yml():
    resp = requests.get(SAMPLE_YML)
    if resp.status_code == 200:
        return yaml.safe_load(resp.txt)
    else:
        print("Could not download sample.yml. Failing!")
        quit(1)

def install_typedb(version):
    subprocess.run("apt install software-properties-common apt-transport-https gpg")
    subprocess.run("gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 17507562824cfdcc")
    subprocess.run("gpg --export 17507562824cfdcc | sudo tee /etc/apt/trusted.gpg.d/vaticle.gpg > /dev/null")
    subprocess.run("echo \"deb https://repo.typedb.com/public/public-release/deb/ubuntu trusty main\" | sudo tee /etc/apt/sources.list.d/vaticle.list > /dev/null")
    subprocess.run("apt update")
    subprocess.run("apt install default-jre")
    subprocess.run("apt install typedb@%s"%version)
    installed_version = subprocess.check_output("typedb server --version")
    print(installed_version) # TODO: Assert instead


yml = get_sample_yml()
if yml['bootstrapper-version'] != BOOTSTRAPPER_VERSION:
    print("This boostrapper is outdated and will not run. Please update to version: ", yml['boostrapper-version'])
    quit(1)

install_typedb(yml['typedb-version'])

