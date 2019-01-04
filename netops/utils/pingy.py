from concurrent.futures import ThreadPoolExecutor
from subprocess import getstatusoutput as get_status

import time


def check_status(ip_address, packets=1):
    status, result = get_status(f"ping -c{packets} -i0.2 -w1 {ip_address}")

    if status is 0:
        ip_status = [ip_address, True ]
        print(ip_status)
    else:
        return
#        ip_status = [ip_address, False]

    return ip_status

def multi_ping(ip_list, pool_size=None):
    """
    Pings a list of provided IP addresses and returns a list of responding
    addresses.

    Requires:
        'ip_list' - list; List of IP addresses
    Optional:
        'pool_size' - int; Can adjust the pool size
    """

    if not pool_size:
        pool_size = 50

    status_dict = {}

    start_time = time.time()

    while True:
        try:
            with ThreadPoolExecutor(max_workers=int(pool_size)) as executor:
                status_list = [ip_status for ip_status in executor.map(
                                check_status, ip_list) if ip_status]
            break
        except OSError as e:
            pool_size = 100

    print("--- %s seconds ---" % (time.time() - start_time))

    return len(status_list)
