from ipaddress import IPv4Address

from loguru import logger
from fastapi import FastAPI, Request

import arp

THE_REGISTER: list[tuple[str, str, list[tuple[str, str]]]] = []
api = FastAPI()

@api.get("/probe")
def rev_probe(request: Request) -> str:
    requester = request.client
    if requester is None:
        logger.error('Request from unknown client')
        return 'Client unknown'

    ip_req = IPv4Address(requester.host)

    logger.debug('Request from [{}], performing ARP ping', ip_req)
    arp_results = arp.do_arp_ping(ip_req)

    logger.info('\n'.join(
        '{:>15s}:\t{} => {}'.format(ip_req.exploded, mac, ip) for mac, ip in arp_results
    ))

    metadata = sorted((k, v) for k, v in request.query_params.items())
    THE_REGISTER.extend((ipaddr, macaddr, metadata) for macaddr, ipaddr in arp_results)

    return 'Endpoint [{}] registered to [{}]'.format(ip_req, '; '.join('{}={}'.format(k, v) for k, v in metadata))

@api.get('/')
def usage() -> str:
    return 'Usage: GET /probe?key1=value1&key2=value2 ...\n'
