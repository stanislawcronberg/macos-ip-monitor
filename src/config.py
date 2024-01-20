import os
from pathlib import Path

from dotenv import load_dotenv
from utils.network import IpProtocol

load_dotenv()


class Config:
    IP_PROTOCOL = IpProtocol[os.getenv("IP_PROTOCOL", "IPv4")]
    PROCESS_NAME = os.getenv("PROCESS_NAME", "")
    IP_WEBSITE = os.getenv("IP_WEBSITE", "https://ipinfo.io")
    NOTIFICATION_LINK = os.getenv("NOTIFICATION_LINK", "https://azure.com")
    CURRENT_IP_FILE = Path(os.getenv("CURRENT_IP_FILEPATH", "logs/current_ip.txt"))
    DEBUG = os.getenv("DEBUG", "False") == "True"
    COPY_IP_TO_BUFFER = os.getenv("COPY_IP_TO_BUFFER", "False") == "True"
