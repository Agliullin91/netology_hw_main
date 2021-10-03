import hashlib


def generator_hash(path):
    with open(path) as f:
        line = 'Start'
        while len(line) != 0:
            line = f.readline()
            line_hash = hashlib.md5(line.encode()).hexdigest()
            value = f'{line_hash} - {line}'
            yield value
    print('End of execution')


if __name__ == '__main__':
    print(generator_hash('generator.txt'))
    for item in generator_hash('generator.txt'):
        print(item)
