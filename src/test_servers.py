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
