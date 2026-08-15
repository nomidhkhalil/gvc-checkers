"""
GVC Greece Pakistan - 24/7 Free Telegram Bot
Runs on GitHub Actions every 5 minutes - No Laptop Needed
"""

import requests
import time
from datetime import datetime

# --- CONFIG - Yahan apna Token aur Chat ID dalo ---
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # e.g. 1234567890:AAH_abc...
CHAT_ID = "YOUR_CHAT_ID_HERE"      # e.g. 1987654321
START_DATE = "01/09/2026"
END_DATE = "30/09/2026"

# GVC Check URL - ye site ka main page hai
GVC_URL = "https://pk-gr-services.gvcworld.eu/"

# Telegram send function
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"Telegram sent: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram failed: {e}")
        return False

# GVC Check logic
def check_gvc_slots():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    try:
        print(f"[{datetime.now()}] Checking GVC: {GVC_URL}")
        resp = requests.get(GVC_URL, headers=headers, timeout=15)
        text = resp.text.lower()
        
        # Check for signs of availability
        no_slot_keywords = ["no appointment", "no slot", "fully booked", "not available", "no date available"]
        has_no_slot = any(k in text for k in no_slot_keywords)
        
        # If page contains calendar or booking button and no "no slot" text
        has_calendar = "calendar" in text or "available" in text or "book" in text
        
        # For GVC, actual slot detection needs deeper parsing of their API
        # This is a basic check - if "no slot" text disappears, we alert
        # You can enhance by checking their AJAX endpoint: /api/appointments etc.
        
        if not has_no_slot and has_calendar:
            return True, "Possible slot - 'no slot' text not found!"
        
        # Also try to find their API endpoint (inspect browser Network tab for exact URL)
        # Example (you need to update this after inspecting):
        # api_url = "https://pk-gr-services.gvcworld.eu/api/calendar/dates?month=9&year=2026"
        # api_resp = requests.get(api_url, headers=headers, timeout=10)
        # if '"available":true' in api_resp.text.lower():
        #     return True, f"API shows available dates! {api_resp.text[:200]}"
        
        return False, "No slot"
        
    except Exception as e:
        print(f"Check error: {e}")
        return False, f"Error: {e}"

def main():
    found, reason = check_gvc_slots()
    if found:
        msg = f"""🇬🇷 <b>GREECE SLOT ALERT!</b> 🇬🇷

<b>Range:</b> {START_DATE} - {END_DATE}
<b>Reason:</b> {reason}
<b>Time:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
<b>Link:</b> {GVC_URL}

Jaldi se login karke book karo!
Bot by: GVC GR-PK V4
"""
        send_telegram(msg)
        print("SLOT FOUND - Alert sent")
    else:
        print(f"No slot: {reason}")
        # Optional: send heartbeat once a day to know bot is alive
        # Uncomment if you want
        # if datetime.now().hour == 9 and datetime.now().minute < 10:
        #     send_telegram(f"✅ Bot Alive - Checked at {datetime.now()} - No slot yet")

if __name__ == "__main__":
    main()
