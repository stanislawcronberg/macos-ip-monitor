from config import Config
from loguru import logger
from utils.misc import copy_ip_to_buffer, is_process_running, notify_ip_change, update_current_ip_file
from utils.network import IpProtocol, retrieve_ip, validate_ip


def main():
    PROCESS_NAME = Config.PROCESS_NAME
    CURRENT_IP_FILE = Config.CURRENT_IP_FILE
    IP_PROTOCOL: IpProtocol = Config.IP_PROTOCOL

    if not (PROCESS_NAME and is_process_running(PROCESS_NAME)) and not Config.DEBUG:
        logger.debug(f"Process {PROCESS_NAME} is not running. Not checking IP.")
        return

    previous_ip = None

    if CURRENT_IP_FILE.exists():
        previous_ip = CURRENT_IP_FILE.read_text().strip()

    current_ip = retrieve_ip(Config.IP_WEBSITE)
    if current_ip is None:
        logger.error("No IP Address retrieved.")
        return

    protocol: IpProtocol = validate_ip(current_ip)
    if protocol != IP_PROTOCOL and protocol != IpProtocol.INVALID:
        logger.warning(
            f"Received IP address {current_ip} is {protocol.value}. " f"Expected an {IP_PROTOCOL.value} address."
        )

    if Config.DEBUG or current_ip != previous_ip:
        notify_ip_change(new_ip=current_ip)
        update_current_ip_file(current_ip=current_ip)

        if Config.COPY_IP_TO_BUFFER:
            copy_ip_to_buffer(new_ip=current_ip)


if __name__ == "__main__":
    main()
