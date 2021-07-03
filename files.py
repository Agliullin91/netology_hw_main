from pprint import pprint


def crd(lst):
    result = {'ingredient_name': lst[0].strip(), 'quantity': lst[1].strip(), 'measure': lst[2].strip()}
    return result


cook_book = {}
ing_quantity = 0
with open('recipes.txt', 'r') as file:
    for line in file:
        food_name = line.strip()
        ing_quantity = int(file.readline().strip())

        ingredients_list = []
        for ing in range(ing_quantity):
            ingredients_list.append(crd(file.readline().split('|')))
        file.readline()
        cook_book[food_name] = ingredients_list

# Функция для вывода cook_book, т.к. pprint перемешивает блюда и ингридиенты при выводе.
def _print_d(dct):
    for item in dct:
        print(f'{item}:')
        for element in dct.get(item):
            print(f'{element}')
        print()

# Блок проверки: Задача №1
_print_d(cook_book)


def get_shop_list_by_dishes(person_count: int = 1, *dishes: str):
    shop_list = {}
    for item in cook_book:
        for element in dishes:
            if element == item:
                for i in cook_book.get(element):
                    if i['ingredient_name'] not in shop_list.keys():
                        ing_name = i['ingredient_name']
                        del(i['ingredient_name'])
                        i['quantity'] = int(i.get('quantity')) * person_count
                        shop_list[ing_name.strip()] = i
                    else:
                        temp = shop_list.get(i['ingredient_name'])
                        temp['quantity'] = int(temp.get('quantity')) + (int(i.get('quantity')) * person_count)
            else:
                pass
    pprint(shop_list)

# Блок проверки: Задача №2
get_shop_list_by_dishes(2, 'Омлет', 'Блины', 'Фахитос')
