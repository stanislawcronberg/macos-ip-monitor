import requests
import json
import ipaddress
from enum import Enum
from pathlib import Path
from pync import Notifier
from loguru import logger


class IpProtocol(Enum):
    IPv4 = "IPv4"
    IPv6 = "IPv6"
    INVALID = "Invalid"


IP_PROTOCOL = IpProtocol.IPv4
PUBLIC_IP_WEBSITE = "https://ipinfo.io"
NOTIFICATION_LINK = "https://azure.com"
LOG_FILE = Path("logs/ip_change.log")
CURRENT_IP_FILE = Path("logs/current_ip.txt")
DEBUG = True

logger.add(LOG_FILE, rotation="1 MB")


def get_current_ip() -> str | None:
    try:
        response = requests.get(PUBLIC_IP_WEBSITE)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        return
    
    ip = json.loads(response.text.strip())["ip"]
    if ip is None:
        logger.warning(f"IP from {PUBLIC_IP_WEBSITE} returned None.")

    return ip


def notify_ip_change(new_ip: str | None) -> None:
    message = f"Your public IP address has changed to {new_ip}."
    Notifier.notify(title="IP Address Change", message=message, open=NOTIFICATION_LINK)


def update_current_ip_file(current_ip: str) -> None:
    with open(CURRENT_IP_FILE, "w") as file:
        file.write(current_ip)

    logger.info(f"IP address changed to {current_ip}")


def validate_ip(ip: str, protocol: IpProtocol) -> IpProtocol:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError as e:
        logger.error(e)
        logger.error(f"IP Address from {PUBLIC_IP_WEBSITE} is neither IPv4 or IPv6. Received: {ip}")
        return IpProtocol.INVALID
    
    protocol = IpProtocol.IPv4 if isinstance(addr, ipaddress.IPv4Address) else IpProtocol.IPv6
    logger.info(f"Received IP protocol: {protocol.value}")
    
    return protocol


def main():
    previous_ip = None

    if CURRENT_IP_FILE.exists():
        with open(CURRENT_IP_FILE, "r") as file:
            previous_ip = file.read().strip()

    current_ip = get_current_ip()
    protocol: IpProtocol = validate_ip(current_ip, IP_PROTOCOL)
    
    if protocol != IP_PROTOCOL and protocol != IpProtocol.INVALID:
        logger.warning(f"Received IP address {current_ip} is {protocol.value}. Expected an {IP_PROTOCOL.value} address.")

    if DEBUG or current_ip != previous_ip:
        notify_ip_change(current_ip)


if __name__ == "__main__":
    main()
