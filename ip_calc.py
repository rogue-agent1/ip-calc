#!/usr/bin/env python3
"""ip_calc - IPv4 subnet calculator."""
import sys, struct, socket
def ip2int(ip): return struct.unpack("!I", socket.inet_aton(ip))[0]
def int2ip(n): return socket.inet_ntoa(struct.pack("!I", n))
def calc(cidr):
    ip, prefix = cidr.split("/"); prefix = int(prefix)
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    net = ip2int(ip) & mask; bcast = net | ~mask & 0xFFFFFFFF
    hosts = (1 << (32 - prefix)) - 2
    return {"network":int2ip(net),"broadcast":int2ip(bcast),"netmask":int2ip(mask),
            "prefix":prefix,"hosts":max(hosts,0),"first":int2ip(net+1) if hosts>0 else "N/A",
            "last":int2ip(bcast-1) if hosts>0 else "N/A","wildcard":int2ip(~mask & 0xFFFFFFFF)}
def contains(cidr, ip):
    info = calc(cidr); return ip2int(info["network"]) <= ip2int(ip) <= ip2int(info["broadcast"])
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: ip_calc.py <CIDR> [check IP]"); sys.exit(1)
    if len(sys.argv) == 3:
        print("Yes" if contains(sys.argv[1], sys.argv[2]) else "No")
    else:
        for k,v in calc(sys.argv[1]).items(): print(f"{k:>12}: {v}")
