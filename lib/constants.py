DEFAULT_ID_SLACK = 100000
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