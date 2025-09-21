class SaveObjects:
    def __init__(self, writer):
        self.write = writer

    def save(self, thing):
        typename = type(thing).__name__
        method = f'save_{typename}'
        assert hasattr(self, method), \
            f'Unknown object type {typename}'
        getattr(self, method)(thing)

    def save_int(self, thing):
        self._write('int', thing)

    def save_str(self, thing):
        lines = thing.split('\n')
        self._write('str', len(lines))
        for line in lines:
            print(line, file=self.writer)

class LoadObjects:
    def __init__(self, reader):
        self.reader = reader

    def load(self):
        line = self.reader.readline()[:-1]
        fields = line.split(":", maxsplit=1)
        assert len(fields) == 2, f"Badly-formed line {line}"
        key, value = fields

        method = f"load_{key}"
        assert hasattr(self, method), f"Unknown object type {key}"
        return getattr(self, method)(value)

    def load_float(self, value):
        return float(value)
