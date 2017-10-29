# http-server


This module defines a server that accepts requests from a client server and logs the request to stdout. Once the request is fully received from the client, the server then returns an echo of what it was sent to the client.


### Getting Started

Start the server in a terminal window
```
python server.py
```

From another terminal, send requests from the client
```
python client(your_request_here)
```

### Testing

Install the required packages
```
pip install -e .[test]
```

Run tox for Python 2.7 & 3.6 compatability
```
tox
```