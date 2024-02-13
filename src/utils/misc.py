import subprocess
from pathlib import Path

import pyperclip
from config import Config
from loguru import logger
from pync import Notifier

# TODO: Add function for checking platform is Darwin or Linux


def is_process_running(name: str) -> bool:
    try:
        result = subprocess.run(["pgrep", "-l", "-f", name], capture_output=True, text=True)
        return name.lower() in result.stdout.lower()
    except subprocess.SubprocessError:
        pass
    return False


def notify_ip_change(new_ip: str | None) -> None:
    message = f"Your public IP address has changed to {new_ip}."
    Notifier.notify(title="IP Address Change", message=message, open=Config.NOTIFICATION_URL)


def update_current_ip_file(current_ip: str, current_ip_file: Path) -> None:
    current_ip_file.write_text(current_ip)
    logger.info(f"IP address changed to {current_ip}")


def copy_ip_to_buffer(new_ip: str):
    pyperclip.copy(new_ip)
    logger.debug(f"Copying IP {new_ip} to buffer.")
