from pprint import pprint
import csv
import re


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)
print()

# Блок исправления ФИО
for item in contacts_list[1:]:
    it_join = ' '.join(item[:3])
    it_split = it_join.strip().split(' ')
    for i, element in enumerate(it_split):
        item[i] = it_split[i]


# Блок правки номеров телефонов
for item in contacts_list[1:]:
    number = item[5]
    result1 = re.sub(r'^8', '+7', number)
    result2 = re.sub(r'\+7\s*\D*495\D*\s*', '+7(495)', result1)
    result3 = re.sub(r'(\)\d{3})(\s|-)*(\d{2})(\s|-)*(\d+)', r'\1-\3-\5', result2)
    result4 = re.sub(r'\s*\(*доб.\s*(\d+)\)*', r' доб.\1', result3)
    item[5] = result4


# Блок удаления дубликатов.Часть 1 (перенос дубликатов в отдельный список)
name_list = []
duplicate_list = []
for item in contacts_list[1:]:
    if ' '.join(item[0:2]) not in name_list:
        name_list.append(' '.join(item[0:2]))
    else:
        for element in contacts_list[1:]:
            if item == element:
                duplicate_list.append(item)
                contacts_list.remove(element)


# Блок удаления дубликатов.Часть 2 (добаление заполненных строк из дубликатов в пустые строки основного списка)
for item in duplicate_list:
    for element in contacts_list:
        if item[0] == element[0] and item[1] == element[1]:
            for i, n in enumerate(element):
                if item[i] != '':
                    element[i] = item[i]

print()
for item in contacts_list:
    print(item)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)


# if __name__ == '__main__':
