#!/usr/bin/env python3

"""

gumd, Grande Unified Multicast Daemon


"""
import argparse
import os
import socket
import sys
from functools import partial
from new_reader import reader

DEFAULT_MCAST = "235.35.3.5:3535"

MAJOR = "0"
MINOR = "0"
MAINTAINENCE = "15"


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

    def __init__(self, addr=None, mttl=None, nethost=None):
        self.ip, self.port = addr.rsplit(":", 1)
        self.nethost = nethost
        self.ttl = mttl
        self.mcast_grp = (self.ip, int(self.port))
        self.dgram_size = 1316
        self.sock = self.mk_sock()

    def mk_sock(self):
        """
        mk_sock , create a socket
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        return sock

    def sock4mcast(self):
        """
        sock4mcast tunes the socket for Multicast
        """

        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl)
        if self.nethost == "0.0.0.0":
            return
        self.sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.nethost)
        )

    def stream_mcast(self, vid):
        """
        stream_mcast streams each item on command line
        """

        self.sock4mcast()
        iface = self.sock.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, 4)
        iface = f"{iface[0]}.{iface[1]}.{iface[2]}.{iface[3]}"
        # print(socket.if_nameindex())
        print(f"Multicast Stream Uri: udp://@{self.ip}:{self.port} on host:{iface}")
        with reader(vid) as gum:
            for chunk in iter(partial(gum.read, self.dgram_size), b""):
                self.sock.sendto(chunk, self.mcast_grp)
        self.sock.close()

    def stream_udp(self, vid):
        """
        stream_udp reads a video and streams it via unicast UDP
        """

        print(f"UDP Stream Uri: udp://{self.ip}:{self.port}")
        with reader(vid) as um:
            for chunk in iter(partial(um.read, self.dgram_size), b""):
                self.sock.sendto(chunk, (self.ip, int(self.port)))
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
        "-u",
        "--udp",
        help='Use Unicast Udp instead of Multicast and use this UDP Unicast address like "127.0.0.1:1234"',
    )

    parser.add_argument(
        "-n",
        "--nethost",
        default="0.0.0.0",
        help='Multicast host ip like "127.0.0.1" or "192.168.1.34". Default is "0.0.0.0" (use default interface)',
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

    parser.add_argument(
        "-a",
        "--addr",
        default=DEFAULT_MCAST,
        help='Multicast Address like "227.1.3.10:4310"',
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
    usage: gumd [-h] [-i INPUT] [-u UDP] [-n NETHOST] [-t TTL] [-v] [-a ADDR]

    options:
      -h, --help            show this help message and exit

      -i INPUT, --input INPUT
                            like "/home/a/vid.ts" or "udp://@235.35.3.5:3535" or "https://futzu.com/xaa.ts"

      -u UDP, --udp UDP     Use Unicast Udp instead of Multicast and use this UDP Unicast address like "127.0.0.1:1234"

      -n NETHOST, --nethost NETHOST
                            Multicast host ip like "127.0.0.1" or "192.168.1.34". Default is "0.0.0.0" (use default interface)
      -t TTL, --ttl TTL     Multicast TTL 1 - 255

      -v, --version         Show version

      -a ADDR, --addr ADDR  Multicast Address like "227.1.3.10:4310"
    """

    args = parse_args()
    if args.version:
        print(version())
        sys.exit()
    daemonize()
    if args.udp:
        gummie = GumD(args.udp, None, None)
        gummie.stream_udp(args.input)
    else:
        ttl = int(args.ttl).to_bytes(1, byteorder="big")
        gummie = GumD(args.addr, ttl, args.nethost)
        gummie.stream_mcast(args.input)
    sys.exit()


if __name__ == "__main__":
    cli()
