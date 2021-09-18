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
    parser.add_argument(
        "-w", "--workers",
        default=cpu_count(),
        type=int,
        help="Number of workers",
        metavar="<num>")
    parser.add_argument(
        "-t", "--threads",
        default=50,
        type=int,
        help="Number of threads (per worker)",
        metavar="<num>")
    parser.add_argument(
        "-r", "--range",
        nargs="+",
        type=parse_range,
        help="Range(s) of group IDs",
        metavar="<range>")
    parser.add_argument(
        "-p", "--proxy-file",
        type=argparse.FileType("r", encoding="UTF-8", errors="ignore"),
        help="File containing HTTP proxies", 
        metavar="<file>")
    parser.add_argument(
        "-u", "--webhook-url",
        type=str,
        help="Send group results to <url>",
        metavar="<url>")
    parser.add_argument(
        "-c", "--cut-off",
        type=parse_human_number,
        help="ID limit for skipping missing groups",
        metavar="<id>")
    parser.add_argument(
        "-C", "--chunk-size",
        default=100, 
        type=int,
        help="Number of groups to be sent per batch request",
        metavar="<size>")
    parser.add_argument(
        "-T", "--timeout",
        default=5.0,
        type=float,
        help="Timeout for connections and responses",
        metavar="<seconds>")
    arguments = parser.parse_args()
    return arguments