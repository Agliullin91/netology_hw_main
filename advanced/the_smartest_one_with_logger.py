import requests
import operator
from logger import logger_path


def search_hero_id(name: str, token=2619421814940190):
    url = f"https://superheroapi.com/api/{token}/search/{name}"
    response = requests.get(url)
    resp = response.json()
    hero_id = resp['results'][0]['id']
    # print(f"{name}'s id is {hero_id}")
    return hero_id


def get_hero_intelligence(id, token=2619421814940190):
    url = f"https://superheroapi.com/api/{token}/{id}/powerstats"
    response = requests.get(url)
    resp = response.json()
    hero_int = resp['intelligence']
    # print(f"{resp['name']}'s intelligence is {resp['intelligence']}")
    return hero_int

@logger_path('C:/netology_hw/advanced/mylog.log')
def whos_thesmartest_one(*names):
    heroes_int = {}
    for item in names:
        heroes_int[item] = int(get_hero_intelligence(search_hero_id(item)))
    sorted_tuples = sorted(heroes_int.items(), key=operator.itemgetter(1), reverse=True)
    print(f"{sorted_tuples[0][0]} is the most intelligent hero, with {sorted_tuples[0][1]} intelligence!")


whos_thesmartest_one('Hulk', 'Thanos', 'Captain America')
