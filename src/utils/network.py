import ipaddress
import json
from enum import Enum

import requests
from loguru import logger


class IpProtocol(Enum):
    IPv4 = "IPv4"
    IPv6 = "IPv6"


# TODO: Log with exceptions in loguru
def retrieve_ip(ip_website: str) -> str | None:
    try:
        response = requests.get(ip_website)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        return

    ip_info: dict = json.loads(response.text.strip())

    if "ip" not in ip_info:
        logger.error(f"Key 'ip' not found in reponse dict from {ip_website}.")
        return

    return ip_info["ip"]


def get_ip_protocol(ip: str) -> IpProtocol | None:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError as e:
        logger.error(f"Invalid IP Address: {e}")
        return

    return IpProtocol.IPv4 if isinstance(addr, ipaddress.IPv4Address) else IpProtocol.IPv6
