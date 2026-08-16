import requests
import os
from datetime import datetime

def send_both(message):
    # Telegram
    try:
        bot_token = os.getenv("BOT_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        if bot_token and chat_id:
            requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage", params={"chat_id": chat_id, "text": message})
            print("Telegram sent: 200")
    except Exception as e:
        print(f"Telegram Error: {e}")

    # Discord Webhook - sabse asaan
    try:
        webhook = os.getenv("DISCORD_WEBHOOK_URL")
        print(f"DISCORD_WEBHOOK exists: {bool(webhook)}")
        if webhook:
            r = requests.post(webhook.strip(), json={"content": message})
            print(f"Discord sent: {r.status_code} - {r.text[:500]}")
        else:
            print("Discord webhook missing")
    except Exception as e:
        print(f"Discord Error: {e}")

url_to_check = "https://pk-gr-services.gvcworld.eu/"
print(f"[{datetime.now()}] Checking GVC")

try:
    page = requests.get(url_to_check, timeout=10)
    if "No slot" in page.text or "no slot" in page.text.lower():
        send_both("❌ GVC: No slot available")
    else:
    print("No slot: No slot")
    send_both("✅ TEST: Bot is working! Telegram + Discord connected - Numan Baya")
