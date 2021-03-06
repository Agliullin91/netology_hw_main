import requests
from pprint import pprint
import os
from pprint import pprint

token_ya = os.getenv('Token_YandexDisc', '1')


def get_files_list():
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
    headers = {'Authorization': token_ya}
    response = requests.get(files_url, headers=headers)
    return response.json()


def create_folder(folder_path):
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {'Authorization': token_ya}
    params = {"path": folder_path}
    response = requests.put(files_url, headers=headers, params=params)
    response.raise_for_status()
    return response.status_code


def _get_upload_link(disk_file_path):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {'Authorization': token_ya}
    params = {"path": disk_file_path, "overwrite": True}
    response = requests.get(upload_url, headers=headers, params=params)
    pprint(response.json())
    return response.json()


def upload_file_to_disk(disk_file_path, filename):
    href = _get_upload_link(disk_file_path=disk_file_path).get("href", "")
    response = requests.put(href, data=open(filename, 'rb'))
    response.raise_for_status()
    if response.status_code == 201:
        return response.status_code


# print(upload_file_to_disk(disk_file_path="netology_hw/text.txt", filename="text.txt"))
# pprint(get_files_list())
print(create_folder("test_folder"))