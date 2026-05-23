import requests
import argparse
from dotenv import load_dotenv
load_dotenv()
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message=None, image_path=None):
    if image_path:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        with open(image_path, "rb") as photo:
            data = {"chat_id": CHAT_ID}
            if message:
                data["caption"] = message
            response = requests.post(url, data=data, files={"photo": photo})
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        response = requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    
    if not response.ok:
        print(f"Telegram error: {response.status_code} {response.text}")

parser = argparse.ArgumentParser()
parser.add_argument("--message", help="Mensaje a enviar")
parser.add_argument("--image", help="Ruta de la imagen")
args = parser.parse_args()

send_telegram(message=args.message, image_path=args.image)