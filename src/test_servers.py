# -*- coding: utf-8 -*-
"""Test for functionality of client and server.py."""

from __future__ import unicode_literals
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
    valid_header = "HTTP/1.1 200 OK"
    assert response_ok()[0:15] == valid_header


def test_response_ok_end_header():
    """Test to make sure response header has two CLRFs, i.e end of header."""
    from server import response_ok
    end_header = '\r\n\r\n'
    response = response_ok()
    assert end_header in response


def test_response_error():
    """Test to see if response error returns a correct error message."""
    from server import response_error
    valid_header = "HTTP/1.1 500 Internal Server Error"
    assert response_error()[0:34] == valid_header


def test_response_error_end_header():
    """Test to make sure response header has two CLRFs, i.e end of header."""
    from server import response_error
    end_header = '\r\n\r\n'
    response = response_error()
    assert end_header in response


def test_response_from_server_received():
    """Test that response received from server is valid response."""
    from client import client
    from server import response_ok
    received_response = client("testtest")
    assert received_response == response_ok()


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
    assert parse_request(response) == '/path/file.html'


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


# def test_parse_request_good_request():
#     """Test to make sure a good request returns the proper URI."""
#     from server import parse_request
#     response =
#     assert parse_request(response) == URI
