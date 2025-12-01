def _do_memory(self, addr):
    self.show()
    return True

def _do_step(self, addr):
    self.state = VMState.STEPPING
    return False

def interact(self, addr):
    prompt = "".join(sorted({key[0] for key in self.handlers}))
    interacting = True
    while interacting:
        try:
            command = self.read(f"{addr:06x} [{prompt}]> ")
            if not command:
                continue
            elif command not in self.handlers:
                self.write(f"Unknown command {command}")
            else:
                interacting = self.handlers[command](self.ip)
        except EOFError:
            self.state = VMState.FINISHED
            interacting = False

def __init__(self, reader=input, writer=sys.stdout):
    super().__init__(reader, writer)
    self.handlers = {
        "d": self._do_disassemble,
        "dis": self._do_disassemble,
        "i": self._do_ip,
        "ip": self._do_ip,
        "m": self._do_memory,
        "memory": self._do_memory,
        "q": self._do_quit,
        "quit": self._do_quit,
        "r": self._do_run,
        "run": self._do_run,
        "s": self._do_step,
        "step": self._do_step,
    }
