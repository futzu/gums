#!/usr/bin/env python3

"""

gumc, Grande Unified Multicast Client


"""



import argparse
import sys
from new_reader import reader


MAJOR = "0"
MINOR = "0"
MAINTAINENCE = "7"


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

    def __init__(self, instuff="udp://@235.35.3.5:3535"):
        self.rdr = reader(instuff)

    def read(self,num_bites):
        """
        GumC.read reads num_bites and returns them
        """
        return self.rdr.read(num_bites)
        

def parse_args():
    """
    parse_args parse command line args
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--instuff",
        default='udp://@235.35.3.5:3535',
        help="""default is 'udp://@235.35.3.5:3535'
                                """,
    )

    parser.add_argument(
        "-b",
        "--bytesize",
        default=1,
        type=int,
        help="Number of bytes to read. default is 1",
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


    usage: gumc [-h] [-i INSTUFF] [-b BYTESIZE]

    optional arguments:
      -h, --help            show this help message and exit
      -i INSTUFF, --instuff INSTUFF
                            default is 'udp://@235.35.3.5:3535'
      -b BYTESIZE, --bytesize BYTESIZE
                            Number of bytes to read. default is 1

      -v, --version         Show version

    """
    args = parse_args()
    if args.version:
        version()
    gumc =GumC(args.instuff)
    print(gumc.read(args.bytesize))

    
if __name__ == '__main__':
    cli()
