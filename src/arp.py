from ipaddress import IPv4Address
from typing import cast

from loguru import logger

from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp
from scapy.config import conf as scapy_conf

SELF_IP: IPv4Address = None # type: ignore

def get_hwaddr() -> tuple[IPv4Address, str]:
    global SELF_IP

    iface, psrc, _ = cast(tuple[str, str, object],
        scapy_conf.route.route(dst = IPv4Address('1.1.1.1').exploded) # pyright: ignore[reportUnknownMemberType]
    )
    SELF_IP = IPv4Address(psrc) # pyright: ignore[reportConstantRedefinition]

    return SELF_IP, iface

def do_arp_ping(ip_address: IPv4Address) -> list[tuple[str, str]]:

    ETHER_BROADCAST = "FF:FF:FF:FF:FF:FF" # I hate strings
    arp_request = Ether(dst = ETHER_BROADCAST) / ARP(psrc = SELF_IP.exploded, pdst = ip_address.exploded) # I really hate strings

    answers, noreplies = srp(arp_request, timeout = 5, verbose = False)

    if len(noreplies) > 0:
        logger.warning("ARP ping failed for addresses: [{}]", ', '.join(pkt.pdst for pkt in noreplies))

    return [(reply.answer.hwsrc, reply.answer.psrc) for reply in answers]
