import json
import logging
import mimetypes
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# from datetime import datetime


BASE_DIR = Path()


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # отримання даних у застосунок з форми
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        # повертаємо дані до початкового вигляду
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        try:
            # перетворюємо рядок на словник
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
            print(data_dict)
            with open('storage/data.json', 'w', encoding='utf-8') as file:
                json.dump(data_dict, file, ensure_ascii=False, indent=4)
        except ValueError as err:
            logging.error(err)
        except OSError as err:
            logging.error(err)
        # редірект
        self.send_response(302)
        self.send_header('Location', '/message')
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        match pr_url.path:
            case "/":
                self.send_html_file("index.html")
            case "/message":
                self.send_html_file("message.html")
            case _:
                file = BASE_DIR.joinpath(pr_url.path[1:])
                if file.exists():
                    self.send_static()
                else:
                    self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(f".{self.path}", 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('localhost', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
