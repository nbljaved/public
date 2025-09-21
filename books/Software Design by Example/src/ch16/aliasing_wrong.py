from objects import SaveObjects, LoadObjects

class SaveAlias(SaveObjects):
    def __init__(self, writer):
        super().__init__(writer)
        self.seen = set()

    def save(self, thing):
        thing_id = id(thing)
        if thing_id in seen:
            self._write('alias', thing_id, "")
            return

        self.seen.add(thing_id)
        typename = type(thing).__name__
        method = f'save_{typename}'
        assert hasattr(self, method), f"Unknown object type {typename}"
        getattr(self, method)(thing)

    def save_list(self, thing):
        self._write('list', id(thing), len(thing))
        for item in thing:
            self.save(item)

class LoadAlias(LoadObjects):
    def __init__(self, reader):
        super().__init__(reader)
        self.seen = {} # dict (not a 'set' like in ReadAlias)

    def load(self):
        line = self.reader.readline()[:-1]
        assert line, "Nothing to read"
        fields = line.split(":", maxsplit=2)
        assert len(fields) == 3, f"Badly-formed line {line}"
        key, ident, value = fields

        # the lines below contain a bug
        # Q. What is the bug ???
        if key == 'alias':
            assert ident in self.seen
            return self.seen[ident]

        method = f'load_{key}'
        assert hasattr(self, method), f"Unknown object type {key}"
        result = getattr(self, method)(value)
        self.seen[ident] = result
        return result
