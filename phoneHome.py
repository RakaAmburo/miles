from dotenv import load_dotenv
import os
import subprocess
from tools import get_logger, handle_exception, publish_event
import sys
from datetime import datetime, time as dt_time
import time
from state_mgr import get_state
import constants as const

sys.excepthook = handle_exception

logger = get_logger("phone-home")

load_dotenv()

PHONE_MAC = os.getenv("PHONE_MAC")
PHONE_IP = os.getenv("PHONE_IP")
PING_FLAG = os.getenv("PING_FLAG", "-n")# win default

INTERVAL = 60  # seconds

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
def is_in_range(start: dt_time, end: dt_time) -> bool:
    now = datetime.now().time()
    if start > end:  
        return now >= start or now <= end
    return start <= now <= end

was_home = True

while True:
    at_home = (is_in_range(dt_time(22, 30), dt_time(9, 0)) and not is_full_armed()) or is_home()
    
    if was_home and not at_home:
        publish_event(const.TOPIC_MOVIL, const.OUT)
    
    if not was_home and at_home:
        publish_event(const.TOPIC_MOVIL, const.IN)
    
    was_home = at_home
    time.sleep(INTERVAL)