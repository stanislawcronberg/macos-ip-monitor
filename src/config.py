import os

from dotenv import load_dotenv
from utils.network import IpProtocol

load_dotenv()


# TODO: Create .env.sample file with the default values
class Config:
    IP_PROTOCOL = IpProtocol[os.getenv("IP_PROTOCOL", "IPv4")]
    PROCESS_NAME = os.getenv("PROCESS_NAME", "")
    PUBLIC_IP_URL = os.getenv("PUBLIC_IP_URL", "https://ipinfo.io")
    NOTIFICATION_URL = os.getenv("NOTIFICATION_URL", "https://azure.com")
    COPY_IP_TO_BUFFER = os.getenv("COPY_IP_TO_BUFFER", "False") == "True"
    DEBUG = os.getenv("DEBUG", "False") == "True"
