# roblox-claimable-group-finder
<p align="center">Tool for finding claimable groups on Roblox.</p>

<p align="center"><img src="https://i.imgur.com/131wdCq.png" height="300" width="637"></p>

# Features
- High-performance scanning (up to 50M+ checks-per-minute)
- Zero dependencies
- Automatic ID calibration on start
- Webhook and HTTP proxy support

# Usage
```bash
python finder.py --workers 16 --proxy-file proxies.txt
```

```
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

# Things to note
- Ownerless groups will be ignored on the first cycle of scanning (regardless of approval-only or locked status).
- Proxies are required as of 2021-09.

# --webhook-url
If the `--webhook-url` arg. is specified, an embed will be sent whenever a claimable group is found. E.g.:

<img src="https://i.imgur.com/VeMBoCA.png" alt="Embed sample" width="400"/>

# --cut-off
By default, when encountering a missing/deleted group, it's ID will be removed from the queue so that it won't be checked again.

The `--cut-off` argument specifies at which ID (and above) missing groups shouldn't be removed from the queue. This is ideal in scenarios where you also wanna scan groups that haven't been created yet.
