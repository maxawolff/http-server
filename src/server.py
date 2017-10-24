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
            message = ''
            if conn:
                buffer_length = 8
                message_complete = False
                while not message_complete:
                    part = conn.recv(buffer_length)
                    message += part.decode('utf8')
                    if len(part) < buffer_length or not len(part):
                        break
                conn.sendall(message.encode('utf8'))
                conn.close()
        except KeyboardInterrupt:
            server.close()
            sys.exit()


if __name__ == '__main__':
    server()
