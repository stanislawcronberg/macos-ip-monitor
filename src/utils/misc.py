import subprocess

import pyperclip
from config import Config
from logger_config import logger
from pync import Notifier


def is_process_running(name: str) -> bool:
    try:
        result = subprocess.run(["pgrep", "-l", "-f", name], capture_output=True, text=True)
        return name.lower() in result.stdout.lower()
    except subprocess.SubprocessError:
        pass
    return False


def notify_ip_change(new_ip: str | None) -> None:
    message = f"Your public IP address has changed to {new_ip}."
    Notifier.notify(title="IP Address Change", message=message, open=Config.NOTIFICATION_LINK)


def update_current_ip_file(current_ip: str) -> None:
    Config.CURRENT_IP_FILE.write_text(current_ip)
    logger.info(f"IP address changed to {current_ip}")


def copy_ip_to_buffer(new_ip: str):
    pyperclip.copy(new_ip)
    logger.debug(f"Copying IP {new_ip} to buffer.")
