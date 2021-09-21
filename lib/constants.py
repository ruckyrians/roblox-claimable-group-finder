GROUP_API = "groups.roblox.com"
GROUP_API_ADDR = (__import__("socket").gethostbyname(GROUP_API), 443)
BATCH_GROUP_REQUEST = (
    b"GET /v2/groups?groupIds=%b HTTP/1.1\n"
    b"Host:groups.roblox.com\n"
    b"Accept-Encoding:deflate\n"
    b"\n")
SINGLE_GROUP_REQUEST = (
    b"GET /v1/groups/%b HTTP/1.1\n"
    b"Host:groups.roblox.com\n"
    b"\n")

DEFAULT_ID_SLACK = 100000
DEFAULT_RANGES = (
    (1, 1250000),
    (2520000, 7960000),
    (8000000, 9930000),
    (9960000, 10760000),
    (10790000, 12340000)
)