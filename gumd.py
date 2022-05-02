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


def reader(uri):
    """
    reader returns an open file handle.

    stdin:              cat video.ts | gumd
    file uri:           gumd -i /home/you/video.ts
    http(s) uri:        gumd -i https://example.com/vid.ts
    udp uris:           gumd -i udp://1.2.3.4:5555
    multicast uris:     gumd -i udp://@227.1.3.10:4310

    """
    # read from stdin
    if uri in [None,sys.stdin.buffer]:
        return sys.stdin.buffer
    # Multicast
    if uri.startswith("udp://@"):
        return open_mcast(uri)
    # Udp
    if uri.startswith("udp://"):
        return open_udp(uri)
    # Http(s)
    if uri.startswith("http"):
        return urllib.request.urlopen(uri)
    # File
    return open(uri, "rb")


def read_stream(sock):
    """
    return a socket that can be read like a file.
    """
    return sock.makefile(mode="rb")


def _mk_udp_sock(udp_ip, udp_port):
    """
    udp socket setup
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    return sock


def _mk_mcast_sock(mcast_grp, mcast_port, all_grps=True):
    """
    multicast socket setup
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 5400000)
    if all_grps:
        sock.bind(("", mcast_port))
    else:
        sock.bind((mcast_grp, mcast_port))
    mreq = struct.pack("4sl", socket.inet_aton(mcast_grp), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock


def open_udp(uri):
    """
    udp://1.2.3.4:5555
    """
    udp_ip, udp_port = (uri.split("udp://")[1]).split(":")
    udp_port = int(udp_port)
    udp_sock = _mk_udp_sock(udp_ip, udp_port)
    return read_stream(udp_sock)


def open_mcast(uri):
    """
    udp://@227.1.3.10:4310
    """
    mcast_grp, mcast_port = (uri.split("udp://@")[1]).split(":")
    mcast_port = int(mcast_port)
    mcast_sock = _mk_mcast_sock(mcast_grp, mcast_port)
    return read_stream(mcast_sock)


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


if __name__ == "__main__":
    args = parse_args()
    daemonize()
    ttl = int(args.ttl).to_bytes(1, byteorder="big")
    gummie = GumD(args.addr, ttl)
    gummie.mcast(args.input)
    sys.exit()