#!/usr/bin/env python3
"""IP calculator — subnet masks, CIDR notation, address ranges."""
import sys, struct, socket

def ip_to_int(ip): return struct.unpack("!I", socket.inet_aton(ip))[0]
def int_to_ip(n): return socket.inet_ntoa(struct.pack("!I", n))

def subnet_info(cidr):
    ip_str, prefix = cidr.split("/"); prefix = int(prefix)
    ip = ip_to_int(ip_str); mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    network = ip & mask; broadcast = network | (~mask & 0xFFFFFFFF)
    first_host = network + 1; last_host = broadcast - 1
    hosts = max(0, broadcast - network - 1)
    return {"network": int_to_ip(network), "broadcast": int_to_ip(broadcast),
            "mask": int_to_ip(mask), "first": int_to_ip(first_host),
            "last": int_to_ip(last_host), "hosts": hosts, "prefix": prefix,
            "binary_mask": bin(mask)[2:].zfill(32)}

def ip_to_binary(ip):
    return ".".join(bin(int(o))[2:].zfill(8) for o in ip.split("."))

def cli():
    if len(sys.argv) < 2: print("Usage: ip_calc <CIDR> | ip_calc binary <IP>"); sys.exit(1)
    if sys.argv[1] == "binary": print(ip_to_binary(sys.argv[2])); return
    info = subnet_info(sys.argv[1])
    for k, v in info.items(): print(f"  {k:>12}: {v}")

if __name__ == "__main__": cli()
