from dotenv import load_dotenv
import os
import subprocess
import time
import requests
from tools import get_logger
import sys
import traceback
from datetime import datetime

logger = get_logger(__name__)

load_dotenv()

PHONE_MAC = os.getenv("PHONE_MAC")
PHONE_IP = os.getenv("PHONE_IP")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PING_FLAG = os.getenv("PING_FLAG", "-n")# win default

INTERVAL = 60  # seconds

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

def is_home(retries=10, delay=30):
    for attempt in range(retries):
        subprocess.run(['ping', PING_FLAG, '1', PHONE_IP], capture_output=True)
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        #print(result.stdout)
        if PHONE_MAC.lower() in result.stdout.lower():
            logger.info("telephone found")
            return True
        logger.error(f"failed attempt: {attempt}") 
        time.sleep(delay)
    return False

def handle_exception(exc_type, exc_value, exc_traceback):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} - CRITICAL - Unhandled exception", file=sys.stderr)
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

sys.excepthook = handle_exception

was_home = True

while True:
    at_home = is_home()
    
    if was_home and not at_home:
        send_telegram("🚨 Phone left home!")
    
    if not was_home and at_home:
        send_telegram("✅ Phone is back home!")
    
    was_home = at_home
    time.sleep(INTERVAL)