import requests
import json
import os

access_token = os.getenv('CLOUDSMITH_TOKEN2')

url = "https://api.cloudsmith.io/v1/packages/typedb/public-release/?page_size=5&sort=-date"

headers = {
    "accept": "application/json",
    "X-Api-Key": access_token
}

response = requests.get(url, headers=headers)


def print_key_hierarchy(data, prefix=''):
    if isinstance(data, dict):
        for key in data:
            # Create a new prefix for nested keys
            new_prefix = f"{prefix}{key}."
            print_key_hierarchy(data[key], new_prefix)
    elif isinstance(data, list):
        # Handle list by iterating through each item
        for index, item in enumerate(data):
            # Create a prefix for items in lists
            list_prefix = f"{prefix}[{index}]."
            print_key_hierarchy(item, list_prefix)
    else:
        # Print the final key path when reaching a non-dictionary or non-list item
        print(prefix.rstrip('.'))


print_key_hierarchy(response.json())
