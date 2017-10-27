# -*- coding: utf-8 -*-
"""Test for functionality of client and server.py."""

import pytest


# def test_message_shorter():
#     """Test for messages shorter than the buffer."""
#     from client import client
#     returned_message = client("short")
#     assert returned_message == "short"


# def test_message_longer():
#     """Test for message longer than the buffer."""
#     from client import client
#     returned_message = client("This is a really long message that we\
#                                 have to type for a test")
#     assert returned_message == "This is a really long message that we\
#                                 have to type for a test"


# def test_message_exactly_one():
#     """Test for message that is exactly one buffer in length."""
#     from client import client
#     returned_message = client("testtest")
#     assert returned_message == "testtest"


# def test_message_unicode():
#     """Test for message containing unicode characters."""
#     from client import client
#     returned_message = client("This is a fancy message, containing\
#                                über-important information")
#     assert returned_message == "This is a fancy message, containing\
#                                über-important information"


def test_response_ok_valid_header():
    """Test to see if response ok returns an HTTP 200 ok response."""
    from server import response_ok
    valid_header = b"HTTP/1.1 200 OK"
    assert response_ok("/webroot/sample.txt") == valid_header


def test_response_ok_end_header():
    """Test to make sure response header has two CLRFs, i.e end of header."""
    from server import response_ok
    end_header = b'\r\n\r\n'
    response = response_ok(b"/webroot/a_web_page.html")
    assert end_header in response


def test_response_error():
    """Test to see if response error returns a correct error message."""
    from server import response_error
    valid_header = b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
    assert response_error(500, "Internal Server Error") == valid_header


def test_response_error_end_header():
    """Test to make sure response header has two CLRFs, i.e end of header."""
    from server import response_error
    end_header = b'\r\n\r\n'
    response = response_error(500, "Internal Server Error")
    assert end_header in response


def test_response_from_server_received():
    """Test that response received from server is valid response."""
    from client import client
    from server import response_ok
    response = client(u"GET webroot/sample.txt HTTP/1.1\r\nHost: "
                      u"www.host1.com\r\n\r\n")
    assert response == response_ok("webroot/sample.txt").decode("utf8")


def test_parse_non_get_request_raises_exception():
    """A request that is not a get request should raise an exception."""
    from server import parse_request
    response = b'POST /path/file.html HTTP/1.1\r\nHost: www.host1.com\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(response)


def test_parse_bad_protocol_raises_exception():
    """A request must use http 1.1 or it will raise an exception."""
    from server import parse_request
    response = b'GET /path/file.html HTTP/1.0\r\nHost: www.host1.com\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(response)


def test_parse_correct_protocol_doesnt_raise_exception():
    """A request must use http 1.1 or it will raise an exception."""
    from server import parse_request
    response = b'GET /path/file.html HTTP/1.1\r\nHost: www.host1.com\r\n\r\n'
    assert parse_request(response) == b'/path/file.html'


def test_parse_bad_host_header():
    """A request must have a proper host header."""
    from server import parse_request
    response = b'GET /path/file.html HTTP/1.1\r\nHost:www.host1.com\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(response)


def test_parse_host_bad_domain():
    """A request must have a proper host header."""
    from server import parse_request
    response = b'GET /path/file.html HTTP/1.1\r\nHost: www.host1.dom\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(response)


def test_parse_host_header_not_valid():
    """A request must have a proper host header."""
    from server import parse_request
    response = b'GET /path/file.html HTTP/1.1\r\nHost: ww.host1.com\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(response)


def test_response_error_returns_valid_response_header():
    """Test that the error_response returns a correctly formed response."""
    from server import response_error
    assert response_error(404, "Not Found") == b"HTTP/1.1 404 Not Found\r\n\r\n"


def test_resolve_uri_returns_content_of_text_file():
    """Should properly return the contents of a text file in a tuple."""
    from server import resolve_uri
    return_val = ("""This is a very simple text file.
Just to show that we can serve it up.
It is three lines long.\n""", "text/plain")
    assert resolve_uri('webroot/sample.txt') == return_val


def test_resolve_uri_content_of_html():
    """Test to see if html file is processed correctly."""
    from server import resolve_uri
    return_val = ("""<!DOCTYPE html>
<html>
<body>

<h1>Code Fellows</h1>

<p>A fine place to learn Python web programming!</p>

</body>
</html>

""", "text/html")
    assert resolve_uri('webroot/a_web_page.html') == return_val


