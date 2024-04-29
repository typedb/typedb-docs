# from cloudsmith_api import api_client, configuration
import requests
import json
import os

# ACCESS_TOKEN = os.getenv('BULLSHIT')
ACCESS_TOKEN = None

PRODUCT_NAMES_N_URLS = \
    {
        'core':
            {
                'mac': {'x86_64': 'typedb-all-mac-x86_64', 'arm64': 'typedb-all-mac-arm64'},
                'linux': {'x86_64': 'typedb-all-linux-x86_64', 'arm64': 'typedb-all-linux-arm64'},
                'windows': {'x86_64': 'typedb-all-windows-x86_64', 'arm64': ''},
            },
        'console':
            {
                'mac': {'x86_64': '', 'arm64': ''},
                'linux': {'x86_64': '', 'arm64': ''},
                'windows': {'x86_64': '', 'arm64': ''},
            },
        'studio':
            {
                'mac': {'x86_64': '', 'arm64': ''},
                'linux': {'x86_64': '', 'arm64': ''},
                'windows': {'x86_64': '', 'arm64': ''},
            },
    }

# platforms = ['mac', 'linux', 'windows']
# architectures = ['x86_64', 'arm64']
# product_types = ['core', 'console', 'studio']
# PRODUCT_NAMES_N_URLS = \
#     { product: {platform: {arch: '' for arch in architectures} for platform in platforms} for product in product_types }
# print(PRODUCT_NAMES_N_URLS)

url = "https://api.cloudsmith.io/v1/packages/typedb/public-release/?query=name%3A"

headers = {
    "accept": "application/json",
    "X-Api-Key": ACCESS_TOKEN
}

sorting = "&query=tag%3Alatest&page_size=10&sort=-date"

for product in PRODUCT_NAMES_N_URLS:
    for os in PRODUCT_NAMES_N_URLS[product]:
        for arch in PRODUCT_NAMES_N_URLS[product][os]:
            if PRODUCT_NAMES_N_URLS[product][os][arch] != '':
                response = requests.get(url + PRODUCT_NAMES_N_URLS[product][os][arch] + sorting)
                print(PRODUCT_NAMES_N_URLS[product][os][arch])
                print("Presenting",
                      product,
                      os,
                      arch)
                for json in response.json():
                    print(json['version'], '---', json['name'], ', files:')
                    for file in json['files']:
                        print('    ', file['filename'])
                # print(response.text)


# print(response.links)
# print(response.text)

# for json in response.json():
#     print(json['version'], '---', json['name'], ', files:')
#     for file in json['files']:
#         print('    ', file['filename'])
    # print(json['name'])
    # print('---------')

# parsed = json.loads(response.text)
# print(json.dumps(parsed, indent=2))
