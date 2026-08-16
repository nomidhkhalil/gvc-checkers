import requests
import os
from datetime import datetime

def send_both(message):
    # Telegram
    try:
        bot_token = os.getenv("BOT_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        print(f"BOT_TOKEN exists: {bool(bot_token)}")
        print(f"CHAT_ID exists: {bool(chat_id)}")
        if bot_token and chat_id:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            r = requests.get(url, params={"chat_id": chat_id, "text": message}, timeout=10)
            print(f"Telegram sent: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"Telegram Error: {e}")

    # Discord Webhook
    try:
        webhook = os.getenv("DISCORD_WEBHOOK_URL")
        print(f"DISCORD_WEBHOOK exists: {bool(webhook)}")
        if webhook:
            webhook = webhook.strip()
            r = requests.post(webhook, json={"content": message}, timeout=10)
            print(f"Discord sent: {r.status_code} - {r.text[:500]}")
    except Exception as e:
        print(f"Discord Error: {e}")

# --- MAIN ---
print(f"[{datetime.now()}] Checking GVC: https://pk-gr-services.gvcworld.eu/")
send_both("✅ TEST SUCCESS: GitHub Bot Working! - Manual Run by Numan Baya")

# Yahan apka asal GVC check wala code ayega
# Agar slot hoga to ye neeche wala bhi chalega
try:
    # Example check - aapka purana logic yahan lagao
    # response = requests.get("https://pk-gr-services.gvcworld.eu/...")
    # if "slot" in response.text:
    #     send_both("🔥 SLOT MIL GAYA!")
    # else:
    print("No slot: No slot - but test message sent above")
except Exception as e:
    print(f"Check Error: {e}")
