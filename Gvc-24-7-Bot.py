import requests, os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EVENT = os.getenv("EVENT_NAME", "")

def send(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.get(url, params={"chat_id": CHAT_ID, "text": msg}, timeout=15)
        print(f"Telegram sent: {r.status_code}")
    except Exception as e:
        print(f"Telegram error: {e}")

print(f"[{datetime.now()}] Checking GVC: https://pk-gr-services.gvcworld.eu/ - Event: {EVENT}")

try:
    r = requests.get("https://pk-gr-services.gvcworld.eu/", headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    has_no_slot = "no slot" in r.text.lower() or "kein termin" in r.text.lower()
    
    if not has_no_slot:
        send("🔥🔥🔥 GVC SLOT MIL GAYA BAYA! https://pk-gr-services.gvcworld.eu/")
        print("SLOT FOUND")
    else:
        print("No slot: No slot")
        # Manual hoga to bata dega, Auto hoga to chup rahega
        if slots_found:
    send_telegram(...)
else:
    send_telegram(...)

except Exception as e:
    print(f"Error: {e}")
    if "workflow_dispatch" in EVENT:
        send(f"Error on manual check: {e}")
