import requests

GITHUB_REPO = "vaticle/typedb"
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases"
FILENAME_ALL = "all-versions.adoc"
FILENAME_LATEST = "latest-version.adoc"
ERRORS = []


class Asset:
    def __init__(self, url=None, check=None):
        self.url = url
        self.check = check


class Arch:
    def __init__(self):
        self.arm = Asset()
        self.x86 = Asset()


class Release:
    def __init__(self, tag_name, rn_url):
        self.version = tag_name
        self.release_notes_url = rn_url
        self.assets = {
            "win": Arch(),
            "lin": Arch(),
            "mac": Arch()
        }

    def __str__(self, tags=False):
        result = ""
        result += f"\n| {self.release_notes_url}[{self.version}]\n"
        for os_key in ["mac", "lin", "win"]:
            result += '| '
            if tags:
                result += f"\n// tag::{os_key}[]\n"
            assets = self.assets[os_key]
            result += f"{assets.x86.url}[x86_64]"
            url_check_status = f"{assets.x86.check}"
            if assets.arm.url is not None:
                result += f" / {assets.arm.url}[arm64]"
                url_check_status += f" {assets.arm.check}"
            result += "\n"
            if tags:
                result += f"// end::{os_key}[]\n"
            result += f"// Check: {url_check_status}\n"
        return result


def check_url(url):
    """Check if the URL exists and accessible (status code < 400)."""
    return requests.head(url).ok


def get_versions(url):
    """Fetch all versions from the GitHub API and process them."""
    result = []
    response = requests.get(f"{url}?per_page=100")
    releases = response.json()
    for release in releases:
        if "rc" in release["name"]:
            print("Version " + release["tag_name"] + " IGNORED: skipping a release candidate version.")
            continue
        if "TypeDB" in release["name"]:
            print("Version " + release["tag_name"] + " will be processed.")
            result.append(get_release_data(release))
        else:
            print("Version " + release["tag_name"] + " IGNORED: no TypeDB in the name field.")
    return result


def get_release_data(release):
    """Process each release data and extract information."""
    release_data = Release(release["tag_name"], release["html_url"])
    for asset in release["assets"]:
        name = asset["name"].lower()
        if "typedb-all-linux" in name:
            if "arm64" in name:
                release_data.assets["lin"].arm.url, release_data.assets["lin"].arm.check = get_asset_data(asset)
            else:
                release_data.assets["lin"].x86.url, release_data.assets["lin"].x86.check = get_asset_data(asset)
        elif "typedb-all-mac" in name:
            if "arm64" in name:
                release_data.assets["mac"].arm.url, release_data.assets["mac"].arm.check = get_asset_data(asset)
            else:
                release_data.assets["mac"].x86.url, release_data.assets["mac"].x86.check = get_asset_data(asset)
        elif "typedb-all-windows" in name:
            if "arm64" in name:
                release_data.assets["win"].arm.url, release_data.assets["win"].arm.check = get_asset_data(asset)
            else:
                release_data.assets["win"].x86.url, release_data.assets["win"].x86.check = get_asset_data(asset)
    return release_data


def get_asset_data(asset):
    """Extract data from asset and verify URL."""
    global ERRORS
    url = asset["browser_download_url"]
    if check_url(url):
        check = "PASSED"
    else:
        check = "Fail"
        ERRORS.append(url)
    return url, check


def generate_table_contents(versions, tags=False):
    """Generate the table contents in asciidoc syntax."""
    result = ""
    for version in versions:
        result += version.__str__(tags)
    return result


def write_file(file_name, content):
    """Write content to the specified file."""
    with open(file_name, "w") as file:
        file.write(content)


def print_json(url):
    x = requests.get(url + "?per_page=100")
    json_data = x.json()
    for json_element in json_data:
        print(json_element)


if __name__ == "__main__":
    """Main workflow"""
    versions = get_versions(API_URL)

    all_downloads = generate_table_contents(versions)
    try:
        write_file(FILENAME_ALL, all_downloads)
        print("\nFile", FILENAME_ALL, "write complete!")
    except IOError:
        print("Error while writing file:", FILENAME_ALL)

    latest_downloads = generate_table_contents([versions[0]], True)
    try:
        write_file(FILENAME_LATEST, latest_downloads)
        print("\nFile", FILENAME_LATEST, "write complete!")
    except IOError:
        print("Error while writing file:", FILENAME_LATEST)

    for error in ERRORS:
        print("Warning! The following error occurred:", error)