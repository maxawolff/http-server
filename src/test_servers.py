"""Test for functionality of client and server.py."""


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
