#!/usr/bin/env python3
"""IP address calculator."""
import struct, socket

def ip_to_int(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def int_to_ip(n):
    return socket.inet_ntoa(struct.pack("!I", n))

def cidr_to_mask(prefix):
    return (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

def mask_to_cidr(mask_int):
    bits = bin(mask_int).count("1")
    return bits

def network_info(cidr):
    ip_str, prefix = cidr.split("/")
    prefix = int(prefix)
    ip = ip_to_int(ip_str)
    mask = cidr_to_mask(prefix)
    network = ip & mask
    broadcast = network | (~mask & 0xFFFFFFFF)
    first_host = network + 1 if prefix < 31 else network
    last_host = broadcast - 1 if prefix < 31 else broadcast
    num_hosts = max(0, broadcast - network - 1) if prefix < 31 else (2 if prefix == 31 else 1)
    return {
        "network": int_to_ip(network), "broadcast": int_to_ip(broadcast),
        "mask": int_to_ip(mask), "prefix": prefix,
        "first_host": int_to_ip(first_host), "last_host": int_to_ip(last_host),
        "num_hosts": num_hosts,
    }

def ip_in_network(ip, cidr):
    info = network_info(cidr)
    ip_int = ip_to_int(ip)
    net_int = ip_to_int(info["network"])
    bcast_int = ip_to_int(info["broadcast"])
    return net_int <= ip_int <= bcast_int

def is_private(ip):
    n = ip_to_int(ip)
    return (ip_to_int("10.0.0.0") <= n <= ip_to_int("10.255.255.255") or
            ip_to_int("172.16.0.0") <= n <= ip_to_int("172.31.255.255") or
            ip_to_int("192.168.0.0") <= n <= ip_to_int("192.168.255.255"))

if __name__ == "__main__":
    import sys
    cidr = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.0/24"
    for k, v in network_info(cidr).items():
        print(f"{k}: {v}")

def test():
    info = network_info("192.168.1.0/24")
    assert info["network"] == "192.168.1.0"
    assert info["broadcast"] == "192.168.1.255"
    assert info["mask"] == "255.255.255.0"
    assert info["num_hosts"] == 254
    assert info["first_host"] == "192.168.1.1"
    assert info["last_host"] == "192.168.1.254"
    # /16
    info2 = network_info("10.0.0.0/16")
    assert info2["num_hosts"] == 65534
    # Membership
    assert ip_in_network("192.168.1.100", "192.168.1.0/24")
    assert not ip_in_network("192.168.2.1", "192.168.1.0/24")
    # Private
    assert is_private("10.0.0.1")
    assert is_private("192.168.1.1")
    assert not is_private("8.8.8.8")
    # Conversions
    assert int_to_ip(ip_to_int("1.2.3.4")) == "1.2.3.4"
    print("  ip_calc: ALL TESTS PASSED")
