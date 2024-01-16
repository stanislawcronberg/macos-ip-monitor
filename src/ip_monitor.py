import ipaddress
import json
import os
import subprocess
from pathlib import Path

import requests
from dotenv import load_dotenv
from loguru import logger
from pync import Notifier
from structures import IpProtocol

load_dotenv()

IP_PROTOCOL = IpProtocol[os.getenv("IP_PROTOCOL", "IPv4")]
PROCESS_NAME = os.getenv("PROCESS_NAME", "")
PUBLIC_IP_WEBSITE = os.getenv("IP_WEBSITE", "https://ipinfo.io")
NOTIFICATION_LINK = os.getenv("NOTIFICATION_LINK", "https://azure.com")
LOG_FILE = Path(os.getenv("LOG_FILEPATH", "logs/ip_change.log"))
CURRENT_IP_FILE = Path(os.getenv("CURRENT_IP_FILEPATH", "logs/current_ip.txt"))
DEBUG = os.getenv("DEBUG", "False") == "True"

logger.add(LOG_FILE, rotation="1 MB")


def get_current_ip() -> str | None:
    try:
        response = requests.get(PUBLIC_IP_WEBSITE)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        return

    ip_info: dict = json.loads(response.text.strip())

    if "ip" not in ip_info:
        logger.error(f"Key 'ip' not found in reponse dict from {PUBLIC_IP_WEBSITE}.")
        return

    return ip_info["ip"]


def notify_ip_change(new_ip: str | None) -> None:
    message = f"Your public IP address has changed to {new_ip}."
    Notifier.notify(title="IP Address Change", message=message, open=NOTIFICATION_LINK)


def update_current_ip_file(current_ip: str) -> None:
    CURRENT_IP_FILE.write_text(current_ip)
    logger.info(f"IP address changed to {current_ip}")


def validate_ip(ip: str) -> IpProtocol:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError as e:
        logger.error(f"Invalid IP Address: {e}")
        return IpProtocol.INVALID

    return IpProtocol.IPv4 if isinstance(addr, ipaddress.IPv4Address) else IpProtocol.IPv6


def is_process_running(name: str) -> bool:
    try:
        # Run pgrep with -l to include process names in the output
        result = subprocess.run(["pgrep", "-l", "-f", name], capture_output=True, text=True)
        return name.lower() in result.stdout.lower()
    except subprocess.SubprocessError:
        pass
    return False


def main():
    if not (PROCESS_NAME and is_process_running(PROCESS_NAME)):
        logger.debug(f"Process {PROCESS_NAME} is not running. Not checking IP.")
        return

    previous_ip = None

    if CURRENT_IP_FILE.exists():
        previous_ip = CURRENT_IP_FILE.read_text().strip()

    current_ip = get_current_ip()
    if current_ip is None:
        logger.error("No IP Address retrieved.")
        return

    protocol: IpProtocol = validate_ip(current_ip)
    if protocol != IP_PROTOCOL and protocol != IpProtocol.INVALID:
        logger.warning(
            f"Received IP address {current_ip} is {protocol.value}. Expected an {IP_PROTOCOL.value} address."
        )

    if DEBUG or current_ip != previous_ip:
        notify_ip_change(new_ip=current_ip)
        update_current_ip_file(current_ip=current_ip)


if __name__ == "__main__":
    main()
