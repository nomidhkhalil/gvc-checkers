import requests
import os
from datetime import datetime

def send_both(message):
    # 1. DISCORD PE BHEJO
    try:
        d_token = os.getenv("DISCORD_TOKEN")
        d_channel = os.getenv("DISCORD_CHANNEL_ID")
        if d_token and d_channel:
            url = f"https://discord.com/api/v10/channels/{d_channel}/messages"
            headers = {"Authorization": f"Bot {d_token}", "Content-Type": "application/json"}
            requests.post(url, headers=headers, json={"content": message})
            print("Discord Sent")
    except Exception as e:
        print(f"Discord Error: {e}")

    # 2. TELEGRAM PE BHEJO
    try:
        t_token = os.getenv("TELEGRAM_TOKEN")
        t_chat = os.getenv("CHAT_ID")
        if t_token and t_chat:
            url = f"https://api.telegram.org/bot{t_token}/sendMessage"
            requests.post(url, json={"chat_id": t_chat, "text": message})
            print("Telegram Sent")
    except Exception as e:
        print(f"Telegram Error: {e}")

def check():
    now = datetime.now().strftime("%d-%m %H:%M")
    msg = f"🔔 GVC Alert Test - {now}\nYe message Telegram + Discord dono pe aa raha hai!"
    send_both(msg)

check()
