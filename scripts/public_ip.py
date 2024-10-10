import os

from system import System
from logger import get_logger
from email_client import send_email

logger = get_logger(__name__)

CACHE_FILE = "public_ip.txt"

def curl_ip() -> str:
    logger.info("Collecting public IP")
    code, ipaddr = System.curl_req("ifconfig.me")
    if code == 200:
        return ipaddr
    
def report_ip(ip_addr: str):
    send_email(ip_addr, "Public IP renewed", ["gbriones.gdl@gmail.com"])

def check_ip():
    old_ip = None
    new_ip = curl_ip()
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            old_ip = f.read()
    if new_ip != old_ip:
        logger.info(f"Public IP has been renewed: {new_ip}")
        with open(CACHE_FILE, 'w') as f:
            f.write(new_ip)
        report_ip(new_ip)
    else:
        logger.info(f"Public IP is still the same: {new_ip}")

if __name__ == '__main__':
    check_ip()