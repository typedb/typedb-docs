import requests

repo = "https://api.github.com/repos/vaticle/typedb-studio/releases"
filename_all = "all-versions.adoc"
filename_latest = "latest-version.adoc"
errors = []


def check_url(url):
    if requests.head(url).status_code < 400:
        return True
    else:
        return False


def get_versions(url):
    x = requests.get(url + "?per_page=100")
    json_data = x.json()
    result = []
    count = 0
    for json_element in json_data:
        count += 1
        # print(json_element["tag_name"] + ": " + json_element["name"])
        if ("TypeDB" in json_element["name"]) \
                and ("TypeDB Workbase" not in json_element["name"]) \
                and ("alpha" not in json_element["name"]):
            release = {"version": json_element["tag_name"],
                       "release_notes": json_element["html_url"],
                       "win":
                           {
                               "url": "",
                               "hash": "",
                               "check": ""
                           },
                       "lin":
                           {
                               "url": "",
                               "hash": "",
                               "check": ""
                           },
                       "mac":
                           {
                               "url": "",
                               "hash": "",
                               "check": ""
                           }
                       }
            for asset in json_element["assets"]:
                # print(asset)
                if "typedb-studio-linux" in asset["name"]:
                    # print(asset["browser_download_url"])
                    if not check_url(asset["browser_download_url"]):
                        errors.append(asset["browser_download_url"])
                        release["lin"]["check"] = "Fail"
                    else:
                        release["lin"]["check"] = "PASSED"
                    release["lin"]["url"] = asset["browser_download_url"]
                elif "typedb-studio-windows" in asset["name"]:
                    # print(asset["browser_download_url"])
                    if not check_url(asset["browser_download_url"]):
                        errors.append(asset["browser_download_url"])
                        release["win"]["check"] = "Fail"
                    else:
                        release["win"]["check"] = "PASSED"
                    release["win"]["url"] = asset["browser_download_url"]
                elif "typedb-studio-mac" in asset["name"]:
                    if not check_url(asset["browser_download_url"]):
                        errors.append(asset["browser_download_url"])
                        release["mac"]["check"] = "Fail"
                    else:
                        release["mac"]["check"] = "PASSED"
                    # print(asset["browser_download_url"])
                    release["mac"]["url"] = asset["browser_download_url"]
                else:
                    errors.append(asset["name"] + ": unrecognized asset.")
            result.append(release)
            print(str(count) + ": version " + json_element["tag_name"] + " will be processed.")
        else:
            print(str(count) + ": version " + json_element["tag_name"]
                  + " IGNORED: no TypeDB Studio in the name field (or alpha).")
    return result


def generate_table_contents(versions, hash=False):
    result = ""
    for version in versions:
        result += '\n| ' + version["release_notes"] + '[' + version["version"] + ']' + '\n'
        for os in ["win", "lin", "mac"]:
            result += '| ' + version[os]["url"] + '[Download]' + '\n'
            result += '// Check: ' + version[os]["check"] + '\n'
            if hash:
                result += '| ' + version[os]["hash"] + '[_SHA256_]' + '\n'
    return result


def write_file(file_name, content):
    with open(file_name, "w") as f:
        f.write(content)


versions = get_versions(repo)
for error in errors:
    print("Warning! The following error occurred while checking asset urls:", error)

all_downloads = generate_table_contents(versions)
# print(all_downloads)
write_file(filename_all, all_downloads)
print("\nFile", filename_all, "write complete!")

latest_downloads = generate_table_contents([versions[0]])
write_file(filename_latest, latest_downloads)
print("\nFile", filename_latest, "write complete!")
