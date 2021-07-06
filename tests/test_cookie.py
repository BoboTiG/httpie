from socket import socket
import multiprocessing

from flask import Flask, make_response

from .utils import http

app = Flask(__name__)


@app.route('/')
def main():
    response = make_response()
    response.set_cookie('hello', value='world')
    response.set_cookie('oatmeal_raisin', value='is the best')
    return response


def available_port():
    conn = socket()
    conn.bind(('', 0))
    port = conn.getsockname()[1]
    conn.close()
    return port


def test_cookie_parser():
    # Fix for macOS (https://github.com/pytest-dev/pytest-flask/issues/104)
    multiprocessing.set_start_method('fork')

    port = available_port()
    server = multiprocessing.Process(target=app.run, kwargs={'port': port})
    server.start()
    try:
        response = http(f'http://localhost:{port}/')
        assert 'Set-Cookie: hello=world; Path=/' in response
        assert 'Set-Cookie: oatmeal_raisin="is the best"; Path=/' in response
    finally:
        server.terminate()
        server.join()
