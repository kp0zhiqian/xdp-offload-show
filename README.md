# xdp-show
A small tool to provide a easy way to check the XDP offloading status.

## Supported Card

- NFP
- ...adding more

## Usage
```shell
usage: xdp_offload_show.py [-h] --port PORT [--interval INTERVAL]

Arguments for xdp-offload-show tool

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  Network interface which running the XDP offloading, required
  --interval INTERVAL, -i INTERVAL
                        Interval to show the output, default is 1 second.
```

## Output example:
```shell
Action               Total                Per Second
xdp_pass_pkts        132345116            6708186 pkt/s
xdp_pass_bytes       7940706983           402491160 Byte/s
xdp_drop_pkts        216676884187         0 pkt/s
xdp_drop_bytes       13000613071871       0 Byte/s
xdp_tx_pkts          0                    0 pkt/s
xdp_tx_bytes         0                    0 Byte/s
xdp_aborted_pkts     0                    0 pkt/s
xdp_aborted_bytes    0                    0 Byte/s
```