def test_resolve_uri_python_file():
    """Resolve should return the contents of a python file."""
    from server import resolve_uri
    return_val = ("""#!/usr/bin/env python

\"\"\"
make_time.py

simple script that returns and HTML page with the current time
\"\"\"

import datetime

time_str = datetime.datetime.now().isoformat()

html = \"\"\"
<http>
<body>
<h2> The time is: </h2>
<p> %s <p>
</body>
</http>
\"\"\" % time_str

print(html)
""", 'text/x-python')
    assert resolve_uri('webroot/make_time.py') == return_val


def test_resolve_uri_image():
    """Should return contents of the image and type."""
    from server import resolve_uri
    return_val = (b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\xb0\x00\x00\x04\xb0\x08\x06\x00\x00\x00\xeb!\xb3\xcf\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\x0b\x12\x00\x00\x0b\x12\x01\xd2\xdd~\xfc\x00\x00\x00\x15tEXtCreation Time\x003/28/09\xee/\xfb\xfc\x00\x00\x00\x1ctEXtSoftware\x00Adobe Fireworks CS3\x98\xd6F\x03\x00\x00 \x00IDATx\x9c\xec\xda1n\xc3@\x10\x04A\x9e\xc1\xff\x7fy\x1d:s$z\xdbR\xd5\x0b&\xe1\x81h\xec\x99\xeb\x9a\x0b\x00\x80\x979\xfe\xae\x00\x00^\xeak{\x00\x00\x00\x00\x00\xfcF\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 \xed\xde\x1e\x00<\xefl\x0f\x00\xf84\x1e^\x80\xbf5\xdb\x03\x80\xa7\xb9\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 \xed\xde\x1e\x00P33\xdb\x13\x00\x80\x0fw\xce\xd9\x9e\x00\x90\xe2\x02\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x80\xb4{{\x00\xc0G:g{\x01\xf0\xa03\xdb\x0b\x80'\xcd\xe5#\x07\xf8k.\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H\xbb\xb7\x07\x00\x00\xbc\x9d3\xdb\x0b\x80'\xf9\xc4{\xbc\xbb\xf0\xf6\\`\x01\x00\x00\x00\x90&`\x01\x00\x00\x00\x90v_3g{\x04\xf0\xe3\x9cG>I7\xd51\xe7\xba\xbc\xbd\xf0\xde\xbc\xbb\x00\x00/\xe4\x02\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x804\x01\x0b\x00\x00\x00\x80\xb4{{\x00\xc0'\x9a\x99\xd9\xde\x00\x00\x00\xf0_\xb8\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x02\x00\x00\x00 M\xc0\x82\xefv\xed\x18\x85a \x08\x82 \x07\xfa\xff\x97\xd7\xa9\x1d8\x12x\x1b\xb9\xea\x05\x137\x03\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4\tX\x00\x00\x00\x00\xa4]\xdb\x03\x00j\xce9\xdb\x13\x00\x00\x00x\xe3\x81\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\x9a\x80\x05\x00\x00\x00@\xda\xb5=\x00\xf8\x89\xb3=\x00\xe0\xbf\xccl/\x00\x00x\x12\x0f,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\xae\xed\x01\xc0\xa7\x99\xd9\x9e\x00\xc0M\xe7l/\x00\x00x\x16\x0f,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\xbd\xde\x00\x13\x00\x00\x01\x85IDAT\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\x04,\x00\x00\x00\x00\xd2\xce\xcclo\x00\x00\x00\x00\x80\xaf<\xb0\x00\x00\x00\x00H\x13\xb0\x00\x00\x00\x00H{\x010m&k\x81\xac\xde\x1e\x00\x00\x00\x00IEND\xaeB`\x82", 'image/png')
    assert resolve_uri('webroot/images/sample_1.png') == return_val


def test_resolve_raises_error_bad_path():
    """Should raise value error when given a non existent path."""
    from server import resolve_uri
    with pytest.raises(ValueError):
        resolve_uri('webrot/make_time.py')


def test_resolve_uri_returns_html_for_directory():
    """Should return an html listing of contents when passed directory."""
    from server import resolve_uri
    file1 = 'sample.txt'
    file2 = 'a_web_page.html'
    assert file1 in resolve_uri(b'webroot')[0]
    assert file2 in resolve_uri(b'webroot')[0]


def test_response_ok_contains_message_body():
    """Test that ok_response also contains valid response body."""
    from server import response_ok
    return_val = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 95\r\n\r\nThis is a very simple text file.\nJust to show that we can serve it up.\nIt is three lines long.\n"
    assert response_ok('webroot/sample.txt') == return_val
