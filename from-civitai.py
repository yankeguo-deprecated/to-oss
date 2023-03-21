import os
import sys
import requests

from requests.auth import AuthBase

from utils import oss_upload, curl_download


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def main():
    model_shasum = sys.argv[1].strip()

    print("model_shasum: " + model_shasum)

    r = requests.get(
        f"https://civitai.com/api/v1/model-versions/by-hash/{model_shasum}",
        auth=BearerAuth(os.getenv('CIVITAI_TOKEN')),
    )
    data = r.json()

    model_id = data['modelId']

    for item in data['files']:
        if 'hashes' not in item:
            continue
        hashes = item['hashes']
        if 'SHA256' not in hashes:
            continue
        item_shasum: str = hashes['SHA256']
        if item_shasum.lower() == model_shasum.lower():
            file_name = item['name']
            file_url = item['downloadUrl']

    print(f'downloading: {model_id}-{file_name}: {file_url}')

    local_file = os.path.join('data', file_name)

    curl_download(local_file, file_url)

    print("downloaded")

    oss_upload(f"models/civitai/{model_id}-{file_name}", local_file)

    print("done")


if __name__ == "__main__":
    main()
