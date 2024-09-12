import argparse
import random
from http.server import HTTPServer, BaseHTTPRequestHandler


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def _message(self):
        with open("index.html", "rb") as file:
            return file.read()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._message())

    def do_HEAD(self):
        self._set_headers()


def run(server_class=HTTPServer, handler_class=S, addr='localhost', port=3000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f'Starting httpd server on {addr}:{port}')
    httpd.serve_forever()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run a simple HTTP server')
    parser.add_argument(
        '-l',
        '--listen',
        default='localhost',
        help='Specify the IP address on which the server listens',
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=3000,
        help='Specify the port on which the server listens',
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
