#!/usr/bin/env python3
import subprocess
import re
import os
import sys
import time
import argparse

BPF_TO_XDP = {
    "bpf_pass_pkts": "xdp_pass_pkts",
    "bpf_pass_bytes": "xdp_pass_bytes",
    "bpf_app1_pkts": "xdp_drop_pkts",
    "bpf_app1_bytes": "xdp_drop_bytes",
    "bpf_app2_pkts": "xdp_tx_pkts",
    "bpf_app2_bytes": "xdp_tx_bytes",
    "bpf_app3_pkts": "xdp_aborted_pkts",
    "bpf_app3_bytes": "xdp_aborted_bytes"
}

class Status:
    # Init Status object with interval and mode attr
    def __init__(self) -> None:
        self.last_total = {}
        self.interval = 1
    # Search the xdp related output and return a list of lines
    def _search_xdp_stat(self, source):
        res = []
        for line in source.split('\n'):
            if re.search(r'bpf_.*', line) is not None:
                item, stat = line.split(":")[0].strip(), line.split(":")[1].strip()
                item = item.replace(item, BPF_TO_XDP[item])
                res.append({
                    "subject": item,
                    "total": stat,
                    "per_sec": '0'
                })
        # init the last_total attr, prepare for the calculation of pps
        if self.last_total == {}:
            for i in res:
                self.last_total[i['subject']] = i['total']
        else:
            for i in res:
                # calculate pps
                i['per_sec'] = str((int(i['total']) - int(self.last_total[i['subject']]))//self.interval)
                self.last_total[i['subject']] = i['total']
        return res


    def get_ethtool_output(self, ifname):
        # run ethtool with -S
        stdout = subprocess.check_output(['ethtool', '-S', ifname]).decode('utf-8')
        # get the result list, the element in the list is tuple
        xdp_output = self._search_xdp_stat(stdout)
        print(f"{'Action':20} {'Total(all time)':20} {'Per Second':20}")
        for i in xdp_output:
            if "pkts" in i['subject']:
                print(f"{i['subject']:20} {i['total']:20} {i['per_sec']+' pkt/s':20}")
            elif "bytes" in i['subject']:
                print(f"{i['subject']:20} {i['total']:20} {i['per_sec']+' Byte/s':20}")

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A easy tool to check the xdp offloading status")
    parser.add_argument("--port", "-p", help="Network interface which running the XDP offloading, required", required=True)
    parser.add_argument("--interval", "-i", help="Interval to show the output, default is 1 second.", default=1, type=int)
    args = parser.parse_args()

    offload_status = Status()
    offload_status.interval = args.interval
    try:
        while True:
            offload_status.get_ethtool_output(args.port)
            # add a newline after one round
            print()
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print('^Bye.')