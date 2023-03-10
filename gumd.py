#!/usr/bin/env python3

"""

gumd, Grande Unicast Multicast Daemon


"""
import argparse
import os
import socket
import sys
from functools import partial
from new_reader import reader

DEFAULT_MULTICAST = "235.35.3.5:3535"
DEFAULT_UNICAST = "127.0.0.1:9999"

MAJOR = "0"
MINOR = "0"
MAINTAINENCE = "17"


def version():
    """
    version prints version as a string

    """
    return f"{MAJOR}.{MINOR}.{MAINTAINENCE}"


class GumD:
    """
    GumD class is the UDP Unicast/Multicast sender
    """

    def __init__(self, addr=None, mttl=1, bind_addr="0.0.0.0:1025"):
        self.dest_ip, self.dest_port = addr.rsplit(":", 1)
        self.src_ip, self.src_port = bind_addr.rsplit(":", 1)
        self.ttl = mttl
        self.dest_grp = (self.dest_ip, int(self.dest_port))
        self.dgram_size = 1316
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.bind((self.src_ip, int(self.src_port)))

    def send_stream(self, vid, multicast=True):
        proto = "udp://"
        if multicast:
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl)
            proto = proto + "@"
        print(
            f"Stream Uri: {proto}{self.dest_ip}:{self.dest_port} from source {self.src_ip}:{self.src_port}"
        )
        with reader(vid) as gum:
            for chunk in iter(partial(gum.read, self.dgram_size), b""):
                self.sock.sendto(chunk, self.dest_grp)
        self.sock.close()


def parse_args():
    """
    parse_args parse command line args
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default=None,
        help="""like "/home/a/vid.ts"
                or "udp://@235.35.3.5:3535"
                or "https://futzu.com/xaa.ts"
             """,
    )

    parser.add_argument(
        "-a",
        "--addr",
        default=DEFAULT_MULTICAST,
        help='Destination Address:Port like "227.1.3.10:4310"',
    )

    parser.add_argument(
        "-u",
        "--unicast",
        action="store_const",
        default=False,
        const=True,
        help='Use Unicast instead of Multicast',
    )

    parser.add_argument(
        "-b",
        "--bind_addr",
        default="0.0.0.0:1025",
        help='Local IP and Port to bind to like "192.168.1.34:5555". Default is "0.0.0.0:1025"',
    )

    parser.add_argument(
        "-t",
        "--ttl",
        default=1,
        help="Multicast TTL 1 - 255",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="store_const",
        default=False,
        const=True,
        help="Show version",
    )

    return parser.parse_args()


def fork():
    """
    fork
    """

    pid = os.fork()
    if pid > 0:
        sys.exit(0)


def daemonize():
    """
    The Steven's double fork
    """

    fork()
    fork()


def cli():
    """
        usage: gumd.py [-h] [-i INPUT] [-a ADDR] [-u] [-b BIND_ADDR] [-t TTL] [-v]

        optional arguments:
          -h, --help            show this help message and exit
          -i INPUT, --input INPUT
                                like "/home/a/vid.ts" or "udp://@235.35.3.5:3535" or "https://futzu.com/xaa.ts"
          -a ADDR, --addr ADDR  Destination Address:Port like "227.1.3.10:4310"
          -u, --unicast         Use Unicast instead of Multicast
          -b BIND_ADDR, --bind_addr BIND_ADDR
                                Local IP and Port to bind to like "192.168.1.34:5555". Default is "0.0.0.0:1025"
          -t TTL, --ttl TTL     Multicast TTL 1 - 255
          -v, --version         Show version
    """

    args = parse_args()
    if args.version:
        print(version())
        sys.exit()
    daemonize()
    ttl = int(args.ttl).to_bytes(1, byteorder="big")
    dest_addr= args.addr
    if args.unicast:
        if dest_addr == DEFAULT_MULTICAST:
            dest_addr = DEFAULT_UNICAST   
    gummie = GumD(dest_addr, ttl, args.bind_addr)
    if args.unicast:
        gummie.send_stream(args.input, multicast=False)
    else:
        gummie.send_stream(args.input, multicast=True)
    sys.exit()


if __name__ == "__main__":
    cli()
