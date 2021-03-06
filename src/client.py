# -*- coding: utf-8 -*-
"""Module to create a client server."""

import socket
import sys


def client(message, buffer=8):
    """Send a message to a server and returns the response string."""
    infos = socket.getaddrinfo('127.0.0.1', 5009)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    message += "%@#!"
    if sys.version_info.major == 3:
        message = message.encode('utf8')
    client.sendall(message)
    buffer_length = buffer
    reply_complete = False
    reply_string = b""
    while not reply_complete:
        part = client.recv(buffer_length)
        reply_string += part
        if b"%@#!" in reply_string:
            break
    client.close()
    reply_string = reply_string.decode("utf8")
    reply_string = reply_string[:reply_string.index(u"%@#!")]
    return reply_string


if __name__ == '__main__':
    client(sys.argv[1])
