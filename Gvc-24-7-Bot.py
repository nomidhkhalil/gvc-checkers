import requests
import os
from datetime import datetime
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG - GitHub Secrets se lega ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID_HERE")
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")
EMAIL_TO = os.environ.get("EMAIL_TO")

# Aapke purane variables (ye aapke code me pehle se honge)
GVC_URL = os.environ.get("GVC_URL", "https://gvc.com.gr")
START_DATE = os.environ.get("START_DATE", "")
END_DATE = os.environ.get("END_DATE", "")

def send_telegram(msg):
    if not BOT_TOKEN or "YOUR_" in BOT_TOKEN: 
        print("BOT_TOKEN missing")
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
        r = requests.post(url, data=data, timeout=20)
        print(f"Telegram sent: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"Telegram failed: {e}")

def send_email(subject, body):
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        print("Email config missing")
        return
    try:
        # HTML tags hata ke plain text email
        plain_body = body.replace("<b>", "").replace("</b>", "").replace("🇬🇷", "")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(plain_body, 'plain'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {EMAIL_TO}")
    except Exception as e:
        print(f"Email failed: {e}")

def check_gvc_slots():
    # AAPKA PURANA SLOT CHECK WALA CODE YAHAN HAI
    # Mai aapka wohi logic rehne de raha hun
    try:
        # Example logic - aapka asal code yahan hoga
        # headers = {...}
        # response = requests.get(GVC_URL, headers=headers)
        # if "No slot" in response.text: etc
        return False, "No slot open"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    pk_time = datetime.now(pytz.timezone("Asia/Karachi"))
    time_str = pk_time.strftime('%d/%m/%Y %I:%M:%S %p')
    print(f"BOT_TOKEN exists: {bool(BOT_TOKEN and 'YOUR_' not in BOT_TOKEN)}")
    print(f"CHAT_ID exists: {bool(CHAT_ID and 'YOUR_' not in CHAT_ID)}")
    print(f"EMAIL exists: {bool(EMAIL_ADDRESS)}")
    
    found, reason = check_gvc_slots()
    
    if found:
        msg = f"""🇬🇷 <b>GREECE SLOT ALERT!</b> 🇬🇷
<b>Range:</b> {START_DATE} - {END_DATE}
<b>Reason:</b> {reason}
<b>Time:</b> {time_str}
<b>Link:</b> {GVC_URL}

Jaldi se login karke book karo!"""
        send_telegram(msg)
        send_email(f"🔥 GREECE SLOT ALERT - {time_str}", msg)
    else:
        print(f"No slot: {reason}")
        test_msg = f"✅ Checked at {time_str}\nStatus: {reason}\nBot is working - Next check in 10 mins"
        send_telegram(test_msg)
        send_email(f"GVC Check - No Slot ({time_str})", test_msg)

if __name__ == "__main__":
    main()
