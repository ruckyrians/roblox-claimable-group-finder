# roblox-claimable-group-finder
Python 3 tool for finding claimable groups on Roblox.

# Usage
```bash
python finder.py --workers 16 --cut-off 11.5m --range 1-1.25m 2.5m-12m --proxy-file proxies.txt
```

```
-h, --help            show this help message and exit
-w <num>, --workers <num>
                      Number of workers
-t <num>, --threads <num>
                      Number of threads (per worker)
-r <range> [<range> ...], --range <range> [<range> ...]
                      Range(s) of group IDs
-p <file>, --proxy-file <file>
                      File containing HTTP proxies
-u <url>, --webhook-url <url>
                      Send group results to <url>
-c <id>, --cut-off <id>
                      ID limit for skipping missing groups
-C <size>, --chunk-size <size>
                      Number of groups to be sent per batch request
-T <seconds>, --timeout <seconds>
                      Timeout for connections and responses
```
