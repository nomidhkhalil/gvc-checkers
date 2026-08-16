import requests
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GVC_URL = "https://pk-gr-services.gvcworld.eu/"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    r = requests.post(url, data=data)
    print(f"Telegram sent: {r.status_code}")
    return r

try:
    print(f"[{datetime.now()}] Checking GVC...")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(GVC_URL, headers=headers, timeout=20)
    text = response.text.lower()
    
    has_slot = not ("no appointment" in text or "no slot" in text or "keine" in text)
    now = datetime.now().strftime("%H:%M:%S")

    if has_slot:
        send_telegram(f"🎉 <b>SLOT MIL GAYA!</b>\nTime: {now}\n{GVC_URL}")
    else:
        send_telegram(f"⏳ No Slot - Checked at {now}")

except Exception as e:
    print(f"Error: {e}")
    send_telegram(f"Error aaya: {e}")
