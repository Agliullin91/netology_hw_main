from random import randrange
from config import token_vk_group, token_vk
import time
import requests
from VKinder_db import Database
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload

token = token_vk_group
token_vk = token_vk


class VK:

    def __init__(self, token):
        self.token = token

    def _resp_check(self, method_name, params):
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

    def _get_search_params(self, user_id):
        """Служебная. Функция для формирования параметров поиска."""
        resp = self._resp_check('users.get', params={'user_ids': user_id, 'fields': 'sex, bdate, city, relation',
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

    def _user_search(self, sex, city, relation, birth_year, offset=1):
        """Служебная. Поиск по заданным параметрам."""
        resp = self._resp_check('users.search',
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
                search_data[href] = self._search_result_get_photo(item.get('id'))
                i += 1
            else:
                pass
        return search_data

    def _search_result_get_photo(self, user_id):
        """Служебная. Вытаскивает 3 самые популярные фотографии профиля."""
        resp = self._resp_check('photos.get',
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


class Bot:

    def __init__(self, token, VK_cls, Database):
        self.token = token
        self.VK = VK_cls
        self.Database = Database
        self.vk = vk_api.VkApi(token=self.token)
        self.upload = VkUpload(self.vk)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message, attachments=None):
        """Функция отправки сообщения пользователю."""
        self.vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), 'attachment': attachments})

    def _get_param(self, param, search_params, user_id, index):
        """Служебная. Спрашивает недостающий параметр поиска у пользователя."""
        search_params.remove(param)
        self.write_msg(user_id, f"Please select your {param}.")
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                break
        search_params.insert(index, request)

    def db_check(self, user_id):
        if self.Database.connection is None:
            self.write_msg(user_id, 'База данных поиска недоступна. Результаты поиска могут повторяться.')
        else:
            pass

    def start_bot(self):
        """Основная функция. Запускает бота."""
        print('Start')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text

                    if request == "привет":
                        self.write_msg(event.user_id, f"Хай, {event.user_id}")
                    elif request == "find":
                        search_params = self.VK._get_search_params(event.user_id)
                        self.db_check(event.user_id)
                        offset = self.Database._get_offset('Search', event.user_id)[0]
                        search_params.append(offset)
                        for item in search_params:
                            if item == 'sex':
                                self._get_param('sex', search_params, event.user_id, 0)
                            elif item == 'city':
                                self._get_param('city', search_params, event.user_id, 1)
                            elif item == 'relation':
                                self._get_param('relation', search_params, event.user_id, 2)
                            elif item == 'birth_year':
                                self._get_param('birth_year', search_params, event.user_id, 3)
                        result = self.VK._user_search(*search_params)
                        result['offset'] = int(offset) + 15
                        self.Database.insert_result(event.user_id, result)
                        del(result['offset'])
                        for item in result:
                            self.write_msg(event.user_id, f"{item}", ','.join(result[item]))
                    elif request == "пока":
                        self.write_msg(event.user_id, "Пока((")
                    else:
                        self.write_msg(event.user_id, "Не поняла вашего ответа...")


VK1 = VK(token_vk)
Database1 = Database('postgresql://vkinder:1234@localhost:5433/vkinder')
Bot1 = Bot(token_vk_group, VK1, Database1)

if __name__ == "__main__":
    Bot1.start_bot()