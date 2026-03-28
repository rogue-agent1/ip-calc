#!/usr/bin/env python3
"""IP/CIDR calculator."""
import sys
def ip_to_int(ip): parts=list(map(int,ip.split('.'))); return (parts[0]<<24)|(parts[1]<<16)|(parts[2]<<8)|parts[3]
def int_to_ip(n): return f"{(n>>24)&255}.{(n>>16)&255}.{(n>>8)&255}.{n&255}"
def calc(cidr):
    ip,prefix=cidr.split('/'); prefix=int(prefix)
    mask=(0xFFFFFFFF<<(32-prefix))&0xFFFFFFFF
    net=ip_to_int(ip)&mask; bcast=net|(~mask&0xFFFFFFFF)
    first=net+1; last=bcast-1; hosts=max(0,(1<<(32-prefix))-2)
    return {"network":int_to_ip(net),"broadcast":int_to_ip(bcast),"netmask":int_to_ip(mask),
            "first":int_to_ip(first),"last":int_to_ip(last),"hosts":hosts,"prefix":prefix}
def main():
    if "--demo" in sys.argv:
        for cidr in ["192.168.1.0/24","10.0.0.0/8","172.16.0.0/16","192.168.1.128/25"]:
            r=calc(cidr); print(f"\n{cidr}:")
            for k,v in r.items(): print(f"  {k}: {v}")
    elif len(sys.argv)>1:
        r=calc(sys.argv[1])
        for k,v in r.items(): print(f"{k}: {v}")
if __name__=="__main__": main()
