import requests
from pprint import pprint
import os
from pprint import pprint

token_ya = os.getenv('Token_YandexDisc', '1')


def get_files_list():
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
    headers = {'Authorization': token_ya}
    response = requests.get(files_url, headers=headers)
    return response.json(), response.status_code


def get_file_meta(file_path):
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {'Authorization': token_ya}
    params = {'path': file_path}
    response = requests.get(files_url, headers=headers, params=params)
    return response.json(), response.status_code


def create_folder(folder_path):
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {'Authorization': token_ya}
    params = {"path": folder_path}
    response = requests.put(files_url, headers=headers, params=params)
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
telo = get_files_list()
print(telo[1])
# for item in telo[0]:
#     print(item[''])
# print(create_folder("test_folder"))
print(get_file_meta("test_folder1"))
print(get_file_meta("test_folder"))