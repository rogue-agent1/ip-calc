import argparse, struct, socket

def ip_to_int(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def int_to_ip(n):
    return socket.inet_ntoa(struct.pack("!I", n))

def cidr_info(cidr):
    ip, bits = cidr.split("/")
    bits = int(bits)
    mask = (0xFFFFFFFF << (32 - bits)) & 0xFFFFFFFF
    ip_int = ip_to_int(ip)
    network = ip_int & mask
    broadcast = network | (~mask & 0xFFFFFFFF)
    first = network + 1 if bits < 31 else network
    last = broadcast - 1 if bits < 31 else broadcast
    hosts = max(0, (1 << (32 - bits)) - 2)
    return {
        "network": int_to_ip(network), "broadcast": int_to_ip(broadcast),
        "netmask": int_to_ip(mask), "first": int_to_ip(first),
        "last": int_to_ip(last), "hosts": hosts, "cidr": bits,
    }

def main():
    p = argparse.ArgumentParser(description="IP/subnet calculator")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("info").add_argument("cidr", help="IP/CIDR e.g. 192.168.1.0/24")
    c = sub.add_parser("contains")
    c.add_argument("cidr"); c.add_argument("ip")
    args = p.parse_args()
    if args.cmd == "info":
        info = cidr_info(args.cidr)
        for k, v in info.items(): print(f"{k:12s}: {v}")
    elif args.cmd == "contains":
        info = cidr_info(args.cidr)
        ip_int = ip_to_int(args.ip)
        net_int = ip_to_int(info["network"])
        bcast_int = ip_to_int(info["broadcast"])
        print("yes" if net_int <= ip_int <= bcast_int else "no")
    else:
        p.print_help()

if __name__ == "__main__":
    main()
