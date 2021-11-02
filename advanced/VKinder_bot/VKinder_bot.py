from random import randrange
from config import token_vk_group, token_vk
import time
import requests

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = token_vk_group
token_vk = token_vk

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


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
        sex = input('Please select your sex(1/2): ')
        if sex == 1:
            search_params.append(2)
        else:
            search_params.append(1)
    if 'city' in response[0]:
        search_params.append(response[0].get('city').get('id'))
    else:
        city = input('Please select your city: ')
        search_params.append(city)
    if 'relation' in response[0]:
        search_params.append(response[0].get('relation'))
    else:
        relation = input('Please select your relation: ')
        search_params.append(relation)
    if 'bdate' in response[0]:
        bdate = response[0].get('bdate')
        birth_year_result = bdate.split('.')
        if len(birth_year_result) == 3:
            birth_year = birth_year_result[-1]
            search_params.append(birth_year)
        else:
            birth_year = input('Please select your year of birth: ')
            search_params.append(birth_year)
    else:
        birth_year = input('Please select your year of birth: ')
        search_params.append(birth_year)
    return search_params


def _user_search(sex, city, relation, birth_year, offset=1):
    """Служебная. Поиск по заданным параметрам."""
    resp = _resp_check('users.search',
                       params={'offset': offset, 'count': 20, 'fields': 'screen_name', 'sex': sex, 'city': city,
                               'status': relation, 'birth_year': birth_year, 'has_photo': 1, 'access_token': token_vk,
                               'v': '5.131'})
    response = resp.get('response').get('items')
    search_data = {'offset': offset}
    i = 1
    for item in response:
        if not item.get('is_closed') and i < 3:
            href = f"https://vk.com/{item.get('screen_name')}"
            time.sleep(0.5)
            search_data[href] = _search_result_get_photo(item.get('id'))
            i += 1
        else:
            pass
    return search_data


def _get_biggest_photo(photo_list):
    """Служебная. Принимает на вход список фотографий разного размера и возвращает индекс фотографии макс. рамера."""
    b_size = 0
    index = 0
    for element in photo_list:
        size = element.get('height') * element.get('width')
        if size > b_size:
            b_size = size
            index = photo_list.index(element)
    return index


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
    photo_href_list = []
    for item in sorted_tuple[:3]:
        index = _get_biggest_photo(response[item[0]].get('sizes'))
        photo_href_list.append(response[item[0]].get('sizes')[index].get('url'))
    return photo_href_list


print('Start')
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "N":
                write_msg(event.user_id, f"{_user_search(*get_info(event.user_id))}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
