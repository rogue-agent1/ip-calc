#!/usr/bin/env python3
"""ip_calc - IP subnet calculator."""
import sys, argparse, json, ipaddress

def analyze(cidr):
    net = ipaddress.ip_network(cidr, strict=False)
    return {"network": str(net.network_address), "broadcast": str(net.broadcast_address) if net.version == 4 else None, "netmask": str(net.netmask), "hostmask": str(net.hostmask), "prefix": net.prefixlen, "num_addresses": net.num_addresses, "usable_hosts": max(0, net.num_addresses - 2) if net.version == 4 else net.num_addresses, "version": net.version, "is_private": net.is_private, "first_host": str(net.network_address + 1) if net.num_addresses > 2 else str(net.network_address), "last_host": str(net.broadcast_address - 1) if net.version == 4 and net.num_addresses > 2 else None}

def main():
    p = argparse.ArgumentParser(description="IP subnet calculator")
    p.add_argument("cidr", help="CIDR notation (e.g. 192.168.1.0/24)")
    p.add_argument("--contains", help="Check if IP is in subnet")
    p.add_argument("--split", type=int, help="Split into N subnets")
    args = p.parse_args()
    result = analyze(args.cidr)
    if args.contains:
        result["contains"] = {args.contains: ipaddress.ip_address(args.contains) in ipaddress.ip_network(args.cidr, strict=False)}
    if args.split:
        net = ipaddress.ip_network(args.cidr, strict=False)
        subs = list(net.subnets(prefixlen_diff=args.split))[:16]
        result["subnets"] = [str(s) for s in subs]
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
