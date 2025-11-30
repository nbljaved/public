class LoggingHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.debug("server about to start receiving")
        data = bytes()
        while True:
            latest = self.request.recv(BLOCK_SIZE)
            self.debug(f"...server received {len(latest)} bytes")
            data += latest
            if len(latest) < BLOCK_SIZE:
                self.debug(f"...server breaking")
                break
        self.debug(f"server finished received, about to reply")
        self.request.sendall(bytes(f"{len(data)}", "utf-8"))

def debug(self, *args):
    print(*args)
