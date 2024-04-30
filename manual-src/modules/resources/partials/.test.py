import requests

platforms = ['mac', 'linux', 'windows']
architectures = ['x86_64', 'arm64']
product_types = ['typedb-all', 'typedb-console', 'typedb-studio']

anchor_start = '^'
anchor_end = '$'

url = "https://api.cloudsmith.io/v1/packages/typedb/public-release/?query=name:"
sorting = f" AND tag:{anchor_start}latest{anchor_end}&page_size=1"

# ACCESS_TOKEN = None
# headers = {
#     "accept": "application/json",
#     "X-Api-Key": ACCESS_TOKEN
# }

for product in product_types:
    for os in platforms:
        for arch in architectures:
            print("\nRequesting:", product, os, arch, end=" -- ")
            query = f"{url}{product}-{os}-{arch}{anchor_end}{sorting}"
            # print(query)
            response = requests.get(query)
            if response.ok:
                results = response.json()
                if len(results) > 0:
                    for result in results:
                        print(result['display_name'], result['version'])
                        # print(result)
                else:
                    print("No results found!")
            else:
                print("Error requesting the", query)
