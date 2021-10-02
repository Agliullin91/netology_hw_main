import json
from pprint import pprint
import re

with open("countries.json") as f:
    country_list = json.load(f)


class CountryIterator:

    with open("countries.json") as f:
        country_list = json.load(f)

    def get_country(self, country_id):
        country = country_list[country_id]['name']['common']
        return country

    def __iter__(self):
        self.cursor = 0
        return self

    def __next__(self):
        if self.cursor == len(country_list):
            raise StopIteration
        country = self.get_country(self.cursor)
        self.cursor += 1
        return country


URL = 'https://en.wikipedia.org/wiki/'
data = {}

for item in CountryIterator():
    result = re.sub(r'\s', '_', item)
    data[item] = f'{URL}{result}'

pprint(data)
with open("countries_links.json", "w") as write_file:
    json.dump(data, write_file)
print(f'JSON file created. {write_file}')


# if __name__ == '__main__':
