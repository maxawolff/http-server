"""."""

import socket
import sys


def server():
    """."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5001)
    server.bind(address)
    server.listen(1)
    while True:
        try:
            conn, addr = server.accept()
            message = ''
            if conn:
                buffer_length = 8
                message_complete = False
                # last_message = ""
                while not message_complete:
                    part = conn.recv(buffer_length)
                    message += part.decode('utf8')
                    if len(part) < buffer_length or len(part) == 0:
                        break
                    # last_message += part.decode('utf8')
                conn.sendall(message.encode('utf8'))
                conn.close()
        except KeyboardInterrupt:
            server.close()
            sys.exit()


if __name__ == '__main__':
    server()
