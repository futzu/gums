"""

mudpie, Multicast Unified Daemon in Python I Explained


"""


import socket
import sys
from functools import partial
from threefive import reader


class MudPie:
    """
    MudPie is a multicast server
    """
    def __init__(self, mip, mport, mttl):
        self.mcast_ip = mip  
        self.mcast_port = mport  
        self.ttl = mttl  
        self.pie_size = 1316
        self.sock = self.mk_sock()

    def mk_sock(self):
        """
        mk_sock , create a socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl)
        return sock

    def vid2mudpie(self, vid):
        """
        vid2mudpie read a video and stream it multicast
        """
        with reader(vid) as mud:
            for mudpie in iter(partial(mud.read, self.pie_size), b""):
                self.sock.sendto(mudpie, (self.mcast_ip, self.mcast_port))

    def mcast(self):
        """
        mcast streams each item on command line
        """
        print(f"udp://@{self.mcast_ip}:{self.mcast_port}")
        for vid in sys.argv[1:]:
            self.vid2mudpie(vid)
        self.sock.close()
        sys.exit()


if __name__ == "__main__":
    M_IP = "235.35.3.5"
    M_PORT = 3535
    M_TTL = b"\x1f"
    pie = MudPie(M_IP, M_PORT, M_TTL)
    pie.mcast()
