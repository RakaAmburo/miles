import logging
import sys
import traceback
from datetime import datetime
import requests
import os


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(name)

""" def handle_exception(exc_type, exc_value, exc_traceback):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} - CRITICAL - Unhandled exception", file=sys.stderr)
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr) """

def handle_exception(exc_type, exc_value, exc_traceback):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tb = traceback.extract_tb(exc_traceback)[-1]
    module = tb.filename.split("/")[-1].replace(".py", "")
    print(f"{timestamp} - {module} - CRITICAL - Unhandled exception", file=sys.stderr)
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)