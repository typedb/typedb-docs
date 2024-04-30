import requests

platforms = ['mac', 'linux', 'windows']
architectures = ['x86_64', 'arm64']
product_types = ['typedb-all', 'typedb-console', 'typedb-studio']

anchor_start = '^'
anchor_end = '$'

endpoint = "https://api.cloudsmith.io/v1/packages/typedb/public-release/"
query_params = f"?query=name:{anchor_start}"
latest = f" AND tag:{anchor_start}latest{anchor_end}"
sorting = f"&sort=-version"


def version_query_param(version) -> str:
    return f" AND version:{anchor_start}{version}{anchor_end}"


def get_released_version(product):
    skip = 0
    latest_version = get_version(product, skip)
    while '-rc' in latest_version:
        skip += 1
        latest_version = get_version(product, skip)
    return latest_version


def get_version(product, skip):
    page = 1 + skip
    os = platforms[0]
    arch = architectures[0]
    query = f"{endpoint}{query_params}{product}-{os}-{arch}{anchor_end}{sorting}&page={page}&page_size=1"
    response = requests.get(query)
    if response.ok:
        res = response.json()[0]["version"]
        return res
    else:
        print(f"Unexpected error trying to retrieve versions! Query: {query}")
        exit(1)
    # for result in response:
    #     return result['version']


def get_release_notes(product):
    match product:
        case 'typedb-all':
            gh_alias = 'typedb'
        case _:
            gh_alias = product
    product_version = get_released_version(product)
    release_notes_link = f"https://github.com/vaticle/{gh_alias}/releases/tag/{product_version}"
    return product_version, release_notes_link


if __name__ == "__main__":
    for product in product_types:
        with open(product + '-latest-links.adoc', 'w') as file:
            latest_released_version, link = get_release_notes(product)
            file.write(f"| \n{link}[{latest_released_version}]\n")
            with open(product + '-latest-version.adoc', 'w') as file2:
                file2.write(f"{latest_released_version}")
            for os in platforms:
                file.write(f"\n| \n// tag::{os}[]\n")
                for arch in architectures:
                    if (arch == 'arm64') and (os == 'windows'):
                        continue  # Such is life, no arm for Win
                    query = f"{endpoint}{query_params}{product}-{os}-{arch}{anchor_end}{version_query_param(latest_released_version)}"
                    response = requests.get(query)
                    if not response.ok:
                        print(f"Unexpected error trying to retrieve versions! Query: {query}")
                        continue
                    result = response.json()
                    if len(result) <= 0:
                        print(f"No results found: {product}-{os}-{arch}")
                        continue
                    download_link = result[0]['cdn_url']  # only the first result
                    if arch != architectures[0]:
                        file.write("/ ")
                    if requests.head(download_link).ok:
                        file.write(f"{download_link}[{arch}]\n")
                    else:
                        print(f"Link check failed: {download_link}")
                        continue
                file.write(f"// end::{os}[]\n")
    print("Processing is complete.")
