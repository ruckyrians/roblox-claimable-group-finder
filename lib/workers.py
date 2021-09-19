from .threads import thread_func
from .utils import ChunkCounter, slice_range
from threading import Thread
from time import time

def worker_func(thread_count, count_queue,
                proxy_list, gid_ranges, **thread_kwargs):    
    check_counter = ChunkCounter()
    proxy_iter = __import__("itertools").cycle(proxy_list) \
                 if proxy_list else None
    threads = []

    for num in range(thread_count):
        thread = Thread(
            target=thread_func,
            name=f"Scanner-{num}",
            daemon=True,
            kwargs=dict(
                check_counter=check_counter,
                proxy_iter=proxy_iter,
                gid_ranges=[
                    slice_range(gid_range, num, thread_count)
                    for gid_range in gid_ranges
                ],
                **thread_kwargs
            )
        )
        threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    try:
        while any(t.is_alive() for t in threads):
            count_queue.put((time(), check_counter.wait(1)))
    except KeyboardInterrupt:
        pass