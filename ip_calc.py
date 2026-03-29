#!/usr/bin/env python3
"""ip_calc - IPv4 subnet calculator and address utilities."""
import sys

def ip_to_int(ip):
    parts = [int(x) for x in ip.split(".")]
    return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]

def int_to_ip(n):
    return f"{(n>>24)&255}.{(n>>16)&255}.{(n>>8)&255}.{n&255}"

def cidr_to_mask(prefix):
    return (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

def mask_to_cidr(mask):
    n = ip_to_int(mask) if isinstance(mask, str) else mask
    bits = 0
    while n & (1 << (31 - bits)):
        bits += 1
        if bits == 32:
            break
    return bits

class Subnet:
    def __init__(self, cidr):
        ip, prefix = cidr.split("/")
        self.prefix = int(prefix)
        self.mask = cidr_to_mask(self.prefix)
        self.network = ip_to_int(ip) & self.mask
        self.broadcast = self.network | (~self.mask & 0xFFFFFFFF)
    @property
    def network_addr(self):
        return int_to_ip(self.network)
    @property
    def broadcast_addr(self):
        return int_to_ip(self.broadcast)
    @property
    def mask_addr(self):
        return int_to_ip(self.mask)
    @property
    def num_hosts(self):
        return max(0, self.broadcast - self.network - 1)
    def contains(self, ip):
        return (ip_to_int(ip) & self.mask) == self.network
    def hosts(self):
        for i in range(self.network + 1, self.broadcast):
            yield int_to_ip(i)

def test():
    s = Subnet("192.168.1.0/24")
    assert s.network_addr == "192.168.1.0"
    assert s.broadcast_addr == "192.168.1.255"
    assert s.mask_addr == "255.255.255.0"
    assert s.num_hosts == 254
    assert s.contains("192.168.1.100")
    assert not s.contains("192.168.2.1")
    s2 = Subnet("10.0.0.0/8")
    assert s2.num_hosts == 16777214
    assert s2.contains("10.255.255.254")
    s3 = Subnet("172.16.0.128/25")
    assert s3.network_addr == "172.16.0.128"
    assert s3.num_hosts == 126
    assert mask_to_cidr("255.255.255.0") == 24
    print("OK: ip_calc")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: ip_calc.py test")
