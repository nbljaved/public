class ApplicationRequestHandler:
    def do_GET(self):
        try:
            url_path = self.path.lstrip("/")
            full_path = Path.cwd().joinpath(url_path)
            if not full_path.exists():
                raise ServerException(f"'{self.path}' not found")
            elif full_path.is_file():
                self.handle_file(self.path, full_path)
            else:
                raise ServerException(f"Unknown object '{self.path}'")
        except Exception as msg:
            self.handle_error(msg)

    # ...etc...

if __name__ == '__main__':
    class RequestHandler(
            BaseHTTPRequestHandler,
            ApplicationRequestHandler
    ):
        pass

    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
