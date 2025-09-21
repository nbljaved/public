def save(writer, thing):
    if isinstance(thing, bool):
        print(f'bool:{thing}', file=writer)

    elif isinstance(thing, float):
        print(f'float:{thing}', file=writer)

    elif isinstance(thing, int):
        print(f'int:{thing}', file=writer)

    elif isinstance(thing, str):
        values = thing.split('\n')
        print(f'str:{len(values)}', file=writer)
        for value in values:
            print(value, file=writer)

    elif isinstance(thing, list):
        print(f'list:{len(thing)}', file=writer)
        for item in thing:
            save(writer, item)

    elif isinstance(thing, dict):
        print(f'dict:{len(thing)}', file=writer)
        for key, value in thing.items():
            save(writer, key)
            save(writer, value)

    else:
        raise ValueError(f'unknown type of thing {type(thing)}')

def load(reader):
    line = reader.readline()[:-1] # ignore the 'newline' character
    assert line, 'Nothing to read'
    fields = line.split(':', maxplit=1) # split of the first ':' from left to right
    assert len(fields) == 2, f'Badly formed line {line}'
    key, value = fields

    if key == 'bool':
        names = {'True': True,
                 'False': False,
                 }
        assert value in names, f'Unknown boolean {value}'
        return names[value]

    elif key == 'float':
        return float(value) # value is a string

    elif key == 'int':
        return int(value)

    elif key == 'str':
        # Unlike list and dict, the 'str:length'
        # is not something that to load we can call the 'load'
        # function recursively
        return '\n'.join([reader.readline()[:-1] # ignore the 'newline' character
                          for _ in range(int(value))])

    elif key == 'list':
        return [load(reader) for _ in range(int(value))]

    elif key == 'dict':
        return {load(reader): load(reader) for _ in range(int(value))}

    else:
        raise ValueError(f'unknown type of thing {line}')
