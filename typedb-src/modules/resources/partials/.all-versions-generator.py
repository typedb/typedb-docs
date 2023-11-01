import requests

repo = "https://api.github.com/repos/vaticle/typedb/releases"
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
        if "TypeDB" in json_element["name"]:
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
                               "url-arm": "",
                               "url-x86": "",
                               "hash": "",
                               "check": ""
                           },
                       "mac":
                           {
                               "url": "",
                               "url-arm": "",
                               "url-x86": "",
                               "hash": "",
                               "check": ""
                           }
                       }
            for asset in json_element["assets"]:
                # print(asset)
                if "typedb-all-linux" in asset["name"]:
                    if "typedb-all-linux-arm64" in asset["name"]:
                        # print(asset["browser_download_url"])
                        release["lin"]["url-arm"] = asset["browser_download_url"]
                        if not check_url(asset["browser_download_url"]):
                            errors.append(asset["browser_download_url"])
                            release["lin"]["check"] += "Fail "
                        else:
                            release["lin"]["check"] += "PASSED "

                    elif "typedb-all-linux-x86_64" in asset["name"]:
                        # print(asset["browser_download_url"])
                        release["lin"]["url-x86"] = asset["browser_download_url"]
                        if not check_url(asset["browser_download_url"]):
                            errors.append(asset["browser_download_url"])
                            release["lin"]["check"] += "Fail "
                        else:
                            release["lin"]["check"] += "PASSED "

                    else:
                        # print(asset["browser_download_url"])
                        release["lin"]["url"] = asset["browser_download_url"]
                        if not check_url(asset["browser_download_url"]):
                            errors.append(asset["browser_download_url"])
                            release["lin"]["check"] = "Fail"
                        else:
                            release["lin"]["check"] = "PASSED"

                elif "typedb-all-windows" in asset["name"]:
                    # print(asset["browser_download_url"])
                    if not check_url(asset["browser_download_url"]):
                        errors.append(asset["browser_download_url"])
                        release["win"]["check"] = "Fail"
                    else:
                        release["win"]["check"] = "PASSED"
                    release["win"]["url"] = asset["browser_download_url"]

                elif "typedb-all-mac" in asset["name"]:

                    if "typedb-all-mac-arm64" in asset["name"]:
                        # print(asset["browser_download_url"])
                        release["mac"]["url-arm"] = asset["browser_download_url"]
                        if not check_url(asset["browser_download_url"]):
                            errors.append(asset["browser_download_url"])
                            release["mac"]["check"] += "Fail "
                        else:
                            release["mac"]["check"] += "PASSED "

                    elif "typedb-all-mac-x86_64" in asset["name"]:
                        # print(asset["browser_download_url"])
                        release["mac"]["url-x86"] = asset["browser_download_url"]
                        if not check_url(asset["browser_download_url"]):
                            errors.append(asset["browser_download_url"])
                            release["mac"]["check"] += "Fail "
                        else:
                            release["mac"]["check"] += "PASSED "

                    else:
                        # print(asset["browser_download_url"])
                        release["mac"]["url"] = asset["browser_download_url"]
                        if not check_url(asset["browser_download_url"]):
                            errors.append(asset["browser_download_url"])
                            release["mac"]["check"] = "Fail"
                        else:
                            release["mac"]["check"] = "PASSED"

                    # print(asset["browser_download_url"])
                    # release["mac"]["url"] = asset["browser_download_url"]
                # else:
                #     errors.append(asset["name"] + ": unrecognized asset.")
            result.append(release)
            print(str(count) + ": version " + json_element["tag_name"] + " will be processed.")
        else:
            print(str(count) + ": version " + json_element["tag_name"] + " IGNORED: no TypeDB in the name field.")
    return result


def generate_table_contents(versions, hash=False, tags=False):
    result = ""
    for version in versions:
        result += '\n| ' + version["release_notes"] + '[' + version["version"] + ']' + '\n'
        # result += 'a|[,bash]' + '\n'
        # result += '----' + '\n'
        # result += 'docker pull vaticle/typedb:' + version["version"] + '\n'
        # result += '----' + '\n'

        for os in ["mac", "lin", "win"]:
            result += '|'
            if tags:
                result += '\n' + '// tag::' + os + '[]' + '\n'
            else:
                result += ' '
            if version[os]["url"] != "":
                result += version[os]["url"] + '[x86_64]' + '\n'
            else:
                if version[os]["url-x86"] != "":
                    result += version[os]["url-x86"] + '[x86_64] /'
                if version[os]["url-arm"] != "":
                    result += ' ' + version[os]["url-arm"] + '[arm64]' + '\n'

            if tags:
                result += '// end::' + os + '[]' + '\n'
            result += '// Check: ' + version[os]["check"] + '\n'
            if hash:
                result += '| ' + version[os]["hash"] + '[_SHA256_]' + '\n'
    return result


def write_file(file_name, content):
    with open(file_name, "w") as f:
        f.write(content)


def print_json(url):
    x = requests.get(url + "?per_page=100")
    json_data = x.json()
    for json_element in json_data:
        print(json_element)

# print_json(repo)

versions = get_versions(repo)
for error in errors:
    print("Warning! The following error occurred while checking asset urls:", error)

all_downloads = generate_table_contents(versions)
# print(all_downloads)
write_file(filename_all, all_downloads)
print("\nFile", filename_all, "write complete!")

latest_downloads = generate_table_contents([versions[0]], tags=True)
write_file(filename_latest, latest_downloads)
print("\nFile", filename_latest, "write complete!")
