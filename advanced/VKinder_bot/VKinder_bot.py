from random import randrange
from config import token_vk_group, token_vk
from VKinder_json import _result_json, _get_offset
import time
import requests

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload

token = token_vk_group
token_vk = token_vk

vk = vk_api.VkApi(token=token)
upload = VkUpload(vk)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, attachments=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), 'attachment': attachments})


def _resp_check(method_name, params):
    """Служебная. Функция обработки ошибок."""
    url = f"https://api.vk.com/method/{method_name}"
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f'Request error: {response.status_code}'
    resp = response.json()
    if 'error' in resp:
        print(f"Server responded with error: {resp.get('error')}")
    else:
        return resp


def get_info(user_id):
    """Функция для формирования параметров поиска.ПЕРЕИМЕНОВАТЬ"""
    resp = _resp_check('users.get', params={'user_ids': user_id, 'fields': 'sex, bdate, city, relation',
                                            'access_token': token_vk, 'v': '5.131'})
    response = resp.get('response')
    search_params = []
    if 'sex' in response[0]:
        if response[0].get('sex') == 1:
            search_params.append(2)
        else:
            search_params.append(1)
    else:
        search_params.append('sex')
    if 'city' in response[0]:
        search_params.append(response[0].get('city').get('id'))
    else:
        search_params.append('city')
    if 'relation' in response[0]:
        search_params.append(response[0].get('relation'))
    else:
        search_params.append('relation')
    if 'bdate' in response[0]:
        bdate = response[0].get('bdate')
        birth_year_result = bdate.split('.')
        if len(birth_year_result) == 3:
            birth_year = birth_year_result[-1]
            search_params.append(birth_year)
        else:
            search_params.append('birth_year')
    else:
        search_params.append('birth_year')
    return search_params


def _user_search(sex, city, relation, birth_year, offset=1):
    """Служебная. Поиск по заданным параметрам."""
    resp = _resp_check('users.search',
                       params={'offset': offset, 'count': 20, 'fields': 'screen_name', 'sex': sex, 'city': city,
                               'status': relation, 'birth_year': birth_year, 'has_photo': 1, 'access_token': token_vk,
                               'v': '5.131'})
    response = resp.get('response').get('items')
    search_data = {}
    i = 1
    for item in response:
        if not item.get('is_closed') and i < 6:
            href = f"https://vk.com/{item.get('screen_name')}"
            time.sleep(0.5)
            search_data[href] = _search_result_get_photo(item.get('id'))
            i += 1
        else:
            pass
    return search_data


def _search_result_get_photo(user_id):
    """Служебная. Вытаскивает 3 самые популярные фотографии профиля."""
    resp = _resp_check('photos.get',
                       params={'owner_id': user_id, 'album_id': 'profile', 'access_token': token_vk, 'v': '5.131',
                               'extended': '1'})
    photo_chart = {}
    response = resp.get('response').get('items')
    for i, item in enumerate(response):
        photo_chart[i] = item.get('likes').get('count')
    sorted_tuple = sorted(photo_chart.items(), key=lambda x: x[1], reverse=True)
    photo_info_list = []
    for item in sorted_tuple[:3]:
        photo_info_list.append(f"photo{response[item[0]].get('owner_id')}_{response[item[0]].get('id')}")
    return photo_info_list


print('Start')
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "find":
                search_params = get_info(event.user_id)
                offset = _get_offset(event.user_id)
                search_params.append(offset)
                for item in search_params:
                    if item == 'sex':
                        search_params.remove(item)
                        write_msg(event.user_id, f"Please select your gender(1/2).")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    request = event.text
                                    break
                        search_params.insert(0, request)
                    elif item == 'city':
                        search_params.remove(item)
                        write_msg(event.user_id, f"Please select your city.")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    request = event.text
                                    break
                        search_params.insert(1, request)
                    elif item == 'relation':
                        search_params.remove(item)
                        write_msg(event.user_id, f"Please select your status.")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    request = event.text
                                    break
                        search_params.insert(2, request)
                    elif item == 'birth_year':
                        search_params.remove(item)
                        write_msg(event.user_id, f"Please specify your year of birth.")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    request = event.text
                                    break
                        search_params.insert(3, request)
                result = _user_search(*search_params)
                result['offset'] = int(offset) + 15
                _result_json(result, event.user_id)
                del(result['offset'])
                for item in result:
                    write_msg(event.user_id, f"{item}", ','.join(result[item]))
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")