from datetime import datetime, timezone
from json import dumps as json_dumps
from socket import socket
from os import name as os_name
from time import sleep

if os_name == "nt":
    set_title = __import__("ctypes").windll.kernel32.SetConsoleTitleW

ssl_context = __import__("ssl").create_default_context()

class ChunkCounter:
    def __init__(self):
        self._count = 0
        self._lock = __import__("threading").Lock()
    
    def add(self, delta):
        with self._lock:
            self._count += delta
        
    def wait(self, interval):
        sleep(interval)
        with self._lock:
            count = self._count
            self._count = 0
            return count

def parse_batch_response(data, limit):
    index = 10
    status = {}
    for _ in range(limit):
        id_index = data.find(b'"id":', index)
        if id_index == -1:
            break
        index = data.find(b',', id_index + 5)
        group_id = data[id_index + 5 : index]
        index = data.find(b'"owner":', index) + 8
        status[group_id] = (data[index] == 123)
        index += 25
    return status

def send_webhook(url, **kwargs):
    payload = json_dumps(kwargs, separators=(",", ":"))
    hostname, path = url.split("://", 1)[1].split("/", 1)
    if ":" in hostname:
        hostname, port = hostname.split(":", 1)
        port = int(port)
    else:
        port = 443 if url.startswith("https") else 80
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
            dict(name="Group ID", value=group_info["id"]),
            dict(name="Group Name", value=group_info["name"]),
            dict(name="Group Members", value=group_info["memberCount"])
        ],
        footer=dict(
            text="github.com/h0nde/roblox-claimable-group-finder"
        ),
        timestamp=datetime.now(timezone.utc).isoformat()
    )

def make_http_socket(addr, timeout=5, proxy_addr=None, ssl_wrap=True, hostname=None):    
    sock = socket()
    sock.settimeout(timeout)
    sock.connect(proxy_addr or addr)
    
    try:
        if proxy_addr:
            sock.send(f"CONNECT {addr[0]}:{addr[1]} HTTP/1.1\r\n\r\n".encode())
            connect_resp = sock.recv(4096)
            if not (
                connect_resp.startswith(b"HTTP/1.1 200")
                or connect_resp.startswith(b"HTTP/1.0 200")
            ):
                raise ConnectionRefusedError

        if ssl_wrap:
            sock = ssl_context.wrap_socket(
                sock,
                suppress_ragged_eofs=False,
                do_handshake_on_connect=False,
                server_hostname=hostname or addr[0])
            sock.do_handshake()

    except:
        shutdown_socket(sock)
        raise

    return sock

def shutdown_socket(sock):
    try:
        sock.shutdown(2)
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
        set_title(text)
    else:
        print(text)
