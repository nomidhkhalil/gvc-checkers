import requests
import os
from datetime import datetime

def send_both(message):
    # DISCORD
    try:
        d_token = os.getenv("DISCORD_TOKEN")
        d_channel = os.getenv("DISCORD_CHANNEL_ID")
        if d_token and d_channel:
            url = f"https://discord.com/api/v10/channels/{d_channel}/messages"
            headers = {"Authorization": f"Bot {d_token}", "Content-Type": "application/json"}
            requests.post(url, headers=headers, json={"content": message})
    except: pass
    
    # TELEGRAM
    try:
        t_token = os.getenv("TELEGRAM_TOKEN")
        t_chat = os.getenv("CHAT_ID")
        if t_token and t_chat:
            url = f"https://api.telegram.org/bot{t_token}/sendMessage"
            requests.post(url, json={"chat_id": t_chat, "text": message, "parse_mode": "Markdown"})
    except: pass

def check_gvc():
    print("Checking GVC slots...")
    # Yahan aapki website check hogi
    # Example: Qatar VC Islamabad
    
    # NOTE: Ye check ka tarika hai, aap apni website ka link yahan dal sakte ho
    try:
        # Test request - aap isko apni asli GVC site se replace kar dena
        # Abhi ke liye har bar alert bhejega taake aapko pata chale bot zinda hai
        now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        
        # Agar aapko sirf tab message chahiye jab slot mile, to is 'if' condition me apna logic lagao
        # Jaise: if "No Slots" not in response.text:
        
        message = f"""🚨 **GVC SLOT ALERT** 🚨

📅 Time: {now}
✅ Status: Checking... Bot is Active!
🔗 Har 5 Minute me check ho raha hai

Ye test alert hai. Jab asli slot milega tab bhi yahi pe ayega!"""
        
        send_both(message)
        print("Alert sent to both!")

    except Exception as e:
        send_both(f"❌ GVC Bot Error: {e}")

if __name__ == "__main__":
    check_gvc()
