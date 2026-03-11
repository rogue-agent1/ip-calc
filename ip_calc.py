#!/usr/bin/env python3
"""IP calculator — subnet info, CIDR, network/broadcast."""
import sys
def parse_cidr(cidr):
    ip, bits = cidr.split("/"); bits = int(bits)
    octets = [int(o) for o in ip.split(".")]
    ip_int = sum(o << (24 - 8*i) for i, o in enumerate(octets))
    mask = ((1 << 32) - 1) ^ ((1 << (32 - bits)) - 1)
    network = ip_int & mask; broadcast = network | ~mask & 0xFFFFFFFF
    hosts = (1 << (32 - bits)) - 2
    def fmt(n): return ".".join(str((n >> (24-8*i)) & 0xFF) for i in range(4))
    return {"network": fmt(network), "broadcast": fmt(broadcast), "mask": fmt(mask),
            "hosts": max(0, hosts), "first": fmt(network+1), "last": fmt(broadcast-1), "cidr": bits}
if __name__ == "__main__":
    cidr = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.0/24"
    info = parse_cidr(cidr)
    for k, v in info.items(): print(f"  {k:12s}: {v}")
