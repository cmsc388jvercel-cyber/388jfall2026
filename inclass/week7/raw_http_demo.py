# raw_http_demo.py -- Week 7, Part 1: what HTTP actually looks like on the wire.
# Start the app first (flask run), then run this in a second terminal.
import socket

HOST, PORT = "localhost", 5007


def send_raw(request_text):
    """Open a TCP connection, send the text exactly as typed, print whatever comes back."""
    with socket.create_connection((HOST, PORT)) as sock:
        sock.sendall(request_text.encode())
        reply = b""
        while chunk := sock.recv(4096):
            reply += chunk
    print(reply.decode())


# 1. A GET request is just lines of text. Note the blank line that ends the headers.
print("===== GET /parts/00345 =====")
send_raw(
    "GET /parts/00345 HTTP/1.1\r\n"
    f"Host: {HOST}:{PORT}\r\n"
    "Accept: application/json\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# 2. Same URL, different Accept header: the server sends a different representation.
print("===== GET /parts/00345 (asking for XML) =====")
send_raw(
    "GET /parts/00345 HTTP/1.1\r\n"
    f"Host: {HOST}:{PORT}\r\n"
    "Accept: application/xml\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# 3. A URL that does not exist: the status line changes, the shape of the reply does not.
print("===== GET /parts/99999 =====")
send_raw(
    "GET /parts/99999 HTTP/1.1\r\n"
    f"Host: {HOST}:{PORT}\r\n"
    "Connection: close\r\n"
    "\r\n"
)
