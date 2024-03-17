#!/usr/bin/env python3

"""

gumc, Grande Unified Multicast Client


"""


import argparse
import sys
import time
from new_reader import reader

MILLION = 1024 << 10

MAJOR = "0"
MINOR = "0"
MAINTAINENCE = "11"


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


class GumC:
    """

    GumC, Grande Unified Multicast Client

    """

    def __init__(
        self,
        instuff="udp://@235.35.3.5:3535",
        outstuff=sys.stdout.buffer,
        bytesize=None,
    ):
        self.instuff = instuff
        self.outstuff = outstuff
        if outstuff != sys.stdout.buffer:
            self.outstuff = open(self.outstuff, "wb")
        self.rdr = reader(self.instuff)
        self.bytesize = bytesize
        self.total_bytes = 0
        self.start_time = None

    def chk_bytesize(self):
        """
        chk_bytesize checks if self.total_bytes
        is larger than self.bytesize.
        """
        if self.bytesize is not None:
            if self.total_bytes >= self.bytesize:
                sys.exit()

    def elapsed(self):
        """
        elapsed calculates how long the client has been reading packets.
        """
        return time.time() - self.start_time

    def read(self, num_bites):
        """
        read reads num_bites and returns them
        """
        data = None
        try:
            data = self.rdr.read(num_bites)
        except:
            sys.stderr.write("Timeout on the socket, no more data available.\n")
            sys.exit()
        return data

    def show_rate(self):
        """
        show_rate shows read rate of gumc.
        """
        elapsed = self.elapsed()
        rate = (self.total_bytes / MILLION) / elapsed
        print(
            f"\t{self.total_bytes/MILLION:0.2f} MB received in {elapsed:5.2f} seconds. {rate:3.2f} MB/Sec",
            end="\r",
            file=sys.stderr,
        )

    def started(self):
        """
        started sets self.start_time if it's not set.
        """
        if not self.start_time:
            self.start_time = time.time()

    def write(self, chunk):
        """
        write writes to outstuff
        """
        self.outstuff.write(chunk)
        self.total_bytes += len(chunk)


def parse_args():
    """
    parse_args parse command line args
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--instuff",
        default="udp://@235.35.3.5:3535",
        help="Input, default is 'udp://@235.35.3.5:3535' ",
    )

    parser.add_argument(
        "-b",
        "--bytesize",
        default=None,
        type=int,
        help="Number of bytes to read, default is to read all.",
    )

    parser.add_argument(
        "-o",
        "--outstuff",
        default=sys.stdout.buffer,
        help="Output, default is sys.stdout.buffer(for piping)",
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


def cli():
    """
    cli  makes a fully functional command line tool

    usage: gumc [-h] [-i INSTUFF] [-b BYTESIZE] [-o OUTSTUFF] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -i INSTUFF, --instuff INSTUFF
                            Input, default is 'udp://@235.35.3.5:3535'
      -b BYTESIZE, --bytesize BYTESIZE
                            Number of bytes to read, default is to read all.
      -o OUTSTUFF, --outstuff OUTSTUFF
                            Output, default is sys.stdout.buffer(for piping)
      -v, --version         Show version


    """
    args = parse_args()
    if args.version:
        print(version())
        sys.exit()
    gumc = GumC(instuff=args.instuff, outstuff=args.outstuff, bytesize=args.bytesize)
    while gumc.instuff:
        chunk = gumc.read(1316)
        gumc.started()
        gumc.write(chunk)
        gumc.show_rate()
        gumc.chk_bytesize()


if __name__ == "__main__":
    cli()
