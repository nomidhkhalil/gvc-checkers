"""
GVC Greece Pakistan - 24/7 Free Telegram Bot
Runs on GitHub Actions every 5 minutes - No Laptop Needed
"""
import requests
import os
from datetime import datetime
import pytz

# --- CONFIG - GitHub Secrets se lega ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID_HERE")
START_DATE = "01/09/2026"
END_DATE = "30/09/2026"

GVC_URL = "https://pk-gr-services.gvcworld.eu/"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"Telegram sent: {r.status_code} - {r.text[:200]}")
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram failed: {e}")
        return False

def check_gvc_slots():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    try:
        print(f"[{datetime.now()}] Checking GVC: {GVC_URL}")
        resp = requests.get(GVC_URL, headers=headers, timeout=15)
        text = resp.text.lower()
        no_slot_keywords = ["no appointment", "no slot", "fully booked", "not available", "no date available"]
        has_no_slot = any(k in text for k in no_slot_keywords)
        has_calendar = "calendar" in text or "available" in text or "book" in text
        if not has_no_slot and has_calendar:
            return True, "Possible slot - 'no slot' text not found!"
        return False, "No slot"
    except Exception as e:
        print(f"Check error: {e}")
        return False, f"Error: {e}"

def main():
    pk_time = datetime.now(pytz.timezone("Asia/Karachi"))
    time_str = pk_time.strftime('%d/%m/%Y %I:%M:%S %p')
    print(f"BOT_TOKEN exists: {bool(BOT_TOKEN and 'YOUR_' not in BOT_TOKEN)}")
    print(f"CHAT_ID exists: {bool(CHAT_ID and 'YOUR_' not in CHAT_ID)}")
    found, reason = check_gvc_slots()
    if found:
        msg = f"""🇬🇷 <b>GREECE SLOT ALERT!</b> 🇬🇷
<b>Range:</b> {START_DATE} - {END_DATE}
<b>Reason:</b> {reason}
<b>Time:</b> {time_str}
<b>Link:</b> {GVC_URL}
Jaldi se login karke book karo!"""
        send_telegram(msg)
    else:
        print(f"No slot: {reason}")
        send_telegram(f"✅ Checked at {time_str}\nStatus: {reason}\nBot is working - Next check in 10 mins")

if __name__ == "__main__":
    main()
