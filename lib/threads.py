from .constants import GROUP_API, GROUP_API_ADDR, BATCH_GROUP_REQUEST,\
    SINGLE_GROUP_REQUEST
from .utils import parse_batch_response, make_http_socket, shutdown_socket,\
    update_stats, send_webhook, make_embed
from datetime import datetime, timezone
from time import time, sleep, perf_counter
from json import loads as json_loads
from zlib import decompress

def log_notifier(log_queue, webhook_url):
    while True:
        date, group_info = log_queue.get()

        print(f"[{date.strftime('%H:%M:%S')}]",
              f"roblox.com/groups/{group_info['id']:08d}",
              "|",
              f"{str(group_info['memberCount']).rjust(2)} member(s)",
              "|",
              group_info["name"])
            
        if webhook_url:
            try:
                send_webhook(
                    webhook_url, embeds=(make_embed(group_info, date),))
            except Exception as err:
                print(f"Error while sending webhook: {err!r}")

def stat_updater(count_queue):
    count_cache = {}

    while True:
        sleep(0.1)

        while True:
            try:
                for ts, count in count_queue.get(block=False):
                    ts = int(ts)
                    count_cache[ts] = count_cache.get(ts, 0) + count
            except:
                break
            
        now = time()
        total_count = 0

        for ts, count in tuple(count_cache.items()):
            if now - ts > 60:
                count_cache.pop(ts)
                continue
            total_count += count
        
        update_stats(f"Speed: {total_count:,}")

def group_scanner(log_queue, count_queue, proxy_iter, timeout, webhook_url,
                  gid_ranges, gid_cutoff, gid_chunk_size):
    gid_tracked = set()
    gid_list = [
        str(gid).encode()
        for gid_range in gid_ranges
        for gid in range(*gid_range)
    ]
    gid_list_len = len(gid_list)
    gid_list_idx = 0

    if gid_cutoff:
        gid_cutoff = str(gid_cutoff).encode()

    while gid_list_len >= gid_chunk_size:
        proxy_addr = next(proxy_iter) if proxy_iter else None
        try:
            sock = make_http_socket(GROUP_API_ADDR, timeout, proxy_addr, hostname=GROUP_API)
        except:
            continue
        
        while True:
            gid_chunk = [
                gid_list[(gid_list_idx + n) % gid_list_len]
                for n in range(1, gid_chunk_size + 1)
            ]
            gid_list_idx += gid_chunk_size

            try:
                # Request batch group details.
                sock.sendall(BATCH_GROUP_REQUEST % b",".join(gid_chunk))
                resp = sock.recv(1048576)
                if not resp.startswith(b"HTTP/1.1 200 OK"):
                    break
                resp = resp.partition(b"\r\n\r\n")[2]
                while resp[-1] != 0:
                    resp += sock.recv(1048576)
                owner_status = parse_batch_response(decompress(resp, -15), gid_chunk_size)

                for gid in gid_chunk:
                    if gid not in owner_status:
                        # Group is missing from the batch response.
                        if not gid_cutoff or gid_cutoff > gid:
                            # Group is outside of cut-off range.
                            # Assume it doesn't exist and ignore it in the future.
                            gid_list.remove(gid)
                            gid_list_len -= 1
                        continue
                    
                    if gid not in gid_tracked:
                        if owner_status[gid]:
                            # Group has an owner and this is the first time it's been checked.
                            # Mark it as tracked.
                            gid_tracked.add(gid)
                        else:
                            # Group doesn't have an owner, and this is only the first time it's been checked.
                            # Assume that it's locked or manual-approval only, and ignore it in the future.
                            gid_list.remove(gid)
                            gid_list_len -= 1
                        continue

                    if owner_status[gid]:
                        # Group has an owner and it's been checked previously.
                        # Skip to next group in the batch.
                        continue

                    # Group is marked as tracked and doesn't have an owner.
                    # Request extra details and determine if it's claimable.
                    sock.sendall(SINGLE_GROUP_REQUEST % gid)
                    resp = sock.recv(1048576)
                    if not resp.startswith(b"HTTP/1.1 200 OK"):
                        break
                    group_info = json_loads(resp.partition(b"\r\n\r\n")[2])

                    if (
                        not group_info["publicEntryAllowed"]
                        or group_info["owner"]
                        or "isLocked" in group_info
                    ):
                        # Group cannot be claimed, ignore it in the future.
                        gid_list.remove(gid)
                        gid_list_len -= 1
                        continue
                    
                    # Send group info back to main process.
                    log_queue.put((datetime.now(timezone.utc), group_info))
                    
                    # Ignore group in the future.
                    gid_list.remove(gid)
                    gid_list_len -= 1

                # Let the counter know gid_chunk_size groups were checked.
                count_queue.put((time(), gid_chunk_size))

            except KeyboardInterrupt:
                exit()
            
            except Exception as err:
                break
            
        shutdown_socket(sock)
