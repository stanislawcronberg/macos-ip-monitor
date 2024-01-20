import ipaddress
import json
from enum import Enum

import requests
from config import Config
from logger_config import logger


class IpProtocol(Enum):
    IPv4 = "IPv4"
    IPv6 = "IPv6"
    INVALID = "Invalid"


def retrieve_ip() -> str | None:
    try:
        response = requests.get(Config.PUBLIC_IP_WEBSITE)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        return

    ip_info: dict = json.loads(response.text.strip())

    if "ip" not in ip_info:
        logger.error(f"Key 'ip' not found in reponse dict from {Config.PUBLIC_IP_WEBSITE}.")
        return

    return ip_info["ip"]


def validate_ip(ip: str) -> IpProtocol:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError as e:
        logger.error(f"Invalid IP Address: {e}")
        return IpProtocol.INVALID

    return IpProtocol.IPv4 if isinstance(addr, ipaddress.IPv4Address) else IpProtocol.IPv6
