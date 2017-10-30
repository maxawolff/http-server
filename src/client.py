# -*- coding: utf-8 -*-
"""Module to create a client server."""

from __future__ import unicode_literals
import socket
import sys
import codecs


def client(message, buffer=8):
    """Send a message to a server and returns the response string."""
    # infos = socket.getaddrinfo('127.0.0.1', 5004)
    # stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    # client = socket.socket(*stream_info[:3])
    # client.connect(stream_info[-1])
    client = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    client.connect(('127.0.0.1', 5000))
    message += "%@#"
    message = codecs.escape_decode(message)[0]
    # if sys.version_info.major == 3:
    #     message = message.encode('utf8')
    client.sendall(message)
    buffer_length = buffer
    reply_complete = False
    reply_string = b""
    while not reply_complete:
        part = client.recv(buffer_length)
        reply_string += part
        if b"%@#" in reply_string:
            break
    client.close()
    reply_string = reply_string.decode("utf8")
    reply_string = reply_string[:reply_string.index(u"%@#")]
    print(reply_string)
    return reply_string


if __name__ == '__main__':
    client(sys.argv[1])
