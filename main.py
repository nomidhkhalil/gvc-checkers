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
            r = requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}")
            print(f"Telegram sent: {r.status_code}")
    except Exception as e:
        print(f"Telegram Error: {e}")

    # 2. Discord - Naya Log Add Kiya
    try:
        token = os.getenv("DISCORD_TOKEN")
        ch_id = os.getenv("DISCORD_CHANNEL_ID")
        print(f"DISCORD_TOKEN exists: {bool(token)}")
        print(f"DISCORD_CHANNEL_ID exists: {bool(ch_id)}")
        
        if token and ch_id:
            headers = {"Authorization": f"Bot {token}"}
            data = {"content": message}
            url = f"https://discord.com/api/v10/channels/{ch_id}/messages"
            r = requests.post(url, headers=headers, json=data)
            print(f"Discord sent: {r.status_code} - {r.text[:200]}")
        else:
            print("Discord skipped - Token or Channel ID missing")
    except Exception as e:
        print(f"Discord Error: {e}")

# ... baaki aapka check wala code
