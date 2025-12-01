class Writer:
    def __init__(self):
        self.seen = []

    def write(self, *args):
        self.seen.extend(args)

class Reader:
    def __init__(self, *args):
        self.commands = args
        self.index = 0

    def __call__(self, prompt):
        assert self.index < len(self.commands)
        self.index += 1
        return self.commands[self.index - 1]

def execute(source, reader, writer):
    program = Assembler().assemble(source.split("\n"), False)
    vm = VM(reader, writer)
    vm.initialize(program)
    vm.run()

def test_disassemble():
    source = """
    hlt
    """
    reader = Reader("d", "q")
    writer = Writer()
    execute(source, reader, writer)
    assert writer.seen == ["hlt | 0 | 0\n"]

def test_print_two_values():
    source = """
    ldc R0 55
    prr R0
    ldc R0 65
    prr R0
    hlt
    """
    reader = Reader("s", "s", "s", "q")
    writer = Writer()
    execute(source, reader, writer)
    assert writer.seen == [
        "000037\n"
    ]
