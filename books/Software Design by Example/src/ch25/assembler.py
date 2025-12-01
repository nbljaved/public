class Assembler:
    def assemble(self, lines):
        lines = self._get_lines(lines)
        labels = self._find_labels(lines)
        instructions = [
            ln for ln in lines if not self._is_label(ln)
        ]
        compiled = [
            self._compile(instr, labels) for instr in instructions
        ]
        program = self._to_text(compiled)
        return program

    def _find_labels(self, lines):
        result = {}
        loc = 0
        for ln in lines:
            if self._is_label(ln):
                label = ln[:-1].strip()
                assert label not in result, f"Duplicated {label}"
                result[label] = loc
            else:
                loc += 1
        return result
    
    def _is_label(self, line):
        return line.endswith(":")

    def _compile(self, instruction, labels):
        tokens = instruction.split()
        op, args = tokens[0], tokens[1:]
        fmt, code = OPS[op]["fmt"], OPS[op]["code"]
    
        if fmt == "--":
            return self._combine(code)
    
        elif fmt == "r-":
            return self._combine(self._reg(args[0]), code)
    
        elif fmt == "rr":
            return self._combine(
                self._reg(args[1]), self._reg(args[0]), code
            )
    
        elif fmt == "rv":
            return self._combine(
                self._val(args[1], labels),
                self._reg(args[0]),
                code
            )

    def _val(self, token, labels):
        if token[0] != "@":
            return int(token)
        lbl = token[1:]
        assert lbl in labels, f"Unknown label '{token}'"
        return labels[lbl]

    def _combine(self, *args):
        assert len(args) > 0, "Cannot combine no arguments"
        result = 0
        for a in args:
            result <<= OP_SHIFT
            result |= a
        return result
