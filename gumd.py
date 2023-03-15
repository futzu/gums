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


DGRAM_SIZE = 1316

DEFAULT_MULTICAST = "235.35.3.5:3535"
DEFAULT_UNICAST = "127.0.0.1:3535"

MAJOR = "0"
MINOR = "0"
MAINTAINENCE = "21"


def version():
    """
    version prints version as a string

    """
    return f"{MAJOR}.{MINOR}.{MAINTAINENCE}"


class GumD:
    """
    GumD class is the UDP Unicast/Multicast sender
    """

    def __init__(self, addr=None, mttl=1, bind_addr="0.0.0.0"):
        self.dest_ip, self.dest_port = addr.rsplit(":", 1)
        self.src_ip = bind_addr.rsplit(":", 1)[0]
        self.src_port = 0
        self.ttl = mttl
        self.dest_grp = (self.dest_ip, int(self.dest_port))
        self.sock = self._mk_sock()
        self.sock.bind((self.src_ip, self.src_port))

    def _mk_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, "SO_REUSEPORT"):
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        return sock

    def iter_dgrams(self, vid):
        """
        iter_dgrams iterates over the video and sends
        self.dgram_size chunks of video to the socket.
        """
        with reader(vid) as gum:
            for dgram in iter(partial(gum.read, DGRAM_SIZE), b""):
                self.sock.sendto(dgram, self.dest_grp)

    def send_stream(self, vid, multicast=True):
        """
        send_stream sets multicast ttl if needed,
        prints socket address info,
        calls self.iter_dgrams,
        and closes the socket
        """
        proto = "udp://"
        if multicast:
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl)
            proto = proto + "@"
        src_ip, src_port = self.sock.getsockname()
        print(
            f"\n\tStream: {proto}{self.dest_ip}:{self.dest_port}\n\tSource: {src_ip}:{src_port}\n"
        )
        self.iter_dgrams(vid)
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
        help='Destination IP:Port like "227.1.3.10:4310"',
    )

    parser.add_argument(
        "-u",
        "--unicast",
        action="store_const",
        default=False,
        const=True,
        help="Use Unicast instead of Multicast",
    )

    parser.add_argument(
        "-b",
        "--bind_addr",
        default="0.0.0.0",
        help='Local IP to bind to like "192.168.1.34". Default is 0.0.0.0',
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
    cli adds command line args
    passes them to a Gumd instance
    and calls self.send_stream
    in just one function call

    Use like this

    import gumd

    if __name__ == "__main__":
        gund.cli()


    """

    args = parse_args()
    if args.version:
        print(version())
        sys.exit()
    daemonize()
    ttl = int(args.ttl).to_bytes(1, byteorder="big")
    multicast = True
    dest_addr = args.addr
    if args.unicast:
        multicast = False
        if dest_addr == DEFAULT_MULTICAST:
            dest_addr = DEFAULT_UNICAST
    gummie = GumD(dest_addr, ttl, args.bind_addr)
    gummie.send_stream(args.input, multicast)
    sys.exit()


if __name__ == "__main__":
    cli()
