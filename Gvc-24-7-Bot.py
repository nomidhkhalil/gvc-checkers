import requests
import os
from datetime import datetime

def send_both(message):
    # 1. Telegram
    try:
        bot_token = os.getenv("BOT_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        print(f"BOT_TOKEN exists: {bool(bot_token)}")
        print(f"CHAT_ID exists: {bool(chat_id)}")
        if bot_token and chat_id:
            r = requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage", params={"chat_id": chat_id, "text": message})
            print(f"Telegram sent: {r.status_code}")
    except Exception as e:
        print(f"Telegram Error: {e}")

    # 2. Discord
    try:
        token = os.getenv("DISCORD_TOKEN")
        ch_id = os.getenv("DISCORD_CHANNEL_ID")
        print(f"DISCORD_TOKEN exists: {bool(token)}")
        print(f"DISCORD_CHANNEL_ID exists: {bool(ch_id)}")
        if token and ch_id:
            headers = {"Authorization": f"Bot {token.strip()}"}
            data = {"content": message}
            url = f"https://discord.com/api/v10/channels/{ch_id.strip()}/messages"
            r = requests.post(url, headers=headers, json=data)
            print(f"Discord sent: {r.status_code} - {r.text[:300]}")
        else:
            print("Discord skipped - Token or Channel ID missing")
    except Exception as e:
        print(f"Discord Error: {e}")

# --- GVC Check ---
url_to_check = "https://pk-gr-services.gvcworld.eu/"
print(f"[{datetime.now()}] Checking GVC: {url_to_check}")

try:
    page = requests.get(url_to_check, timeout=10)
    if "No slot" in page.text or "no slot" in page.text.lower():
        print("No slot: No slot")
        send_both("❌ GVC: No slot available")
    else:
        print("Slot FOUND!")
        send_both("✅ GVC SLOT FOUND! Jaldi check karo: " + url_to_check)
except Exception as e:
    print(f"Check error: {e}")
    send_both(f"Error checking GVC: {e}")
