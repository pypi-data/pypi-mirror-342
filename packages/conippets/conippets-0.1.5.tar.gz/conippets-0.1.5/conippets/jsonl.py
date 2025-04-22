from conippets import json

def read(file, encoding='utf-8', eager=True):
    f = open(file, mode='r', encoding=encoding)
    def make_generator(f):
        yield from (json.loads(line) for line in f)
        f.close()
    if eager:
        return list(make_generator(f))
    else:
        return make_generator(f)

def __writelines__(file, data, *, mode, encoding):
    with open(file, mode=mode, encoding=encoding) as f:
        for item in data:
            line = json.dumps(item, ensure_ascii=False, indent=None)
            f.write(line + '\n')

def write(file, data, encoding='utf-8'):
    __writelines__(file, data, mode='w', encoding=encoding)

def append(file, data, encoding='utf-8'):
    __writelines__(file, data, mode='a', encoding=encoding)