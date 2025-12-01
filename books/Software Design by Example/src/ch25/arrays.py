DIVIDER = ".data"

def assemble(self, lines):
    lines = self._get_lines(lines)
    to_compile, to_allocate = self._split(lines)

    labels = self._find_labels(lines)
    instructions = [ln for ln in to_compile if not self._is_label(ln)]

    base_of_data = len(instructions)
    self._add_allocations(base_of_data, labels, to_allocate)

    compiled = [self._compile(instr, labels) for instr in instructions]
    program = self._to_text(compiled)
    return program

def _split(self, lines):
    try:
        split = lines.index(self.DIVIDER)
        return lines[0:split], lines[split + 1:]
    except ValueError:
        return lines, []
