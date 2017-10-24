# -*- coding: utf-8 -*-
"""Test for functionality of client and server.py."""

from __future__ import unicode_literals


def test_message_shorter():
    """Test for messages shorter than the buffer."""
    from client import client
    returned_message = client("short")
    assert returned_message == "short"


def test_message_longer():
    """Test for message longer than the buffer."""
    from client import client
    returned_message = client("This is a really long message that we\
                                have to type for a test")
    assert returned_message == "This is a really long message that we\
                                have to type for a test"


def test_message_exactly_one():
    """Test for message that is exactly one buffer in length."""
    from client import client
    returned_message = client("testtest")
    assert returned_message == "testtest"


def test_message_unicode():
    """Test for message containing unicode characters."""
    from client import client
    returned_message = client("This is a fancy message, containing\
                               über-important information")
    assert returned_message == "This is a fancy message, containing\
                               über-important information"


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
    assert response_error() == """HTTP/1.1 500 Internal Server Error\r\nContent-Type:
     text/plain\r\n\r\nthis is a response"""
