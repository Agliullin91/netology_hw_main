documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def get_doc_num_list():
    '''Создает список документов из каталога'''
    doc_num_list = []
    for item in documents:
        doc_num_list.append(item["number"])
    return doc_num_list


def people():
    '''Выводит владельца запрашиваемого документа.'''
    doc_number = input("Введите номер документа: ")
    if doc_number in get_doc_num_list():
        for item in documents:
            if doc_number == item["number"]:
                return item["name"]
            else:
                pass
    else:
        return "Документ с таким номером отсутсвует."


def shelf():
    '''Выводит номер полки на которой лежит запрашиваемый документ.'''
    doc_number = input("Введите номер документа: ")
    if doc_number in get_doc_num_list():
        for item in directories:
            if doc_number in directories[item]:
                return f"Документ найден на {item} полке."
            else:
                pass
    else:
        return "Документ с таким номером отсутсвует."


def person_list():
    '''Выводит список всех документов и их владельцев.'''
    for item in documents:
        print(f'{item["type"]} {item["number"]} {item["name"]}')


def add():
    '''Добавляет новый документ в каталог и на полку.'''
    doc_number = input("Укажите номер документа: ")
    doc_type = input("Укажите тип документа: ")
    doc_person = input("Укажите владельца документа: ")
    doc_shelf = input("Укажите полку для размещения документа: ")
    if doc_shelf in directories:
        documents.append({"type": doc_type, "number": doc_number, "name": doc_person})
        directories[doc_shelf].append(doc_number)
        return f"Документ добавлен на {doc_shelf} полку."
    else:
        return f"Документ не добавлен. Полки с таким номером не существует."


def delete():
    '''Удаляет документ из списка документов и с полки.'''
    doc_number = input("Введите номер документа: ")
    if doc_number in get_doc_num_list():
        for item in documents:
            if doc_number == item["number"]:
                documents.remove(item)
            else:
                pass
        for element in directories:
            if doc_number in directories[element]:
                directories[element].remove(doc_number)
            else:
                pass
        return f"Документ с номером {doc_number} удален."
    else:
        return "Документ с таким номером отсутсвует."


def move():
    '''Перемещает указанный документ на другую полку.'''
    doc_number = input("Введите номер документа: ")
    doc_shelf = input("Введите номер полки для размещения документа: ")
    if doc_number not in get_doc_num_list() or doc_shelf not in directories:
        return "Введенные номер документа или полки некорректны."
    else:
        for item in directories:
            if doc_number in directories[item]:
                directories[item].remove(doc_number)
        directories[doc_shelf].append(doc_number)
        return f"Документ с номером {doc_number} перемещен на {doc_shelf} полку."


def add_shelf():
    '''Добавляет полку для размещения документов.'''
    new_shelf = input("Укажите номер создаваемой полки: ")
    if new_shelf not in directories:
        directories[new_shelf] = []
        return directories
    else:
        return "Полка с таким номером уже существует."


def main():
    command_list = ['p', 's', 'l', 'a', 'd', 'm', 'as', 'q']
    while True:
        user_input = input("Введите команду: ")
        if user_input in command_list:
            if user_input == 'p':
                print(people())
            elif user_input == 's':
                print(shelf())
            elif user_input == 'l':
                print(person_list())
            elif user_input == 'a':
                print(add())
            elif user_input == 'd':
                print(delete())
            elif user_input == 'm':
                print(move())
            elif user_input == 'as':
                print(add_shelf())
            elif user_input == 'q':
                break
        else:
            print('Введите корректную команду.')


