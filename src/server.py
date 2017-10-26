# -*- coding: utf-8 -*-
"""Module to create an echo server."""

from __future__ import unicode_literals
import socket
import sys


def server():
    """Accept client connection and sends response back to client."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5003)
    server.bind(address)
    server.listen(1)
    while True:
        try:
            conn, addr = server.accept()
            request = b''
            if conn:
                buffer_length = 8
                message_complete = False
                while not message_complete:
                    part = conn.recv(buffer_length)
                    request += part
                    if b"%@#!" in request:
                        break
                sys.stdout.write(request.decode("utf8").replace("%@#!", ""))
                reply = b""
                try:
                    reply = parse_request(request)
                    reply = response_ok(reply)
                except ValueError:
                    reply = response_error(400, "Bad Request")
                reply += b"%@#!"
                conn.sendall(reply)
                conn.close()
        except KeyboardInterrupt:
            server.close()
            sys.exit()


def response_ok(uri):
    """Return a 200 ok response."""
    return b"HTTP/1.1 200 OK\r\n\r\n" + uri


def response_error(error_code, reason_phrase):
    """Return a well-formed HTTP error response."""
    response = "HTTP/1.1 "
    response += str(error_code) + " " + reason_phrase + "\r\n\r\n"
    return response


def parse_request(request):
    """Return the URI of the request if it is a valid get request."""
    request = request.decode('utf8')
    header = request[:request.index('\r\n')]
    list_of_headers = header.split()
    if list_of_headers[0] != 'GET':
        raise ValueError("Request method must be GET")
    if list_of_headers[2] != 'HTTP/1.1':
        raise ValueError("Request protocol must use HTTP/1.1")
    host = request.split("\r\n")[1]
    if not host.startswith("Host: "):
        raise ValueError("Request must include the Host header")
    address = host.split()[1]
    if not address.split('.')[0] == 'www' or not address.split('.')[2] \
            == 'com':
        raise ValueError("Invalid domain in host header")
    return list_of_headers[1].encode('utf8')


def resolve_uri(uri):
    """Return a response body with the content and the type of file."""
    import mimetypes
    import io
    import os
    if os.path.exists(uri):
        type_of_file = mimetypes.guess_type(uri)[0]
        if type_of_file.startswith('image'):
            file = io.open(uri, 'rb')
            file_content = file.read()
            file.close()
            return (file_content, type_of_file)
        else:
            file = io.open(uri)
            file_content = file.read()
            file.close()
            return (file_content, type_of_file)
    else:
        raise ValueError("No file or directory of the given name")


if __name__ == '__main__':
    server()
