from datetime import datetime, timezone
from urllib.parse import urlsplit
from os import name as os_name
import json
import socket
import threading
import time
import ssl
if os_name == "nt":
    SetConsoleTitleW = __import__("ctypes").windll.kernel32.SetConsoleTitleW

ssl_context = ssl.create_default_context()

class ChunkCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()
    
    def add(self, delta):
        with self._lock:
            self._count += delta
        
    def wait(self, interval):
        time.sleep(interval)
        with self._lock:
            count = self._count
            self._count = 0
            return count

def send_webhook(url, **kwargs):
    payload = json.dumps(kwargs, separators=(",", ":"))
    hostname, path = url.split("://", 1)[1].split("/", 1)
    if ":" in hostname:
        hostname, port = hostname.split(":", 1)
        port = int(port)
    else:
        port = 443 if "https" in url else 80
    sock = make_http_socket((hostname, port), ssl_wrap="https" in url)
    try:
        sock.send(
            f"POST /{path} HTTP/1.1\r\n"
            f"Host: {hostname}\r\n"
            f"Content-Length: {len(payload)}\r\n"
            "Content-Type: application/json\r\n"
            "\r\n"
            f"{payload}".encode())
        sock.recv(4096)
    finally:
        shutdown_socket(sock)

def make_embed(group_info):
    return dict(
        title="Found claimable group",
        url=f"https://www.roblox.com/groups/{group_info['id']}",
        fields=[
            dict(name="Group Id", value=group_info["id"]),
            dict(name="Group Name", value=group_info["name"]),
            dict(name="Group Members", value=group_info["memberCount"])
        ],
        footer=dict(
            text="github.com/h0nde/roblox-claimable-group-finder"
        ),
        timestamp=datetime.now(timezone.utc).isoformat()
    )

def make_http_socket(addr, timeout=5, proxy_addr=None, ssl_wrap=True):    
    try:
        sock = None
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect(proxy_addr or addr)

        if proxy_addr:
            sock.send(f"CONNECT {addr[0]}:{addr[1]} HTTP/1.1\r\n\r\n".encode())
            connect_resp = sock.recv(4096)
            if (
                not connect_resp.startswith(b"HTTP/1.1 200")
                and not connect_resp.startswith(b"HTTP/1.0 200")
            ):
                raise ConnectionRefusedError(
                    "Proxy server did not return a correct response for tunnel request")

        if ssl_wrap:
            sock = ssl_context.wrap_socket(
                sock,
                suppress_ragged_eofs=False,
                do_handshake_on_connect=False,
                server_hostname=addr[0])
            sock.do_handshake()
        
        return sock
    
    except:
        if sock:
            shutdown_socket(sock)
        raise

def shutdown_socket(sock):
    if sock:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()

def slice_list(lst, num, total):
    per = int(len(lst)/total)
    chunk = lst[per * num : per * (num + 1)]
    return chunk

def slice_range(r, num, total):
    per = int((r[1]-r[0]+1)/total)
    return (
        r[0] + (num * per),
        r[0] + ((num + 1) * per)
    )

def update_stats(text):
    if os_name == "nt":
        SetConsoleTitleW(text)
    else:
        print(text)
