import operator

text_dict = {}

with open('1.txt', 'r', encoding='utf-8') as file1:
    text1 = file1.read().strip()
    text_dict.setdefault('text1', text1)

with open('2.txt', 'r', encoding='utf-8') as file2:
    text2 = file2.read().strip()
    text_dict.setdefault('text2', text2)

with open('3.txt', 'r', encoding='utf-8') as file3:
    text3 = file3.read().strip()
    text_dict.setdefault('text3', text3)


sorted_tuples = sorted(text_dict.items(), key=operator.itemgetter(1), reverse=True)


with open('text.txt', 'w', encoding='utf-8') as text:
    for key, value in sorted_tuples:
        text.write(key + '\n')
        text.write(str(len(value.split('\n'))) + '\n')
        text.write(value + "\n")
