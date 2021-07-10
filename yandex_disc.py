import requests
from pprint import pprint

with open('yandex_token.txt') as file:
    token = file.read()


def get_files_list():
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
    headers = {'Authorization': token}
    response = requests.get(files_url, headers=headers)
    return response.json()


def _get_upload_link(disk_file_path):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {'Authorization': token}
    params = {"path": disk_file_path, "overwrite": True}
    response = requests.get(upload_url, headers=headers, params=params)
    pprint(response.json())
    return response.json()


def upload_file_to_disk(disk_file_path, filename):
    href = _get_upload_link(disk_file_path=disk_file_path).get("href", "")
    response = requests.put(href, data=open(filename, 'rb'))
    response.raise_for_status()
    if response.status_code == 201:
        print("Success")


upload_file_to_disk(disk_file_path="netology_hw/text.txt", filename="text.txt")