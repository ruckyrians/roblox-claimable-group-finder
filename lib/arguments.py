from multiprocessing import cpu_count
import argparse

def parse_human_number(s):
    if s[-1] == "m":
        s = int(float(s[:-1]) * 1000000)
    else:
        s = int(s)
    return s

def parse_range(range_string):
    fields = tuple(map(parse_human_number, range_string.split("-", 1)))
    return fields

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers", type=int, default=cpu_count(), help="Number of workers")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Number of threads (per worker)")
    parser.add_argument("-r", "--range", type=parse_range, required=True, nargs="+", help="Range(s) of group IDs")
    parser.add_argument("-c", "--cut-off", type=parse_human_number, help="ID limit for skipping missing groups")
    parser.add_argument("-p", "--proxy-file", type=argparse.FileType("r", encoding="UTF-8", errors="ignore"), help="File containing HTTP proxies")
    parser.add_argument("-u", "--webhook-url", type=str, help="Send group results to <url>")
    parser.add_argument("-C", "--chunk-size", type=int, default=100, help="Number of groups to be sent per batch request")
    parser.add_argument("-T", "--timeout", type=float, default=5.0, help="Timeout for connections and responses")
    arguments = parser.parse_args()
    return arguments