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
    address = ('127.0.0.1', 5002)
    server.bind(address)
    server.listen(1)
    while True:
        try:
            conn, addr = server.accept()
            request = ''
            if conn:
                buffer_length = 8
                message_complete = False
                while not message_complete:
                    part = conn.recv(buffer_length)
                    request += part.decode('utf8')
                    if len(part) < buffer_length:
                        break
                if request[-1] == ' ':
                    request = request[0:len(request) - 1]
                sys.stdout.write(request)
                reply = response_ok()
                if len(reply) % 8 == 0:
                    reply += " "
                conn.sendall(reply.encode('utf8'))
                conn.close()
        except KeyboardInterrupt:
            server.close()
            sys.exit()


def response_ok():
    """Return a 200 ok response."""
    header = """HTTP/1.1 200 OK\r\nContent-Type:
     text/plain\r\n\r\nthis is a response"""
    return header


def response_error():
    """Return a 500 interernal server error message."""
    header = """HTTP/1.1 500 Internal Server Error\r\nContent-Type:
     text/plain\r\n\r\nthis is a response"""
    return header


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
    if not address.split('.')[0] == 'www' or not address.split('.')[2] == 'com':
        raise ValueError("Invalid domain in host header")
    return list_of_headers[1]


if __name__ == '__main__':
    server()
