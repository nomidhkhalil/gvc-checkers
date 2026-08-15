import requests
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GVC_URL = "https://pk-gr-services.gvcworld.eu/"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, data=data)
    print(f"Telegram sent: {r.status_code}")
    return r

def check_gvc():
    print(f"[{datetime.now()}] Checking GVC: {GVC_URL}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(GVC_URL, headers=headers, timeout=20)
        text = response.text.lower()

        if "no appointment" in text or "no slot" in text or "keine termine" in text or "currently no" in text or "no appointments available" in text:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

has_slot = check_gvc()
now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")

if has_slot:
    send_telegram(f"🎉 SLOT MIL GAYA! 🎉\n\nLink: {GVC_URL}\nTime: {now}\n\nJaldi book karo!")
else:
    send_telegram(f"⏳ Check kiya: No Slot\nTime: {now}\nLink: {GVC_URL}\n\n5 min baad phir check karunga...")
