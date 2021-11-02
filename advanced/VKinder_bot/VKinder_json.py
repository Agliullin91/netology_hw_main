import json
import os.path
from pprint import pprint


def _result_json(data, file_name):
    """Служебная. Создает json-файл с результатами поиска."""
    with open(f"{file_name}.json", "w") as write_file:
        json.dump(data, write_file)


def _get_offset(file_name):
    if os.path.exists(f"{file_name}.json"):
        with open(f"{file_name}.json", "r") as file:
            result = json.load(file)
            user_offset = result.get('offset')
    else:
        user_offset = 1
    return user_offset


def show_result(file_name):
    with open(f"{file_name}.json", "r") as file:
        result = json.load(file)
    print(len(result))
    pprint(result)


if __name__ == "__main__":
    show_result('340756722')