class FileHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("server about to start receiving")
        data = bytes()
        while True:
            latest = self.request.recv(CHUNK_SIZE)
            print(f"...server received {len(latest)} bytes")
            data += latest
            if len(latest) < CHUNK_SIZE:
                print(f"...server breaking")
                break
        print(f"server finished received, about to reply")
        self.request.sendall(bytes(f"{len(data)}", "utf-8"))
