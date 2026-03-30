from dotenv import load_dotenv
import os
import subprocess
import time
import requests
from tools import get_logger, handle_exception
import sys
from datetime import datetime, time as dt_time
from state_mgr import get_state
import constants as const

sys.excepthook = handle_exception

logger = get_logger("phone-home")

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

def is_home(retries=14, delay=30):
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

def is_full_armed():
    state = get_state(const.FULL_ARMED)
    return state == const.ON

# result = is_in_range(time(22, 30), time(8, 0))
def is_in_range(start: time, end: dt_time) -> bool:
    now = datetime.now().time()
    if start > end:  
        return now >= start or now <= end
    return start <= now <= end

was_home = True

while True:
    at_home = is_home() #or (is_in_range() and not full_armed())
    
    if was_home and not at_home:
        send_telegram("🚨 Phone left home!")
    
    if not was_home and at_home:
        send_telegram("✅ Phone is back home!")
    
    was_home = at_home
    time.sleep(INTERVAL)