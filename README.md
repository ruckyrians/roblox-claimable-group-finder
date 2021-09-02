# roblox-unclaimed-group-finder
Python 3 tool for finding unclaimed groups on Roblox. Supports multi-threading, multi-processing and HTTP proxies.

This tool is able to achieve checks in the tens-of-millions per minute due to it's use of a batch API endpoint.

# Usage
```bash
python scanner.py --workers 16 --range 1-1.25m 2.5m-12m --cut-off 11.5m --webhook-url WEBHOOKURL
```

```
  -t THREADS, --threads THREADS
                        amount of threads per worker
  -w WORKERS, --workers WORKERS
                        amount of workers (processes)
  -r RANGE [RANGE ...], --range RANGE [RANGE ...]
                        range of group ids to be scanned
  -c CUT_OFF, --cut-off CUT_OFF
                        group ids past this point won't be blacklisted based on their current validity status
  -p PROXY_FILE, --proxy-file PROXY_FILE
                        list of HTTP proxies, separated by newline
  -u WEBHOOK_URL, --webhook-url WEBHOOK_URL
                        found groups will be posted to this url
  --get-funds GET_FUNDS
                        attempt to obtain amount of funds in a group
  --chunk-size CHUNK_SIZE
                        amount of groups to be sent per API request
  --timeout TIMEOUT     timeout for server connections and responses
```
