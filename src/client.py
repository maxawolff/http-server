"""."""

import socket


def client(message, buffer=8):
    """."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))

    buffer_length = buffer
    reply_complete = False
    reply_string = ""
    while not reply_complete:
        part = client.recv(buffer_length)
        reply_string += part.decode("utf8")
        if len(part) < buffer_length:
            break
    client.close()
    print(reply_string)


if __name__ == '__main__':
    import sys
    client(sys.argv[1])
