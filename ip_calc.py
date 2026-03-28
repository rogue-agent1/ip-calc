#!/usr/bin/env python3
"""IP calculator — subnet masks, CIDR notation, address ranges."""
import sys, struct, socket
def ip_to_int(ip): return struct.unpack("!I", socket.inet_aton(ip))[0]
def int_to_ip(n): return socket.inet_ntoa(struct.pack("!I", n))
def subnet_info(cidr):
    ip_str, prefix = cidr.split("/"); prefix = int(prefix)
    ip = ip_to_int(ip_str); mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    network = ip & mask; broadcast = network | (~mask & 0xFFFFFFFF)
    return {"network": int_to_ip(network), "broadcast": int_to_ip(broadcast), "mask": int_to_ip(mask), "hosts": max(0, broadcast-network-1), "prefix": prefix}
def cli():
    if len(sys.argv) < 2: print("Usage: ip_calc <CIDR>"); sys.exit(1)
    for k,v in subnet_info(sys.argv[1]).items(): print(f"  {k:>12}: {v}")
if __name__ == "__main__": cli()
