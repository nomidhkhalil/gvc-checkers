import requests
import os
from datetime import datetime

def send_both(message):
    # 1. Discord
    try:
        token = os.getenv("DISCORD_TOKEN")
        ch_id = os.getenv("DISCORD_CHANNEL_ID")
        if token and ch_id:
            url = f"https://discord.com/api/v10/channels/{ch_id}/messages"
            headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
            requests.post(url, headers=headers, json={"content": message})
    except Exception as e:
        print(f"Discord Error {e}")

    # 2. Telegram
    try:
        BOT_TOKEN = os.getenv("BOT_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")
        if t_token and chat_id:
            url = f"https://api.telegram.org/bot{t_token}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": message})
    except Exception as e:
        print(f"Telegram Error {e}")

def main():
    now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    msg = f"✅ GVC Bot Active - {now}\nHar 5 min check ho raha hai - Discord + Telegram OK!"
    send_both(msg)

main()
