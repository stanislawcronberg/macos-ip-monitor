from pathlib import Path

from config import Config
from loguru import logger
from utils.misc import copy_ip_to_buffer, is_process_running, notify_ip_change, update_current_ip_file
from utils.network import IpProtocol, get_ip_protocol, retrieve_ip


def main():
    PROCESS_NAME = Config.PROCESS_NAME
    IP_PROTOCOL: IpProtocol = Config.IP_PROTOCOL
    CURRENT_IP_FILE = Path(".current_ip.txt")

    # If the DEBUG flag is False, or the PROCESS_NAME is specified but not running,
    # then the script exits without checking the IP address.
    if not (Config.DEBUG or (PROCESS_NAME and is_process_running(PROCESS_NAME))):
        logger.debug(f"Process {PROCESS_NAME} is not running. Not checking IP.")
        return

    if Config.DEBUG:
        logger.info()

    # If the CURRENT_IP_FILE exists, then the previous IP address is retrieved.
    previous_ip = None
    if CURRENT_IP_FILE.exists():
        previous_ip = CURRENT_IP_FILE.read_text().strip()

    current_ip = retrieve_ip(Config.PUBLIC_IP_URL)
    if current_ip is None:
        logger.error("No IP Address retrieved.")
        return

    protocol: IpProtocol | None = get_ip_protocol(current_ip)
    if protocol != IP_PROTOCOL:
        logger.warning(
            f"Received IP address {current_ip} is {protocol.value}. Expected an {IP_PROTOCOL.value} address."
        )
    elif protocol is None:
        logger.error(f"Could not parse IP protocol for {current_ip}")
        return

    # If the DEBUG flag is True, or the IP address has changed,
    # then the IP address is updated and a notification is sent.
    if Config.DEBUG or current_ip != previous_ip:
        notify_ip_change(new_ip=current_ip)
        update_current_ip_file(current_ip=current_ip, current_ip_file=CURRENT_IP_FILE)

        if Config.COPY_IP_TO_BUFFER:
            copy_ip_to_buffer(new_ip=current_ip)


if __name__ == "__main__":
    main()
