from dotenv import load_dotenv
import os
import subprocess
import time
import requests

load_dotenv()

PHONE_MAC = os.getenv("PHONE_MAC")
PHONE_IP = os.getenv("PHONE_IP")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

INTERVAL = 60  # seconds

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

def is_home(retries=3, delay=5):
    for attempt in range(retries):
        #subprocess.run(['ping', '-n', '1', PHONE_IP], capture_output=True)
        subprocess.run(['ping', '-c', '1', PHONE_IP], capture_output=True)
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        print(result.stdout)
        if PHONE_MAC.lower() in result.stdout.lower():
            print("telephone found")
            return True
        print(f"failed attempt: {attempt}") 
        time.sleep(delay)
    return False

was_home = True

while True:
    at_home = is_home()
    
    if was_home and not at_home:
        send_telegram("🚨 Phone left home!")
    
    if not was_home and at_home:
        send_telegram("✅ Phone is back home!")
    
    was_home = at_home
    time.sleep(INTERVAL)