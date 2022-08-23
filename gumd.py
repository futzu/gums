#!/usr/bin/env python3

"""

gumd, Grande Unified Multicast Daemon


"""
import argparse
import os
import socket
import struct
import sys
import urllib.request
from functools import partial
from new_reader import reader


MAJOR = "0"
MINOR = "0"
MAINTAINENCE = "5"


def version():
    """
    version prints version as a string

    Odd number versions are releases.
    Even number versions are testing builds between releases.

    Used to set version in setup.py
    and as an easy way to check which
    version you have installed.

    """
    return f"{MAJOR}.{MINOR}.{MAINTAINENCE}"



class GumD:
    """
    GumD class is a multicast server instance
    """

    def __init__(self, addr, mttl):
        self.mcast_ip, self.mcast_port = addr.rsplit(":", 1)
        self.ttl = mttl
        self.pack_size = 1316
        self.sock = self.mk_sock()

    def mk_sock(self):
        """
        mk_sock , create a socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl)
        return sock

    def vid2mstream(self, vid):
        """
        vid2mstream read a video and stream it multicast
        """
        with reader(vid) as gum:
            for chunk in iter(partial(gum.read, self.pack_size), b""):
                self.sock.sendto(chunk, (self.mcast_ip, int(self.mcast_port)))

    def mcast(self, vid):
        """
        mcast streams each item on command line
        """
        print(f"stream uri: udp://@{self.mcast_ip}:{self.mcast_port}")
        self.vid2mstream(vid)
        self.sock.close()
        sys.exit()


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
        "-a", "--addr", default="235.35.3.5:3535", help='like "227.1.3.10:4310"'
    )

    parser.add_argument(
        "-t",
        "--ttl",
        default=1,
        help="1 - 255",
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
    cli  makes a fully functional command line tool

    usage: gumd [-h] [-i INPUT] [-a ADDR] [-t TTL] [-v]

    options:

      -h, --help            show this help message and exit

      -i INPUT, --input INPUT
                            like "/home/a/vid.ts" or
                            "udp://@235.35.3.5:3535" or
                            "https://futzu.com/xaa.ts"

      -a ADDR, --addr ADDR  like "227.1.3.10:4310"

      -t TTL, --ttl TTL     1 - 255

      -v, --version         Show version

    """
    args = parse_args()
    if args.version:
        print(version())
        sys.exit()
    daemonize()
    ttl = int(args.ttl).to_bytes(1, byteorder="big")
    gummie = GumD(args.addr, ttl)
    gummie.mcast(args.input)
    sys.exit()


if __name__ == "__main__":
    cli()
