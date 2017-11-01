"""Module to create a simple server using gevent."""

from __future__ import unicode_literals
import io
import mimetypes
import os
import sys


def http_server(socket, address):
    """Handle incoming connections and send appropriate response."""
    buffer_length = 8
    request = b''
    message_complete = False
    while not message_complete:
        try:
            part = socket.recv(buffer_length)
            request += part
            if b"%@#" in request:
                message_complete = True
                sys.stdout.write(request.decode("utf8").replace("%@#", ""))
                reply = b""
                try:
                    uri = parse_request(request)
                    reply = response_ok(uri)
                except ValueError:
                    socket.sendall(response_error(400, "Bad Request"))
                except IOError as error:
                    socket.sendall(response_error(404, error))
                reply += b"%@#"
                try:
                    socket.sendall(reply)
                except:
                    pass
                break
        except KeyboardInterrupt:
            print("\nClosing server")
            socket.close()
            server.close()
            sys.exit()


def response_ok(uri):
    """Return a 200 ok response."""
    response_header = b"HTTP/1.1 200 OK\r\n"
    resolved_uri_contents = resolve_uri(uri)
    response_type_header = "Content-Type: " + resolved_uri_contents[1] + "\r\n"
    response_header += response_type_header.encode('utf8')
    response_len = len(resolved_uri_contents[0])
    response_len_header = "Content-Length: " + str(response_len) + "\r\n"
    response_header += response_len_header.encode('utf8')
    if "image" in resolved_uri_contents[1]:
        resolved_uri_contents[0].decode("utf8")
    full_response = response_header + b"\r\n" + resolved_uri_contents[0]\
        .encode('utf8')
    return full_response


def response_error(error_code, reason_phrase):
    """Return a well-formed HTTP error response."""
    response = b"HTTP/1.1 "
    response += str(error_code).encode('utf8') + b" " + reason_phrase\
        .encode('utf8') + b"\r\n\r\n"
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
    if address.split('.')[0] != 'www' or address.split('.')[2] != 'com':
        raise ValueError("Invalid domain in host header")
    return list_of_headers[1].encode('utf8')


def resolve_uri(uri):
    """Return a response body with the content and the type of file."""
    if os.path.exists(uri):
        if (os.path.isdir(uri)):
            list_of_files = os.listdir(uri)
            directory_contents = ""
            for file in list_of_files:
                directory_contents += "<li>" + file + "</li>\n"
            html_response = """<!DOCTYPE html>
<html>
<body>
<ul>
%s</ul>
</body>
</html>""" % directory_contents
            return (html_response, "text/html")
        type_of_file = mimetypes.guess_type(uri.decode('utf8'))[0]
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
        raise IOError("No file or directory of the given name")


if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 5000), http_server)
    print('Starting HTTP server on port 5000')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
