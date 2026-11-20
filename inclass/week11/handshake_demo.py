# handshake_demo.py -- Week 11, Part 2: the HTTP request that becomes a WebSocket.
# Needs app.py running on port 5102. Uses a raw socket so we can see every byte.
import base64
import hashlib
import os
import socket

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"       # a constant from the WebSocket standard (RFC 6455)
key = base64.b64encode(os.urandom(16)).decode()

request = (
    "GET /socket.io/?EIO=4&transport=websocket HTTP/1.1\r\n"
    "Host: localhost:5102\r\n"
    "Upgrade: websocket\r\n"
    "Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {key}\r\n"
    "Sec-WebSocket-Version: 13\r\n"
    "\r\n"
)
print("--- we send ---")
print(request)

s = socket.create_connection(("localhost", 5102))
s.sendall(request.encode())
reply = s.recv(4096).decode(errors="replace")
s.close()
head = reply.split("\r\n\r\n")[0]
print("--- the server answers ---")
print(head)

expected = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()
print()
print("Sec-WebSocket-Accept we compute ourselves:", expected)
print("status code is 101 (Switching Protocols):", head.startswith("HTTP/1.1 101"))
print("accept header matches our computation:   ", expected in head)
