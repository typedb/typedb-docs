# from cloudsmith_api import api_client, configuration
import requests
import json
import os

access_token = os.getenv('CLOUDSMITH_TOKEN')
products = {'core_server', 'console', 'studio', }
file_path = 'output.txt'

url = "https://api.cloudsmith.io/v1/packages/typedb/public-release/?page_size=500&sort=-date"

headers = {
    "accept": "application/json",
    "X-Api-Key": access_token
}

response = requests.get(url, headers=headers)
if response.ok:
    with open(file_path, 'w') as file:
        for result in response.json():
            file.write(json.dumps(result)+'\n')
else:
    print("Error:", response)
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

# for json1 in response.json():
#     print(json1)
#     print(json.dumps(json1))
#     print(type(json1))

